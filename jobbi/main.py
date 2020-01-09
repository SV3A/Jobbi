#!/bin/python3
import sys
import view
from pathlib import Path
from controller import Controller

__version__ = "0.2"
__author__ = "Svend Andersen"

img_path = Path("./img/")


def main():
    app = view.initApp()
    window = view.JobbiUI()
    window.show()
    controller = Controller(view=window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
