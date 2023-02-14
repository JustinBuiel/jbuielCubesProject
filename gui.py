import random
import sqlite3
import db_utils as db
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QPushButton, QScrollArea,
                               QVBoxLayout, QWidget, QMainWindow)

# got a lot of this code from https://www.pythonguis.com/tutorials/pyqt6-qscrollarea/

# test

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        db_connection = sqlite3.connect('form_entries.db')
        db_cursor = db_connection.cursor()

        # try to get list of data for short version of entries
        self.entries: list = db.get_minimal_data(db_cursor)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        for entry in self.entries:
            # object = QLabel(entry)
            # self.vbox.addWidget(object)
            self.vbox.addWidget(QPushButton(text=entry))

        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Scroll Area Demonstration')

    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
