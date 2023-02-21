from PySide6.QtGui import QPalette, QColor, QFont
import PySide6.QtWidgets as QW

BLACK = QColor(30, 27, 24)
WHITE = QColor(255, 255, 255)
BLUE = QColor(20, 20, 125)


def set(app: QW.QApplication):
    app_palette = app.palette()
    font = QFont()
    font.setFamilies("Inter")
    font.setPointSize(11)
    app.setFont(font)
    app_palette.setColor(QPalette.ColorRole.Window, BLACK)
    app_palette.setColor(QPalette.ColorRole.Base, BLUE)
    app_palette.setColor(QPalette.ColorRole.Button, BLUE)
    app_palette.setColor(QPalette.ColorRole.WindowText, WHITE)
    app_palette.setColor(QPalette.ColorRole.Text, WHITE)
    app_palette.setColor(QPalette.ColorRole.ButtonText, WHITE)

    app.setPalette(app_palette)
    app.setStyle('Fusion')
