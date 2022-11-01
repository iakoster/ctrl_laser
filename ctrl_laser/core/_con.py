import serial
from typing import Any

from pyinstr_iakoster.communication import Connection, Message


__all__ = [
    "UART",
]


class UART(Connection):

    _hapi: serial.Serial
    ADDRESS_TYPE = str

    def __init__(
            self,
            port: str,
            baudrate: int = 9600,
            timeout: float = 0.3
    ):

        hapi = serial.Serial(
            port,
            baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout,
            xonxoff=False,
            rtscts=False,
            dsrdtr=True
        )
        super().__init__(hapi, address="PC", logger="self")

    def close(self) -> None:
        self._hapi.close()

    def setup(self, *args: Any, **kwargs: Any) -> Connection:
        pass

    def _bind(self, address: ADDRESS_TYPE) -> None:
        if hasattr(self, "_addr"):
            raise ValueError("you can't change address")

    def _receive(self) -> tuple[bytes, ADDRESS_TYPE]:
        return self._hapi.read(1024), self._hapi.port

    def _transmit(self, message: Message) -> None:
        self._hapi.write(message.to_bytes())
