import sys
import fix_icon_win

from buttons import Button
from display import Display, Info
from main_window import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
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
    info = Info('2.0 ^ 10.0 = 1024')
    window.addToVlayout(info)

    # Display
    display = Display('0')
    window.addToVlayout(display)

    # Botoes
    button = Button('Texto do botão')
    window.addToVlayout(button)
        
    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
