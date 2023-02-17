import sqlite3
import PySide6.QtWidgets as QW
from PySide6.QtCore import QMetaObject, Qt, Slot
import db_utils as db


class database_viewer(QW.QWidget):
    def __init__(self, MainWindow):
        QW.QWidget.__init__(self)
        self.MainWindow = MainWindow
        self.MainWindow.resize(1280, 720)

        self.outerWidget = QW.QWidget()
        self.outerLayout = QW.QHBoxLayout()

        # set up the widgets and layouts we will need
        self.scrollArea = QW.QScrollArea()
        self.leftWidget = QW.QWidget()
        self.leftLayout = QW.QVBoxLayout()
        self.scrollLayout = QW.QVBoxLayout()
        self.scrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)

        self.rightWidget = QW.QWidget()
        self.rightLayout = QW.QGridLayout()
        self.rightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rightLayout.setVerticalSpacing(15)

        # set up the database connections and get the labelled dictionary
        try:
            db_connection = sqlite3.connect('form_entries.db')
            db_cursor = db_connection.cursor()
            self.entries_dict = db.get_entries_dict(db_cursor)
        except sqlite3.Error as db_connect_error:
            print(f'A gui database error has occurred: {db_connect_error}')

        # try to get list of data for short version of entries
        self.entries: list = db.get_minimal_data(db_cursor)
        for entry in self.entries:
            self.addListItem(entry)

        self.leftWidget.setLayout(self.leftLayout)
        self.scrollArea.setWidget(self.leftWidget)
        self.scrollLayout.addWidget(self.scrollArea)
        self.outerLayout.addLayout(self.scrollLayout)

        self.show_data(id=1, entries_dict=self.entries_dict)
        self.outerLayout.addLayout(self.rightLayout)

        self.outerWidget.setLayout(self.outerLayout)

        self.MainWindow.setCentralWidget(self.outerWidget)
        QMetaObject.connectSlotsByName(self.MainWindow)

    def addListItem(self, entry):
        """Add buttons to the main page list based on database entries"""
        # code help from https://stackoverflow.com/questions/60250842/how-to-create-dynamic-buttons-in-pyqt5 (buttons)
        pushButton = QW.QPushButton(
            parent=self, text=entry)
        pushButton.setObjectName(entry)
        self.leftLayout.addWidget(pushButton)

        pushButton.clicked.connect(self.click_handler)

    @Slot()
    def click_handler(self):
        """Handle button clicks on main page"""
        dict = self.entries_dict
        button = self.sender()
        number = button.objectName()
        print(button.objectName())
        count = 0
        for char in number:
            if char == '.':
                break
            count += 1
        number = number[:count]

        self.show_data(id=int(number), entries_dict=dict)

    def show_data(self, id, entries_dict):
        new_dict = {k: v for k, v in entries_dict.items()}
        new_dict = self.first_rows(
            new_dict, id, row=1, stop='Organization Name')
        new_dict = self.first_rows(new_dict, id, row=4, stop='Course Project')

        self.rightLayout.addItem(QW.QSpacerItem(0, 30), 3, 0, 1, 8)

        count = 0
        while True:
            try:
                self.widge = self.rightLayout.itemAt(count).widget()
                if type(self.widge) == QW.QLineEdit:
                    self.widge.setEnabled(False)
                count += 1
            except AttributeError:
                break

        self.rightLayout.addItem(QW.QSpacerItem(0, 30), 7, 0, 1, 8)
        new_dict = self.check_boxes(new_dict, id, col=0, stop='Summer 2022')
        new_dict = self.check_boxes(
            new_dict, id, col=4, stop='Org Name Permission')

        while True:
            try:
                self.widge = self.rightLayout.itemAt(count).widget()
                self.widge.setEnabled(False)
                count += 1
            except AttributeError:
                break

    def first_rows(self, new_dict, id, row, stop):
        count = -1
        remove_list = []
        for label, info in new_dict[id].items():
            if label == stop:
                break
            remove_list.append(label)
            count += 1
            self.rightLayout.addWidget(QW.QLabel(label), row + 1, count)
            if info is not None:
                count += 1
                self.rightLayout.addWidget(QW.QLineEdit(info), row, count - 1)
            else:
                count += 1
                self.rightLayout.addWidget(
                    QW.QLineEdit(''), row, count - 1)
        new_dict[id] = {
            key:  val for key, val in new_dict[id].items() if key not in remove_list}
        return new_dict

    def check_boxes(self, new_dict, id, col, stop):
        count = 8
        remove_list = []
        if col == 0:
            self.rightLayout.addWidget(
                QW.QLabel(text='Collaborative Opportunities:'), count, col)
        elif col == 4:
            self.rightLayout.addWidget(
                QW.QLabel(text='Time Frame:'), count, col)
        count += 1
        for label, info in new_dict[id].items():
            if label == stop:
                break
            remove_list.append(label)
            newBox = QW.QCheckBox(text=label)
            if info is not None:
                newBox.setChecked(True)
            self.rightLayout.addWidget(newBox, count, col)
            count += 1

        new_dict[id] = {
            key:  val for key, val in new_dict[id].items() if key not in remove_list}
        return new_dict
