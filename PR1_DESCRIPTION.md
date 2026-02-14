# PR 1: Scan – timeout, dedupe, fix --timeout 0 hang

## Pushing (this fork only)

**All work stays in this fork (mzpwr/bluetti-bt-lib). Do not push to or open PRs against the original repository (Patrick762/bluetti-bt-lib).**

To push this branch using SSH, ensure `origin` points to **this fork** only:

```bash
git remote set-url origin git@github.com:mzpwr/bluetti-bt-lib.git
git push -u origin Develop
```

Open any pull requests against branches in **this fork** (mzpwr/bluetti-bt-lib), not the original repo.

## Summary
Improves `bluetti-scan` with an optional duration mode, deduplication by address, and a fix for `--timeout 0` hanging.

## Changes
- **`-t / --timeout SECONDS`** (optional): When set, scan for the given number of seconds and list every discovered device once. When omitted, behavior is unchanged: stop as soon as the first supported device is found.
- **Deduplication by address**: Each device is reported at most once (by BLE address), so long timeouts no longer repeat the same device.
- **PBOX handling**: Devices whose name starts with `PBOX` are included in timeout mode and reported as type `PBOX`.
- **`--timeout 0` fix**: A zero timeout no longer hangs. The condition now uses `timeout_seconds is not None` (instead of `... and timeout_seconds > 0`), so `asyncio.sleep(0)` runs and the scanner exits instead of waiting on `stop_event`, which is never set when a numeric timeout is provided.

## Usage
```bash
# Legacy: stop at first device
bluetti-scan

# Scan 15 seconds, list all devices (deduplicated)
bluetti-scan --timeout 15

# Zero timeout: exit immediately (no hang)
bluetti-scan --timeout 0
```

## Testing
- Run `bluetti-scan` with no args: should stop at first device.
- Run `bluetti-scan --timeout 5`: should run ~5 seconds and list devices.
- Run `bluetti-scan --timeout 0`: should exit immediately without hanging.
