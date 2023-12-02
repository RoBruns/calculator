from PySide6.QtWidgets import QPushButton, QGridLayout
from variables_and_styles import MEDIUM_FONT_SIZE
from utils import isNumOrDot


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridmask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['CLOSE',  '0', '.', '='],
        ]
        self._makeGrid()

    def _makeGrid(self):
        for rowNumber, rowData in enumerate(self._gridmask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText):
                    button.setProperty('cssClass', 'specialButton')

                self.addWidget(button, rowNumber, colNumber)
