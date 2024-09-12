import random
import string
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'koukinourhen03@gmail.com'
EMAIL_PASSWORD = 'qzsk bgmn enms cdbu'
RECIPIENT_EMAIL = 'nourhenekouki016@gmail.com'

# Temporary storage for verification codes
verification_codes = {}

def send_verification_email(email, code):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = 'Registration Confirmation Code'

            body = f"Your registration confirmation code is: {code}"
            msg.attach(MIMEText(body, 'plain'))

            server.send_message(msg)
            print("Verification email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class Ui_RegistrationWindow(object):
    def setupUi(self, MainWindow):
        
        self.MainWindow = MainWindow  # Store MainWindow as an instance attribute
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

        # Email input
        self.label_email = QtWidgets.QLabel(self.centralwidget)
        self.label_email.setGeometry(QtCore.QRect(50, 160, 100, 20))
        self.label_email.setObjectName("label_email")
        self.lineEdit_email = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_email.setGeometry(QtCore.QRect(150, 160, 200, 20))
        self.lineEdit_email.setObjectName("lineEdit_email")

        # Register button
        self.pushButton_register = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_register.setGeometry(QtCore.QRect(150, 220, 100, 30))
        self.pushButton_register.setObjectName("pushButton_register")
        self.pushButton_register.clicked.connect(self.register_user)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

         # Back button
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(10, 10, 75, 30))
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_back.setText("Back")
        self.pushButton_back.clicked.connect(self.go_back)

        # SQLite Database Connection
        self.conn = sqlite3.connect('user_management.db')
        self.create_table()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Registration Page"))
        self.label_title.setText(_translate("MainWindow", "User Registration"))
        self.label_username.setText(_translate("MainWindow", "Username"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.label_email.setText(_translate("MainWindow", "Email"))
        self.pushButton_register.setText(_translate("MainWindow", "Register"))

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT NOT NULL,
                            verified INTEGER DEFAULT 0)''')
        self.conn.commit()

    def register_user(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        email = self.lineEdit_email.text()

        if not username or not password or not email:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("All fields are required!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        code = generate_random_code()
        verification_codes[email] = code
        send_verification_email(email, code)

        self.verification_window = QtWidgets.QMainWindow()
        self.ui_verification = Ui_CodeVerificationWindow(username, password, email, code)
        self.ui_verification.setupUi(self.verification_window)
        self.verification_window.show()
    
    def go_back(self):
        self.MainWindow.close()  # Close the verification window

        # Create and show the registration window
        from WelcomePage import Ui_WelcomeWindow  # Import Ui_WelcomeWindow

         # Close the login window
        self.welcome_window = QtWidgets.QMainWindow()
        self.ui_welcome = Ui_WelcomeWindow()
        self.ui_welcome.setupUi(self.welcome_window)
        self.welcome_window.show()


class Ui_CodeVerificationWindow(QtWidgets.QMainWindow):
    def __init__(self, username, password, email, code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.email = email
        self.code = code
        self.conn = sqlite3.connect('user_management.db')

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(100, 20, 200, 40))
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")

        # Code input
        self.label_code = QtWidgets.QLabel(self.centralwidget)
        self.label_code.setGeometry(QtCore.QRect(50, 80, 100, 20))
        self.label_code.setObjectName("label_code")
        self.lineEdit_code = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_code.setGeometry(QtCore.QRect(150, 80, 200, 20))
        self.lineEdit_code.setObjectName("lineEdit_code")

        # Verify button
        self.pushButton_verify = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_verify.setGeometry(QtCore.QRect(150, 120, 100, 30))
        self.pushButton_verify.setObjectName("pushButton_verify")
        self.pushButton_verify.clicked.connect(self.verify_code)

        

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Verification Page"))
        self.label_title.setText(_translate("MainWindow", "Enter Verification Code"))
        self.label_code.setText(_translate("MainWindow", "Code"))
        self.pushButton_verify.setText(_translate("MainWindow", "Verify"))

    def verify_code(self):
        entered_code = self.lineEdit_code.text()

        if entered_code != self.code:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid verification code!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email, verified) VALUES (?, ?, ?, 1)",
                       (self.username, self.password, self.email))
        self.conn.commit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Registration Successful!")
        msg.setWindowTitle("Success")
        msg.exec_()

        self.window().close()  # Close the verification window



    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_RegistrationWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
