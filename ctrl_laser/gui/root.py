from __future__ import annotations

from PyQt5.QtWidgets import QMainWindow, QMessageBox
import qtawesome as qta

from .py_ui import Ui_root
from ..core import Arduino, UART


__all__ = ["WinRoot"]


class UiRoot(Ui_root):

    def __init__(self, root: WinRoot):
        self.setupUi(root)
        self.parent = root

        self._setup_parent()
        self._setup_ui()

    def connected(self, connected: bool) -> None:

        if connected:
            connect_icon = qta.icon(
                "mdi.lan-connect", options=[{'color': "#11aa11"}]
            )
        else:
            connect_icon = qta.icon(
                "mdi.lan-disconnect", options=[{'color': "#aa1111"}]
            )
        self.connect.setIcon(connect_icon)
        self._port.setEnabled(not connected)

        for wid in (
            self._regime,
            self.read_regime,
            self.write_regime,
            self.set_regime_off,
            self._pulse_period,
            self.read_pulse_period,
            self.write_pulse_period,
            self._pulse_width,
            self.read_pulse_width,
            self.write_pulse_width,
        ):
            wid.setEnabled(connected)

        if not connected:
            self._clear_firmware_info()

    def _clear_firmware_info(self) -> None:
        for wid in (
            self._firmware_version,
            self._firmware_date,
            self._timer_frequency,
        ):
            wid.setText("Unknown")

    def _setup_parent(self) -> None:
        self.parent.setFixedSize(360, 240)

    def _setup_ui(self) -> None:
        self.connected(False)

        for wid in (
            self.write_regime, self.write_pulse_period, self.write_pulse_width
        ):
            wid.setIcon(qta.icon("ri.upload-2-fill"))

        for wid in (
            self.read_regime, self.read_pulse_period, self.read_pulse_width
        ):
            wid.setIcon(qta.icon("ri.download-2-fill"))

    @property
    def firmware_date(self) -> str:
        return self._firmware_date.text()

    @firmware_date.setter
    def firmware_date(self, date: list[int]) -> None:
        self._firmware_date.setText(".".join(map(str, date)))

    @property
    def firmware_version(self) -> str:
        return self._firmware_version.text()

    @firmware_version.setter
    def firmware_version(self, version: list[int]) -> None:
        self._firmware_version.setText(".".join(map(str, version)))

    @property
    def port(self) -> str:
        return self._port.currentText()

    @port.setter
    def port(self, port: str | list[str]) -> None:
        if isinstance(port, str):
            self._port.setCurrentText(port)
        else:
            self._port.clear()
            self._port.addItems(port)

    @property
    def timer_frequency(self) -> int:
        return int(self._timer_frequency.text())

    @timer_frequency.setter
    def timer_frequency(self, freq: int) -> None:
        self._timer_frequency.setText(str(freq))


class WinRoot(QMainWindow):

    dev: Arduino

    def __init__(self):
        super().__init__()
        self.ui = UiRoot(self)

        self.ui.port = UART.get_available_com_ports()

        self._attach_signals()

    def connect(self) -> None:

        if self.is_connected:
            del self.dev
            self.ui.connected(self.is_connected)
            return

        self.dev = Arduino(self.ui.port)

        try:
            self.ui.firmware_version = self.dev.read_firmware_version()
            self.ui.firmware_date = self.dev.read_update_date()
            self.ui.timer_frequency = self.dev.read_timer_frequency()
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Ошибка подключения",
                f"Не получилось подключиться к плате Arduino\n{exc}"
            )
            del self.dev
        else:
            self.ui.connected(self.is_connected)

    def _attach_signals(self) -> None:
        self.ui.connect.clicked.connect(self.connect)

    @property
    def is_connected(self) -> bool:
        return hasattr(self, "dev")
