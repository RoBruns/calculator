import sys

import fix_icon_win
from buttons import ButtonsGrid
from display import Display, Info
from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables_and_styles import WINDOW_ICON_PATH, setupTheme

# Corrige o icone da janela no Windows
fix_icon_win.fix_icon_win()

if __name__ == "__main__":
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Define o icone da janela
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info conta
    info = Info('Sua conta')
    window.addWidgetToVlayout(info)

    # Display
    display = Display('')
    window.addWidgetToVlayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info, app)
    window.vLayout.addLayout(buttonsGrid)

    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
