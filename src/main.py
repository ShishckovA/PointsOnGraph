import sys

from PyQt5.QtWidgets import QApplication

from ui.windows import Window

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
