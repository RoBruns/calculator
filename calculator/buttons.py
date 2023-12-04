import math
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isNumOrDot, isValidNumber
from variables_and_styles import MEDIUM_FONT_SIZE

if TYPE_CHECKING:
    from display import Display, Info


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
    def __init__(self, display: 'Display', info: 'Info', app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridmask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['CLOSE',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
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

    def _makeGrid(self):
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

        if text == 'CLOSE':
            button.setProperty('cssClass', 'closeButton')
            button.clicked.connect(app.quit)
  
        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '/*-+^':
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._operatorClicked, button)
                )
        
        if text == '◀':
            self._connectButtonClicked(button, self.display.backspace)
            
        if text == '=':
            self._connectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self.equationInitialValue
        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op} ???'

    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
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
            print('ZeroDivisionError')
        except OverflowError:
            print('OverflowError')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        
        if result == 'error':
            self._left = None
