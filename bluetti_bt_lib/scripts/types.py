from dataclasses import dataclass


@dataclass
class ReadallData:
    mac: str
    iotVersion: int
    encryption: bool
    registers: dict[str, str]

    def toJSON(self):
        return {
            "mac": self.mac,
            "iotVersion": self.iotVersion,
            "encryption": self.encryption,
            "registers": self.registers,
        }
