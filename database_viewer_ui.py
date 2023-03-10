import sqlite3
import time
import PySide6.QtWidgets as QW
from PySide6.QtCore import QMetaObject, Qt, Slot
import db_utils as db


class database_viewer(QW.QMainWindow):
    def __init__(self, DB_NAME, TABLE_NAMES) -> None:
        super().__init__()
        self.resize(1280, 720)
        ENTRY_TABLE = TABLE_NAMES[0]

        try:
            db_connection = sqlite3.connect(DB_NAME)
            db_cursor = db_connection.cursor()
            self.tagged_entries: dict[int, dict[str, str]
                                      ] = db.get_tagged_dict(db_cursor, ENTRY_TABLE)
            self.button_strings: list[str] = db.get_button_data(
                db_cursor, ENTRY_TABLE)
            db.shutdown_database(db_connection)
        except sqlite3.Error as db_connect_error:
            print(f'A gui database error has occurred: {db_connect_error}')

        # setup main conatiner widget
        self.outer_widget = QW.QWidget()
        self.outer_layout = QW.QHBoxLayout()

        # setup left widget that will hold buttons
        self.scroll_area = QW.QScrollArea()
        self.scroll_area.setFrameShape(QW.QFrame.Shape.NoFrame)
        self.left_widget = QW.QWidget()
        self.left_layout = QW.QVBoxLayout()
        self.scroll_layout = QW.QVBoxLayout()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)

        for string in self.button_strings:
            self._add_button(string)

        # finalize left widget and layout
        self.left_widget.setLayout(self.left_layout)
        self.scroll_area.setWidget(self.left_widget)
        self.scroll_layout.addWidget(self.scroll_area)

        # setup right widget that will house the entry information
        self.right_widget = QW.QWidget()
        self.right_layout = QW.QGridLayout()
        self.right_container = QW.QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_layout.setVerticalSpacing(15)

        # finalize right widget and layout
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setEnabled(False)
        self.right_container.addWidget(self.right_widget)

        self.claim_button = QW.QPushButton(text="Claim Project")
        self.right_container.addWidget(self.claim_button)

        # finalize outer widget and layout
        self.outer_layout.addLayout(self.scroll_layout)
        self.outer_layout.addLayout(self.right_container)
        self.outer_widget.setLayout(self.outer_layout)

        self.claim_button.clicked.connect(self.claim_click_handler)
        # tell the app to use outer_widget as the main widget
        self.setCentralWidget(self.outer_widget)
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def _click_handler(self) -> None:
        """handle button clicks on left layout"""
        self.left_widget.setEnabled(False)
        time.sleep(.1)

        button = self.sender()
        button_string = button.objectName()

        char_counter = 0
        for char in button_string:
            if char == '.':
                break
            char_counter += 1
        id_number: int = int(button_string[:char_counter])

        self.show_entry_data(id_number)

    @Slot()
    def claim_click_handler(self):
        # claim logic here
        pass

    def _add_button(self, string: str) -> None:
        """Add buttons to the left layout list based on database entries"""
        # code help from https://stackoverflow.com/questions/60250842/how-to-create-dynamic-buttons-in-pyqt5 (buttons)
        push_button = QW.QPushButton(string)
        push_button.setObjectName(string)
        self.left_layout.addWidget(push_button)
        push_button.clicked.connect(self._click_handler)

    def show_entry_data(self, id: int) -> None:
        """click handler calls this to populate the data fields in right_layout"""
        display__instance: dict[int, dict[str, str]] = {
            k: v for k, v in self.tagged_entries.items()}

        # clear layout so we aren't stacking on top of old data
        while self.right_layout.count():
            child = self.right_layout.takeAt(0)
            if child.widget() is not None:
                self.right_layout.removeWidget(child.widget())
                child.widget().deleteLater()
            else:
                self.right_layout.removeItem(child)

        display__instance = self._first_rows(
            display__instance, id, 1, 'Organization Name')

        self.right_layout.addItem(QW.QSpacerItem(0, 30), 3, 0, 1, 8)

        display__instance = self._first_rows(
            display__instance, id, 4, 'Course Project')

        self.right_layout.addItem(QW.QSpacerItem(0, 30), 7, 0, 1, 8)

        display__instance = self._check_boxes(
            display__instance, id, 0, 'Summer 2022')

        display__instance = self._check_boxes(
            display__instance, id, 4, 'Do we have your permission to use your organization\'s name?')

        self.right_layout.addItem(QW.QSpacerItem(0, 30), 16, 0, 1, 8)

        # handle the final data point
        for label, info in display__instance[id].items():
            self.right_layout.addWidget(QW.QLabel(label), 17, 0, 1, 4)
            self.right_layout.addWidget(QW.QLineEdit(info), 17, 4, 1, 4)

        time.sleep(.1)
        self.left_widget.setEnabled(True)

    def _first_rows(self, display__instance: dict[int, dict[str, str]], id: int,
                    row: int, stop_on: str) -> dict[int, dict[str, str]]:
        """handle the personal information placement"""
        col_counter = -1
        removal_list = []
        for label, info in display__instance[id].items():
            if label == stop_on:
                break
            removal_list.append(label)
            col_counter += 1
            self.right_layout.addWidget(
                QW.QLabel(' ' + label), row + 1, col_counter)
            col_counter += 1
            self.right_layout.addWidget(
                QW.QLineEdit(info), row, col_counter - 1)

        display__instance[id] = {key:  val for key, val
                                 in display__instance[id].items() if key not in removal_list}
        return display__instance

    def _check_boxes(self, display__instance: dict[int, dict[str, str]], id: int,
                     col: int, stop_on: str) -> dict[int, dict[str, str]]:
        """handle the check box placement"""
        row_counter = 8
        removal_list = []
        if col == 0:
            self.right_layout.addWidget(
                QW.QLabel(text='Collaborative Opportunities:'), row_counter, col)
        elif col == 4:
            self.right_layout.addWidget(
                QW.QLabel(text='Time Frame:'), row_counter, col)
        row_counter += 1
        for label, info in display__instance[id].items():
            if label == stop_on:
                break
            removal_list.append(label)
            new_box = QW.QCheckBox(label)
            if info is not None:
                new_box.setChecked(True)
            self.right_layout.addWidget(new_box, row_counter, col)
            row_counter += 1

        display__instance[id] = {key:  val for key, val
                                 in display__instance[id].items() if key not in removal_list}
        return display__instance
