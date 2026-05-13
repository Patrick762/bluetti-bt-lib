"""Custom exceptions for Bluetti Bluetooth communication."""


class BluettiBluetoothError(Exception):
    """Base exception for Bluetti Bluetooth communication errors."""
    pass


class DeviceNotFoundError(BluettiBluetoothError):
    """The BLE device was not found during scanning.

    The device may be out of range or powered off.
    """
    pass


class ConnectionFailedError(BluettiBluetoothError):
    """The BLE device was found but the connection could not be established.

    Another Bluetooth client may already be connected to the device.
    """
    pass


class EncryptionHandshakeError(BluettiBluetoothError):
    """The BLE connection was established but the encryption handshake failed.

    This likely indicates a library bug. Please open an issue.
    """
    pass
