# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/nounou/surveillance_system/settings_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox
import os
import shutil
import subprocess
import sys  
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(460, 300, 281, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(100, 30, 591, 61))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(460, 190, 281, 81))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.widget = QtWidgets.QLabel(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(120, 190, 241, 191))
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.pushButton_2.clicked.connect(self.activate_script)
        self.pushButton_3.clicked.connect(self.add_person)
        self.pushButton_4.clicked.connect(self.delete_person)
        self.pushButton.clicked.connect(self.desactivate_script)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "activate"))
        self.pushButton.setText(_translate("MainWindow", "desactivate"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt; font-weight:600; text-decoration: underline; color:#a40000;\">Surveillance_System</span></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "add_person"))
        self.pushButton_4.setText(_translate("MainWindow", "delete_person"))

    def add_person(self):
        # Open a file dialog to select an image file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            # Specify the folder to save the selected image
            save_folder = "/home/nounou/surveillance_system/known_faces"
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            # Save the image to the specified folder
            base_name = os.path.basename(fileName)
            save_path = os.path.join(save_folder, base_name)
            shutil.copy(fileName, save_path)

            # Display the image in the widget
            pixmap = QtGui.QPixmap(save_path)
            pixmap = pixmap.scaled(self.widget.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.widget.setPixmap(pixmap)

            # Show success message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Image added successfully!")
            msg.setWindowTitle("Success")
            msg.exec_()  

    def delete_person(self):
        folder_path="/home/nounou/surveillance_system/known_faces"
        if not os.path.exists(folder_path):
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No images found to delete.")
            msg.setWindowTitle("Warning")
            msg.exec_()
            return
        
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Image to Delete", folder_path, "Image Files (*.png *.jpg *.bmp)", options=options)
    
        if fileName:
        # Ask for confirmation before deletion
            reply = QMessageBox.question(None, 'Confirm Deletion', f"Are you sure you want to delete {os.path.basename(fileName)}?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
            if reply == QMessageBox.Yes:
                try:
                    # Delete the selected image file
                    os.remove(fileName)
                    
                    # Show success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"{os.path.basename(fileName)} deleted successfully!")
                    msg.setWindowTitle("Success")
                    msg.exec_()

                    # Clear the QLabel if the deleted image was being displayed
                    self.widget.clear()
                    
                except Exception as e:
                    # Show error message if the deletion fails
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(f"Error deleting the image: {str(e)}")
                    msg.setWindowTitle("Error")
                    msg.exec_()

    def activate_script(self):
         # Path to the external Python script
        script_path = "/home/nounou/surveillance_system/surveillance.py"
        # Run the external script
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
                    
    def desactivate_script(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Surveillance script deactivated!")
            msg.setWindowTitle("Deactivated")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No script is running to stop!")
            msg.setWindowTitle("Warning")
            msg.exec_()        






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
