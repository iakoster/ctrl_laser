from typing import Any

import serial
import serial.tools.list_ports as list_ports

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
            dsrdtr=True,
        )
        super().__init__(hapi, address="PC", logger="self")

    def close(self) -> None:
        self._hapi.close()

    def setup(self, *args: Any, **kwargs: Any) -> "UART":
        return self

    def _bind(self, address: ADDRESS_TYPE) -> None:
        if self._addr != address:
            raise ValueError("you can't change address")

    def _receive(self) -> tuple[bytes, ADDRESS_TYPE]:
        return self._hapi.read(1024), self._hapi.port

    def _transmit(self, message: Message) -> None:
        self._hapi.write(message.to_bytes())

    @staticmethod
    def get_available_com_ports() -> list[str]:
        return [port.name for port in list_ports.comports()]
