import sqlite3
# import time
import PySide6.QtWidgets as QW
from PySide6.QtCore import Slot, QMetaObject
import db_utils as db


class claim_window(QW.QMainWindow):
    def __init__(self, id, DB_NAME, TABLE_NAMES):
        super().__init__()
        self.DB_NAME = DB_NAME
        self.ENTRY_TABLE, self.USER_TABLE, self.CLAIM_TABLE = TABLE_NAMES
        self.resize(1280, 720)
        self.id = id

        self.central_widget = QW.QWidget()
        self.central_layout = QW.QVBoxLayout()
        self.outer_layout = QW.QHBoxLayout()
        self.labels = QW.QVBoxLayout()
        self.text_boxes = QW.QVBoxLayout()

        self.check_button = QW.QPushButton(text="Submit")
        self.initial_screen()

        self.outer_layout.addLayout(self.labels)
        self.outer_layout.addLayout(self.text_boxes)
        self.central_layout.addLayout(self.outer_layout)
        self.central_layout.addWidget(self.check_button)
        self.central_widget.setLayout(self.central_layout)

        self.setCentralWidget(self.central_widget)
        QMetaObject.connectSlotsByName(self)

        self.check_button.clicked.connect(self.check_for_user)

    @Slot()
    def check_for_user(self):
        self.exists = False
        user = self.email.text()
        response = None
        try:
            db_connection = sqlite3.connect(self.DB_NAME)
            db_cursor = db_connection.cursor()
            db_cursor.execute(f'''SELECT email FROM {self.USER_TABLE}''')
            results = db_cursor.fetchall()

            for row in results:
                if user == row[0]:
                    self.exists = True
                    db_cursor.execute(
                        f'''SELECT * FROM {self.USER_TABLE} WHERE email like \'{user}\' ''')
                    response: list = db_cursor.fetchall()
                    response: tuple = response[0]

            db.shutdown_database(db_connection)
        except sqlite3.Error as db_connect_error:
            print(
                f'A claim window gui database error has occurred: {db_connect_error}')

        user_data = None
        if self.exists:
            user_data = response[1:]

        self.full_info(user_data)

    @Slot()
    def claim_handler(self):
        user_info = []

        user_info.append(self.first_name.text())
        user_info.append(self.last_name.text())
        user_info.append(self.title.text())
        user_info.append(self.email.text())
        user_info.append(self.dept.text())

        if not self.exists:
            db.create_user(self.DB_NAME, self.USER_TABLE, tuple(user_info))

        try:
            db_connection = sqlite3.connect(self.DB_NAME)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                f'''SELECT userID FROM {self.USER_TABLE} WHERE email like \'{self.email.text()}\' ''')
            response = db_cursor.fetchall()

            user_id = response[0][0]
        except sqlite3.Error as user_id_error:
            print(f"Error while getting userID: {user_id_error}")

        db.claim_project(self.DB_NAME, self.CLAIM_TABLE, user_id, self.id)
        self.close()

    def initial_screen(self):
        self.labels.addWidget(QW.QLabel(text="Email"))
        self.email = QW.QLineEdit()
        self.text_boxes.addWidget(self.email)

    def full_info(self, user_data: list):

        self.clear_layout()

        self.labels.addWidget(QW.QLabel(text="First Name"))
        self.first_name = QW.QLineEdit()
        self.text_boxes.addWidget(self.first_name)
        self.labels.addWidget(QW.QLabel(text="Last Name"))
        self.last_name = QW.QLineEdit()
        self.text_boxes.addWidget(self.last_name)
        self.labels.addWidget(QW.QLabel(text="Title"))
        self.title = QW.QLineEdit()
        self.text_boxes.addWidget(self.title)
        self.labels.addWidget(QW.QLabel(text="Email"))
        self.email = QW.QLineEdit()
        self.text_boxes.addWidget(self.email)
        self.labels.addWidget(QW.QLabel(text="Department"))
        self.dept = QW.QLineEdit()
        self.text_boxes.addWidget(self.dept)

        if user_data is not None:
            print("there")
            self.first_name.setText(user_data[0])
            self.last_name.setText(user_data[1])
            self.title.setText(user_data[2])
            self.email.setText(user_data[3])
            self.dept.setText(user_data[4])

        claim_button = QW.QPushButton(text="Claim Project")
        self.central_layout.addWidget(claim_button)

        claim_button.clicked.connect(self.claim_handler)

    def clear_layout(self) -> None:
        child = self.labels.takeAt(0)
        self.labels.removeWidget(child.widget())
        child.widget().deleteLater()

        child = self.text_boxes.takeAt(0)
        self.text_boxes.removeWidget(child.widget())
        child.widget().deleteLater()

        child = self.central_layout.takeAt(1)
        self.central_layout.removeWidget(child.widget())
        child.widget().deleteLater()
