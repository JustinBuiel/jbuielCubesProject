"""
This is the main driver module that handles the interactions between the other modules
"""

import PySide6.QtWidgets as QW
from style_sheet import set
from update_or_show_ui import update_or_show

if __name__ == "__main__":
    app = QW.QApplication([])
    set(app)

    ui = update_or_show()
    ui.show()
    print('Running UI')

    app.exec()
