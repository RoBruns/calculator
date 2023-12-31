import math
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isNumOrDot, isValidNumber
from variables_and_styles import MEDIUM_FONT_SIZE

if TYPE_CHECKING:
    from display import Display, Info
    from main_window import MainWindow


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
    def __init__(self, display: 'Display', info: 'Info',  app,
                 window: 'MainWindow', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridmask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self.app = app
        self._equation = ''
        self.equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None
        self.equation = self.equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    @Slot()
    def _insertKeyTextToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)

    @Slot()
    def _operatorKeyClicked(self, text):
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Digite um número antes de usar um operador')
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ???'

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.deletePressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertKeyTextToDisplay)
        self.display.opratorPressed.connect(self._operatorKeyClicked)

        for rowNumber, rowData in enumerate(self._gridmask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button, self.app)

                self.addWidget(button, rowNumber, colNumber)
                slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button, app):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

        if text in '/*-+^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._operatorClicked, button)
                )

        if text == '◀':
            self._connectButtonClicked(button, self.display.backspace)

        if text == '=':
            self._connectButtonClicked(button, self._eq)

    @Slot(bool)
    def _makeSlot(self, func, *args, **kwargs):
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        newNumber = float(displayText) * -1

        if newNumber.is_integer():
            newNumber = int(newNumber)

        self.display.setText(str(newNumber))

    @Slot()
    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self.equationInitialValue
        self.display.clear()
        self.display.setFocus()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Digite um número antes de usar um operador')
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op} ???'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError('Você não digitou o segundo numero')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Não é possível dividir por zero')
        except OverflowError:
            self._showError('O resultado é muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setWindowTitle("Error")
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInnfo(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setWindowTitle("Info")
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()