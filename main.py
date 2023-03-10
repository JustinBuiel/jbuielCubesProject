"""
This is the main driver module that handles the interactions between the other modules
"""

import PySide6.QtWidgets as QW
from update_or_show_ui import update_or_show
from style_sheet import set
# from gather_data import DB_NAME, TABLE_NAME

if __name__ == "__main__":
    app = QW.QApplication([])
    set(app)

    ui = update_or_show()
    ui.show()
    print('Running UI')

    app.exec()
