from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QMessageBox
from main_window import Ui_MainWindow  # Import Ui_MainWindow

class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        self.main_window = MainWindow  # Store the reference to the login window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(100, 20, 200, 40))
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")

        # Username input
        self.label_username = QtWidgets.QLabel(self.centralwidget)
        self.label_username.setGeometry(QtCore.QRect(50, 80, 100, 20))
        self.label_username.setObjectName("label_username")
        self.lineEdit_username = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_username.setGeometry(QtCore.QRect(150, 80, 200, 20))
        self.lineEdit_username.setObjectName("lineEdit_username")

        # Password input
        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setGeometry(QtCore.QRect(50, 120, 100, 20))
        self.label_password.setObjectName("label_password")
        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(150, 120, 200, 20))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")

        # Login button
        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(150, 180, 100, 30))
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.clicked.connect(self.login_user)

        # Back button
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(10, 10, 75, 30))
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_back.clicked.connect(self.go_back)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # SQLite Database Connection
        self.conn = sqlite3.connect('user_management.db')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login Page"))
        self.label_title.setText(_translate("MainWindow", "User Login"))
        self.label_username.setText(_translate("MainWindow", "Username"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.pushButton_login.setText(_translate("PushButton", "Login"))
        self.pushButton_back.setText(_translate("PushButton", "Back"))

    def login_user(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if not username or not password:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Both fields are required!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND verified=1", (username, password))
        user = cursor.fetchone()

        if user:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Login Successful!")
            msg.setWindowTitle("Success")
            msg.exec_()

            # Create and show the main window
            self.main_window.hide()  # Hide the login window
            from WelcomePage import Ui_WelcomeWindow  # Import Ui_WelcomeWindow

            self.main_window = QtWidgets.QMainWindow()
            self.ui_main = Ui_MainWindow()
            self.ui_main.setupUi(self.main_window)
            self.main_window.show()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid username or password, or user not verified!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def go_back(self):
        from WelcomePage import Ui_WelcomeWindow  # Import Ui_WelcomeWindow

        self.main_window.close()  # Close the login window
        self.welcome_window = QtWidgets.QMainWindow()
        self.ui_welcome = Ui_WelcomeWindow()
        self.ui_welcome.setupUi(self.welcome_window)
        self.welcome_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
