from __future__ import annotations

from PyQt5.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QDialog,
)

import backend.pc_polynomial
from backend import pc_polynomial
from ui.utils import AThread


class PolynomialShowWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.polynomial = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Polynomial")
        self.setGeometry(300, 300, 300, 200)
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 280, 100)
        self.button_calculate = QPushButton("Вычислить", self)
        self.button_calculate.move(20, 120)
        self.button_calculate.clicked.connect(self.calculate)

        self.button_save = QPushButton("Сохранить", self)
        self.button_save.move(120, 120)
        self.button_save.clicked.connect(self.save)
        self.show()

    def resizeEvent(self, event):
        h, w = self.height(), self.width()
        self.text_edit.setGeometry(10, 10, w - 20, 100)

    def calculate(self):
        n, m, g = self.parent().get_graph()
        self.text_edit.setText("Идёт вычисление...")
        thread = AThread(self, pc_polynomial.build, n, m, g)
        thread.finished.connect(lambda: self.after_calculate(thread))
        thread.start()

    def after_calculate(self, thread: AThread):
        if thread.ok:
            self.polynomial = thread.result
            self.show_polynomial()
        else:
            self.show_error()

    def show_polynomial(self):
        poly_string = backend.pc_polynomial.prepare_for_showing(self.polynomial)
        self.text_edit.setText(poly_string)

    def show_error(self):
        self.text_edit.setText("Ошибка")

    def save(self):
        if not self.polynomial:
            return
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setNameFilter("Graph files (*.poly);;All files (*)")
        dialog.setDefaultSuffix("poly")
        if dialog.exec_() == QDialog.Accepted:
            with open(dialog.selectedFiles()[0], "w") as file:
                file.write(
                    backend.pc_polynomial.prepare_for_saving(self.polynomial)
                )
