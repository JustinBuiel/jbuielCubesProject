from PySide6.QtCore import Qt, Slot, QMetaObject
import PySide6.QtWidgets as QtWidgets
import sqlite3
import db_utils as db


class list_of_btns(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        QtWidgets.QWidget.__init__(self)
        MainWindow.resize(1280, 720)

        # set up the widgets and layouts we will need
        self.scrollArea = QtWidgets.QScrollArea()
        self.collectWidget = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout()

        try:
            db_connection = sqlite3.connect('form_entries.db')
            db_cursor = db_connection.cursor()
        except sqlite3.Error as db_connect_error:
            print(f'A gui database error has occurred: {db_connect_error}')

        # try to get list of data for short version of entries
        self.entries: list = db.get_minimal_data(db_cursor)
        for entry in self.entries:
            self.addListItem(entry)

        # "commit" the changes
        self.collectWidget.setLayout(self.verticalLayout)

        # set the scroll area settings and bind it to "central widget"
        self.scrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.collectWidget)
        MainWindow.setCentralWidget(self.scrollArea)

        QMetaObject.connectSlotsByName(MainWindow)

    def addListItem(self, entry):
        """Add buttons to the main page list based on database entries"""
        # code help from https://stackoverflow.com/questions/60250842/how-to-create-dynamic-buttons-in-pyqt5 (buttons)
        pushButton = QtWidgets.QPushButton(
            parent=self, text=entry)
        pushButton.setObjectName(entry)
        self.verticalLayout.addWidget(pushButton)

        pushButton.clicked.connect(self.click_handler)

    @ Slot()
    def click_handler(self):
        """Handle button clicks on main page"""
        MainWindow = QtWidgets.QMainWindow()
        button = self.sender()
        print(button.objectName())
        self.info = entry_info(MainWindow, id=button.objectName()[0])
        self.info.show()


class entry_info(QtWidgets.QWidget):
    def __init__(self, MainWindow, id):
        QtWidgets.QWidget.__init__(self)
        MainWindow.resize(1280, 720)

        # add a button to hide the window for now
        self.button = QtWidgets.QPushButton(text='Back ' + str(id))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.go_back)

        # todo: add all info about the correct entry based on id passed in

    @Slot()
    def go_back(self):
        # just hides window
        self.hide()
