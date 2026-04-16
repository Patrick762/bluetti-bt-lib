"""Decode register blocks from a bluetti_data.json dump."""

import json
import struct
import sys


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from(">H", data, offset * 2)[0]


def decode_block(start: int, data: bytes) -> None:
    for i in range(len(data) // 2):
        val = u16(data, i)
        print(f"  reg {start + i:4d}: {val:6d}  (0x{val:04x})")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "bluetti_data.json"
    with open(path) as f:
        dump = json.load(f)

    registers = dump["registers"]
    print(f"MAC: {dump['mac']}  IoT v{dump['iotVersion']}  encryption={dump['encryption']}")
    print()

    for key in sorted(registers.keys(), key=int):
        hex_str = registers[key]
        if not hex_str:
            continue
        data = bytes.fromhex(hex_str)
        start = int(key)
        print(f"=== Block {start} (regs {start}–{start + len(data)//2 - 1}) ===")

        # Try ASCII if the bytes look printable
        try:
            ascii_str = data.decode("ascii").strip("\x00").strip()
            if ascii_str and all(32 <= ord(c) < 127 for c in ascii_str):
                print(f"  ascii: {ascii_str!r}")
        except Exception:
            pass

        decode_block(start, data)
        print()


if __name__ == "__main__":
    main()
