"""Long-running Bluetti register poller. Writes data/snapshots.jsonl."""

import argparse
import asyncio
import json
import signal
import struct
import time
from datetime import datetime
from pathlib import Path

from bluetti_bt_lib.base_devices import BaseDeviceV2
from bluetti_bt_lib.bluetooth.device_reader import DeviceReader, DeviceReaderConfig

BLUETTI_UUID = "A7108915-E5F4-F6E6-BA0B-2CFA96DF1397"
OUTPUT = Path(__file__).parent.parent / "data" / "snapshots.jsonl"

# Known fields: reg -> (label, unit, scale)
KNOWN = {
    102:  ("SoC",    "%",  1.0),
    140:  ("DC_out", "W",  1.0),
    142:  ("AC_out", "W",  1.0),
    144:  ("DC_in",  "W",  1.0),
    146:  ("AC_in",  "W",  1.0),
    1314: ("Vac",    "V",  0.1),
}


def get_reg(registers: dict, reg: int) -> int | None:
    """Extract a uint16 value for a specific register number."""
    block = 1 + ((reg - 1) // 10) * 10
    hex_str = registers.get(str(block), "")
    if not hex_str:
        return None
    offset = reg - block
    data = bytes.fromhex(hex_str)
    if offset * 2 + 2 > len(data):
        return None
    return struct.unpack_from(">H", data, offset * 2)[0]


def flatten(registers: dict) -> dict[int, int]:
    """Expand register blocks into {reg_num: uint16} for diffing."""
    flat: dict[int, int] = {}
    for key, hex_str in registers.items():
        if not hex_str:
            continue
        start = int(key)
        data = bytes.fromhex(hex_str)
        for i in range(len(data) // 2):
            flat[start + i] = struct.unpack_from(">H", data, i * 2)[0]
    return flat


def format_known(registers: dict) -> str:
    parts = []
    for reg, (name, unit, scale) in KNOWN.items():
        val = get_reg(registers, reg)
        if val is not None:
            parts.append(f"{name}:{val * scale:.1f}{unit}" if scale != 1.0 else f"{name}:{val}{unit}")
    return "  ".join(parts)


async def run(args: argparse.Namespace) -> None:
    device = BaseDeviceV2()
    reader = DeviceReader(
        BLUETTI_UUID,
        device,
        asyncio.Future,
        DeviceReaderConfig(use_encryption=True, timeout=55),
    )

    OUTPUT.parent.mkdir(exist_ok=True)

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, stop.set)
    loop.add_signal_handler(signal.SIGTERM, stop.set)

    seq = 0
    prev_flat: dict[int, int] = {}

    print(f"Polling {BLUETTI_UUID}")
    print(f"Interval: {args.interval}s  |  Output: {OUTPUT}")
    print("Ctrl+C to stop cleanly.\n")

    while not stop.is_set():
        ts = datetime.now().isoformat(timespec="seconds")
        t0 = time.monotonic()

        data = await reader.read(
            only_registers=device.get_full_registers_range(),
            raw=True,
        )

        took_ms = int((time.monotonic() - t0) * 1000)
        ok = data is not None
        registers = {str(k): v.hex() for k, v in data.items()} if ok else {}

        # Write snapshot
        snapshot = {"ts": ts, "seq": seq, "ok": ok, "took_ms": took_ms, "registers": registers}
        with OUTPUT.open("a") as f:
            f.write(json.dumps(snapshot) + "\n")

        # Build terminal line
        flag = "ok  " if ok else "FAIL"
        line = f"[{ts[11:]}] #{seq:<4} {flag} {took_ms / 1000:4.1f}s"
        if ok:
            line += "  " + format_known(registers)

        # Diff against previous successful snapshot
        if ok:
            cur_flat = flatten(registers)
            if prev_flat:
                changed = {
                    r: (prev_flat[r], cur_flat[r])
                    for r in cur_flat
                    if r in prev_flat and prev_flat[r] != cur_flat[r]
                }
                if changed:
                    if len(changed) <= 8:
                        diff = "  ".join(f"r{r}:{old}→{new}" for r, (old, new) in sorted(changed.items()))
                    else:
                        sample = "  ".join(
                            f"r{r}:{old}→{new}" for r, (old, new) in list(sorted(changed.items()))[:6]
                        )
                        diff = f"{sample}  … (+{len(changed) - 6} more)"
                    line += f"\n          ** {diff} **"
            prev_flat = cur_flat

        print(line, flush=True)
        seq += 1

        try:
            await asyncio.wait_for(stop.wait(), timeout=args.interval)
        except asyncio.TimeoutError:
            pass

    print("\nStopped.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Poll Bluetti registers → data/snapshots.jsonl")
    parser.add_argument(
        "--interval", type=int, default=60, metavar="SECONDS",
        help="seconds between reads (default: 60)",
    )
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
