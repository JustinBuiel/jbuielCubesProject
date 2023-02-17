from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


def set(app_palette):

    app_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    app_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app_palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    app_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    app_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    app_palette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
    app_palette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    app_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    app_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    app_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    app_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    app_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    app_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    app_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    app_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    app_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    app_palette.setColor(QPalette.ColorRole.HighlightedText,
                         QColor(127, 127, 127))
