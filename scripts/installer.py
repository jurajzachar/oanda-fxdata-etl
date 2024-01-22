import PyInstaller.__main__
from pathlib import Path
NAME = "oanda-fxdata-etl"
HERE = Path(__file__).parent.absolute()
path_to_search = str(HERE / ".." / NAME)
path_to_main = path_to_search + "/main.py"


def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        '--name',
        'oanda-fxdata-etl',
        '--paths',
        path_to_search
    ])
