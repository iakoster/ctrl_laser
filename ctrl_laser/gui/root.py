from __future__ import annotations

from PyQt5.QtWidgets import QMainWindow
import qtawesome as qta

from .py_ui import Ui_root


__all__ = ["WinRoot"]


class UiRoot(Ui_root):

    def __init__(self, root: WinRoot):
        self.setupUi(root)
        self.parent = root

        self._setup_parent()
        self._setup_ui()

    def port_opened(self, opened: bool) -> None:
        if opened:
            self.connect.setIcon(
                qta.icon("mdi.lan-connect", options=[{'color': "#11aa11"}])
            )
        else:
            self.connect.setIcon(
                qta.icon("mdi.lan-disconnect", options=[{'color': "#aa1111"}])
            )

    def _setup_parent(self) -> None:
        self.parent.setFixedSize(360, 240)

    def _setup_ui(self) -> None:
        self.port_opened(False)

        for wid in (
            self.write_regime, self.write_pulse_period, self.write_pulse_width
        ):
            wid.setIcon(qta.icon("ri.upload-2-fill"))

        for wid in (
            self.read_regime, self.read_pulse_period, self.read_pulse_width
        ):
            wid.setIcon(qta.icon("ri.download-2-fill"))


class WinRoot(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UiRoot(self)
