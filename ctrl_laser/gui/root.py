from __future__ import annotations

from PyQt5.QtWidgets import QMainWindow

from .py_ui import Ui_root


__all__ = ["WinRoot"]


class UiRoot(Ui_root):

    def __init__(self, root: WinRoot):
        self.setupUi(root)


class WinRoot(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UiRoot(self)
