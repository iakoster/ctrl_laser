import io
from pathlib import Path

from PyQt5 import uic

QT_UI_DIR = Path().absolute()
PY_UI_DIR = QT_UI_DIR.parent / "ctrl_laser/gui/py_ui"


def check_py_ui_dir() -> bool:
    py_ui_dir_exists = PY_UI_DIR.exists()
    if not py_ui_dir_exists:
        PY_UI_DIR.mkdir(parents=True)
    return py_ui_dir_exists


def clear_py_ui():
    py_ui_files = list(PY_UI_DIR.iterdir())
    deleted_files = 0
    for py_ui in py_ui_files:
        if py_ui.is_file() and py_ui.name != '__init__.py':
            py_ui.unlink()
            deleted_files += 1
    print(f'Deleted {deleted_files} files')


def convert_qt_ui():
    ui_files = list(QT_UI_DIR.iterdir())
    created_files = 0
    for ui_file in ui_files:
        if ui_file.match('*.ui'):
            py_path = PY_UI_DIR / ui_file.with_suffix('.py').name
            with io.open(py_path, 'w', encoding='utf-8') as py_file:
                uic.compileUi(str(ui_file), py_file)
            created_files += 1
    print(f'Created {created_files} files')


if __name__ == '__main__':
    print(f'Qt .ui files directory:\n{QT_UI_DIR}')
    print(f'Qt .py files directory:\n{PY_UI_DIR}\n')
    if check_py_ui_dir():
        clear_py_ui()
    convert_qt_ui()
