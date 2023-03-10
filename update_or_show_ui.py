import PySide6.QtWidgets as QW
from PySide6.QtCore import Slot, QMetaObject
from database_viewer_ui import database_viewer
from gather_data import update_data, DB_NAME, TABLE_NAMES

ENTRY_TABLE, USER_TABLE, CLAIM_TABLE = TABLE_NAMES


class update_or_show(QW.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.main = QW.QWidget()
        choice = QW.QVBoxLayout()
        update = QW.QPushButton(text="Update Data")
        show = QW.QPushButton(text="Visualize Data")
        choice.addWidget(update)
        choice.addWidget(show)

        self.main.setLayout(choice)

        self.setCentralWidget(self.main)
        QMetaObject.connectSlotsByName(self)

        update.clicked.connect(self.update_click_handler)
        show.clicked.connect(self.show_click_handler)

    @Slot()
    def update_click_handler(self):
        update_data()
        self.data_viewer = database_viewer(DB_NAME, TABLE_NAMES)
        self.data_viewer.show()
        self.close()

    @Slot()
    def show_click_handler(self):
        self.data_viewer = database_viewer(DB_NAME, TABLE_NAMES)
        self.data_viewer.show()
        self.close()
