#!/bin/python3
import sys
import view
from controller import Controller

__version__ = "0.1"
__author__ = "Svend Andersen"


def main():
    app = view.initApp()
    window = view.getJobUI()
    window.show()
    controller = Controller(view=window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
