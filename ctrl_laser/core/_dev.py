from pyinstr_iakoster.communication import Message

from ._pf import PF
from ._con import UART


__all__ = ["Arduino"]


class Arduino(object):

    def __init__(
            self,
            port: str
    ):
        self._con = UART(port)
        self._pf = PF

    def read_firmware_version(self) -> list[int]:
        ans = self.send(
            self._pf["firmware_ver"].read(response=0, data_length=b"\x00")
        )
        version = []
        for byte in ans.data.content:
            version.append(byte)
        return version

    def read_update_date(self) -> list[int]:
        ans = self.send(
            self._pf["update_date"].read(response=0, data_length=b"\x00")
        )
        val = ans.data.unpack()[0]
        return [val // 10000, val // 100 % 100, val % 100]

    def read_timer_frequency(self) -> int:
        return self.send(
            self._pf["timer_frequency"].read(response=0, data_length=b"\x00")
        ).data.unpack()[0]

    def read_regime(self) -> int:
        return self.send(
            self._pf["regime"].read(response=0, data_length=b"\x00")
        ).data.unpack()[0]

    def read_pulse_period(self) -> int:
        return self.send(
            self._pf["pulse_period"].read(response=0, data_length=b"\x00")
        ).data.unpack()[0]

    def read_pulse_width(self) -> int:
        return self.send(
            self._pf["pulse_width"].read(response=0, data_length=b"\x00")
        ).data.unpack()[0]

    def send(self, msg: Message) -> Message:
        msg.set_src_dst(src="PC", dst=self.address)
        return self._con.send(msg)

    def write_regime(self, regime: int) -> int:
        return self.send(
            self._pf["regime"].write(regime, response=0)
        ).data.unpack()[0]

    def write_pulse_period(self, period: int) -> int:
        return self.send(
            self._pf["pulse_period"].write(period, response=0)
        ).data.unpack()[0]

    def write_pulse_width(self, width: int) -> int:
        return self.send(
            self._pf["pulse_width"].write(width, response=0)
        ).data.unpack()[0]

    @property
    def address(self):
        return self._con.hapi.port

    @property
    def connection(self) -> UART:
        return self._con

    def __del__(self) -> None:
        self._con.close()

