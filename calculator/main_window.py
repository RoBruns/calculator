
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configurações da janela
        self.setWindowTitle("Calculadora")
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)

    # Ajusta o tamanho da janela para o tamanho do conteúdo
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # Adiciona um widget ao layout vertical
    def addToVlayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
