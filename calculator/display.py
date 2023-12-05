from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLabel, QLineEdit, QWidget
from utils import isEmpty, isNumOrDot
from variables_and_styles import (BIG_FONT_SIZE, MINIMUN_WIDTH,
                                  SMALL_FONT_SIZE, TEXT_MARGIN)


class Display(QLineEdit):
    eqPressed = Signal()
    deletePressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    opratorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    # Configura o estilo do display
    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f"font-size: {BIG_FONT_SIZE}px;")
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUN_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isOpertor = text in ['+', '-', '*', '/']

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()

        if isDelete:
            self.deletePressed.emit()
            return event.ignore()

        if isEsc:
            self.clearPressed.emit()
            return event.ignore()

        if isOpertor:
            self.opratorPressed.emit(text)
            return event.ignore()
        # Não passa o evento se o texto for vazio
        if isEmpty(text):
            return event.ignore()

        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f"font-size: {SMALL_FONT_SIZE}px;")
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
