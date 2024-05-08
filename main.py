import sys
from PyQt5.QtWidgets import QApplication
import App_GUI as ap
import tkinter as tk


if __name__ == "__main__":

    FW = 'pyqt' # pyqt / tk

    if FW  == 'tk':
        control_app = ap.ControlWindow(tk.Tk())

    if FW == 'pyqt':
        app = QApplication(sys.argv)
        main_window = ap.MainWindow()
        main_window.show()
        sys.exit(app.exec_())
