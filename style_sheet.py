import PySide6.QtWidgets as QW
from PySide6.QtGui import QColor, QFont, QPalette

BACKGROUND = QColor(30, 27, 24)
TEXT = QColor(255, 255, 255)
ACCENT = QColor(20, 20, 125)


def set(app: QW.QApplication):
    app_palette = app.palette()
    font = QFont()
    font.setFamilies("Inter")
    font.setPointSize(11)
    app.setFont(font)
    app_palette.setColor(QPalette.ColorRole.Window, BACKGROUND)
    app_palette.setColor(QPalette.ColorRole.Base, ACCENT)
    app_palette.setColor(QPalette.ColorRole.Button, ACCENT)
    app_palette.setColor(QPalette.ColorRole.WindowText, TEXT)
    app_palette.setColor(QPalette.ColorRole.Text, TEXT)
    app_palette.setColor(QPalette.ColorRole.ButtonText, TEXT)

    app.setPalette(app_palette)
    app.setStyle('Fusion')
