# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- **LED panel state (register 2007, read-only)**: Generalized support for devices with an LED panel (AC60, EL10). New shared enum `LedPanelState` (in `enums.led_mode`): OFF=0, NORMAL=1, BRIGHT=2, BLINKING=3. Both AC60 and EL10 expose `LED_MODE` (`led_mode`) as a read-only field; the device does not accept writes to this register. Use `bluetti-read` to see the value.

### Fixed

- **bluetti-read encryption flag**: The `--encryption` option now works correctly. It is a proper flag (`-e` / `--encryption`); use it when the device requires encryption (e.g. **Handsfree 1**). Previously the option used `type=bool`, which did not parse correctly.

### Note for users of encrypted devices

- **Handsfree 1** and some other devices use encryption. When reading or interacting with them, pass the encryption flag:  
  `bluetti-read -m <address> -t "Handsfree 1" --encryption`
