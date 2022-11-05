import sys
import logging.config

from PyQt5.Qt import QApplication

from pyinstr_iakoster.log import get_logging_dict_config

from ctrl_laser import WinRoot


def _except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


logging.config.dictConfig(get_logging_dict_config(
    info_rotating_file_handler=False,
    error_file_handler=False,
))
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    sys.excepthook = _except_hook
    app = QApplication(sys.argv)
    root = WinRoot()
    root.show()
    sys.exit(app.exec_())


