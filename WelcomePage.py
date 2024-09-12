from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from registrationPage import Ui_RegistrationWindow  # Import the Registration page
from loginPage import Ui_LoginWindow  # Import the Login page

class Ui_WelcomeWindow(object):
    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(100, 20, 200, 40))
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")

        # Register button
        self.pushButton_register = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_register.setGeometry(QtCore.QRect(100, 100, 200, 30))
        self.pushButton_register.setObjectName("pushButton_register")
        self.pushButton_register.clicked.connect(self.open_registration)

        # Login button
        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(100, 150, 200, 30))
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.clicked.connect(self.open_login)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome Page"))
        self.label_title.setText(_translate("MainWindow", "Welcome"))
        self.pushButton_register.setText(_translate("MainWindow", "Register"))
        self.pushButton_login.setText(_translate("MainWindow", "Login"))

    def open_registration(self):
        self.main_window.hide()
        self.registration_window = QtWidgets.QMainWindow()
        self.ui_registration = Ui_RegistrationWindow()
        self.ui_registration.setupUi(self.registration_window)
        self.registration_window.show()

    def open_login(self):
        self.main_window.hide()
        self.login_window = QtWidgets.QMainWindow()
        self.ui_login = Ui_LoginWindow()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_WelcomeWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
