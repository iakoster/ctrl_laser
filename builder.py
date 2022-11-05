"""
Скрипт-сборщик проекта в исполняемый файл exe.
"""
import os
import shutil
import PyInstaller.__main__
from pathlib import Path

from ctrl_laser import __version__


ONE_FILE = True
NAME = "ctrl laser"


def get_files(path: Path) -> list[Path]:
    paths = []
    for sub in path.iterdir():
        if sub.is_dir():
            paths += get_files(sub)
        else:
            paths.append(sub)
    return paths


full_name = f"{NAME} {__version__}"
proj_dir = os.getcwd()
bundl_dir = r'{}\bundl'.format(proj_dir)
build_dir = r'{}\build'.format(bundl_dir)
dist_dir = r'{}\dist'.format(bundl_dir)
prog_dir = r'{}\{}'.format(dist_dir, full_name)

input_str = None
while input_str not in ["y", "n"]:

    print(f"\nТЕКУЩИЕ НАСТРОЙКИ\nИмя программы: {NAME}\nВерсия программы: {__version__}")
    input_str = input("Версия программы указано верно? (y/n)\n").lower()

    if input_str not in ["y", "n"]:
        print("Неверный ответ")
    elif input_str in ["n"]:
        raise KeyboardInterrupt()


print(f"\n\nПолное имя программы: {full_name}\n")
print(f"Директория программы:\n{prog_dir}\n")
input("Нажмите Enter для продолжения\n")

print('Очистка папки сборки')
if os.path.exists(bundl_dir):
    shutil.rmtree(bundl_dir)

if os.path.exists(dist_dir) and os.listdir(dist_dir):
    print("Директория сборки программы не пустая\nУдаление содержимого...\n")
    shutil.rmtree(dist_dir)

PyInstaller.__main__.run([
    r"{}\main.py".format(proj_dir),
    "--workpath", build_dir,
    "--specpath", bundl_dir,
    "--distpath", dist_dir,
    "--name", full_name,
    "--console",
    "-F" if ONE_FILE else "-D",
])  # todo: make via Analysis, PYZ, EXE, COLLECT (pyinstaller.org/en/stable/spec-files.html)


# for src in get_files(Path("data")):
#     dst = Path(prog_dir) / src
#     if not dst.parent.exists():
#         dst.parent.mkdir(parents=True)
#     shutil.copyfile(src, dst)
#     print("copy data", src.absolute(), "->", dst)


if not ONE_FILE:
    shutil.make_archive(prog_dir, "zip", proj_dir)
    print("Создан .zip архив директории %s" % prog_dir)

input("Нажмите Enter для выхода\n")
