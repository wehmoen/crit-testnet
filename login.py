from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from modules.sub_modules import db
import crit
from modules.sub_modules import save_key_ronin
from cryptography.fernet import Fernet
import os


success = False
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(396, 248)
        MainWindow.setStyleSheet("background-color:rgb(53, 52, 88)")
        MainWindow.setWindowIcon(QtGui.QIcon("image\QUEST_logo_sword_RGB-1.ico"))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 331, 101))
        self.label.setObjectName("label")
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(80, 100, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password_input.setFont(font)
        self.password_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setObjectName("password_input")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        if self.check_db():
            self.pushButton.setGeometry(QtCore.QRect(130, 145, 121, 31))
            self.pushButton.clicked.connect(self.user_login)
        else:
            self.password_input_2 = QtWidgets.QLineEdit(self.centralwidget)
            self.password_input_2.setGeometry(QtCore.QRect(80, 140, 221, 31))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.password_input_2.setFont(font)
            self.password_input_2.setStyleSheet("background-color:rgb(255, 255, 255)")
            self.password_input_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_input_2.setObjectName("password_input_2")
            self.pushButton.setGeometry(QtCore.QRect(130, 180, 121, 31))
            self.pushButton.clicked.connect(self.main_window)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "            QPushButton:hover:!pressed\n"
            "            {\n"
            "            border: 1px solid rgb(231, 109, 109);\n"
            "            background-color:rgb(255, 255, 255);\n"
            "            color: rgb(231, 109, 109);\n"
            "            }\n"
            "            QPushButton{\n"
            "            background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "            }"
        )
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        if self.check_db():
            MainWindow.setWindowTitle(_translate("MainWindow", "Login"))
            self.label.setText(
                _translate(
                    "MainWindow",
                    "<html><head/><body><p align='center'><span style=' font-size:22pt; font-weight:600; color:#ffffff;'>Verify it's you</span></p></body></html>",
                )
            )
            self.password_input.setPlaceholderText(
                _translate("MainWindow", "Enter your password")
            )

            self.pushButton.setText(_translate("MainWindow", "Continue"))

        else:
            MainWindow.setWindowTitle(_translate("MainWindow", "Set Password"))
            self.label.setText(
                _translate(
                    "MainWindow",
                    '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600; color:#ffffff;">Set your password</span></p></body></html>',
                )
            )
            self.password_input.setPlaceholderText(
                _translate("MainWindow", "Set your password")
            )
            self.password_input_2.setPlaceholderText(
                _translate("MainWindow", "Re-type your password")
            )
            self.pushButton.setText(_translate("MainWindow", "Save"))

    def try_decrypt(self,user_input):
        """Try to decrypt private key"""
        key_data = db.records("SELECT * FROM keys WHERE status =?", "active")
        db.commit
        try:
            salt = save_key_ronin.read_KEK()
            password = bytes(user_input, "utf-8")
            decryption_key = save_key_ronin.get_decryption_key(password, salt)
            f = Fernet(decryption_key)
            pvt_key_bytes = f.decrypt(key_data[0][0])
            pvt_key = pvt_key_bytes.decode("utf-8")
            return pvt_key

        except Exception as e:
            print(e)
    
    def check_db(self):
        """Check db if it has any data"""
        accounts = db.records("SELECT * FROM keys")
        db.commit

        if len(accounts) > 0 :
            return True
        else:
            return False

    def main_window(self):
        """Main window if the password matches"""
        p1 = self.password_input.text()
        p2 = self.password_input_2.text()

        if p1=="" and p2 == "":
            msg =QMessageBox()
            msg.setWindowTitle("Crit Bot")
            msg.setText("Password can't be empty.")
            x = msg.exec_()
        elif p1 == p2 :
            MainWindow.close()
            self.new_window = QtWidgets.QMainWindow()
            self.ui = crit.Crit_MainWindow()
            self.ui.setupUi(self.new_window)
            self.new_window.show()
            os.environ['user_pass'] = p2
            
        else:
            msg =QMessageBox()
            msg.setWindowTitle("Crit Bot")
            msg.setText("Password doesn't match")
            self.password_input.clear()
            self.password_input_2.clear()
            x = msg.exec_()
    
    def user_login(self):
        """Existing User login"""
        user_password = self.password_input.text()
        try:
            key = self.try_decrypt(user_password)
            if key :
                MainWindow.close()
                os.environ['user_pass'] = user_password
                self.new_window = QtWidgets.QMainWindow()
                self.ui = crit.Crit_MainWindow()
                self.ui.setupUi(self.new_window)
                self.new_window.show()

            else:
                msg =QMessageBox()
                msg.setWindowTitle("Crit Bot")
                msg.setText("Incorrect Password!")
                self.password_input.clear()
                x = msg.exec_()

        except Exception as e :
            msg =QMessageBox()
            msg.setWindowTitle("Crit Bot")
            msg.setText(f"Error: {e}")
            self.password_input.clear()
            x = msg.exec_()
            


if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
