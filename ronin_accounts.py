from PyQt5 import QtCore, QtGui, QtWidgets


class Accounts_gui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 694)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 351, 671))
        self.frame.setStyleSheet("background-color:rgb(89, 79, 108);\n" "")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(30, 10, 311, 61))
        self.label.setObjectName("label")
        self.private_key_input = QtWidgets.QTextEdit(self.frame)
        self.private_key_input.setGeometry(QtCore.QRect(20, 80, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.private_key_input.setFont(font)
        self.private_key_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.private_key_input.setObjectName("private_key_input")
        self.ronin_add_input = QtWidgets.QTextEdit(self.frame)
        self.ronin_add_input.setGeometry(QtCore.QRect(20, 130, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ronin_add_input.setFont(font)
        self.ronin_add_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.ronin_add_input.setObjectName("ronin_add_input")
        self.gas_price_input = QtWidgets.QTextEdit(self.frame)
        self.gas_price_input.setGeometry(QtCore.QRect(20, 180, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.gas_price_input.setFont(font)
        self.gas_price_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.gas_price_input.setObjectName("gas_price_input")
        self.save_ronin_btn = QtWidgets.QPushButton(self.frame)
        self.save_ronin_btn.setGeometry(QtCore.QRect(20, 230, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.save_ronin_btn.setFont(font)
        self.save_ronin_btn.setStyleSheet(
            "            QPushButton:hover:!pressed\n"
            "            {\n"
            "              border: 1px solid rgb(231, 109, 109);\n"
            "              background-color:rgb(255, 255, 255);\n"
            "              color: rgb(231, 109, 109);\n"
            "            }\n"
            "            QPushButton{\n"
            "            background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "            }"
        )
        self.save_ronin_btn.setObjectName("save_ronin_btn")
        self.cancel_btn = QtWidgets.QPushButton(self.frame)
        self.cancel_btn.setGeometry(QtCore.QRect(180, 230, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setStyleSheet(
            "            QPushButton:hover:!pressed\n"
            "            {\n"
            "              border: 1px solid rgb(231, 109, 109);\n"
            "              background-color:rgb(255, 255, 255);\n"
            "              color: rgb(231, 109, 109);\n"
            "            }\n"
            "            QPushButton{\n"
            "            background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "            }"
        )
        self.cancel_btn.setObjectName("cancel_btn")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(350, 0, 541, 671))
        self.frame_2.setStyleSheet("background-color:rgb(53, 52, 88)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(20, 20, 501, 621))
        self.frame_3.setStyleSheet(
            "background-color:rgb(81, 79, 108);\n" "border-radius:5px;"
        )
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setGeometry(QtCore.QRect(20, 20, 461, 581))
        self.frame_4.setStyleSheet("background-color:rgb(111, 108, 144)")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 421, 41))
        self.label_2.setObjectName("label_2")
        self.account_list_view = QtWidgets.QListView(self.frame_4)
        self.account_list_view.setGeometry(QtCore.QRect(20, 70, 421, 321))
        self.account_list_view.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.account_list_view.setTabKeyNavigation(True)
        self.account_list_view.setObjectName("account_list_view")
        self.edit_btn = QtWidgets.QPushButton(self.frame_4)
        self.edit_btn.setGeometry(QtCore.QRect(20, 410, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.edit_btn.setFont(font)
        self.edit_btn.setStyleSheet(
            "            QPushButton:hover:!pressed\n"
            "            {\n"
            "              border: 1px solid rgb(231, 109, 109);\n"
            "              background-color:rgb(255, 255, 255);\n"
            "              color: rgb(231, 109, 109);\n"
            "            }\n"
            "            QPushButton{\n"
            "            background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "            }"
        )
        self.edit_btn.setObjectName("edit_btn")
        self.delete_btn = QtWidgets.QPushButton(self.frame_4)
        self.delete_btn.setGeometry(QtCore.QRect(240, 410, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.delete_btn.setFont(font)
        self.delete_btn.setStyleSheet(
            "            QPushButton:hover:!pressed\n"
            "            {\n"
            "              border: 1px solid rgb(231, 109, 109);\n"
            "              background-color:rgb(255, 255, 255);\n"
            "              color: rgb(231, 109, 109);\n"
            "            }\n"
            "            QPushButton{\n"
            "            background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "            }"
        )
        self.delete_btn.setObjectName("delete_btn")
        self.set_active_btn = QtWidgets.QPushButton(self.frame_4)
        self.set_active_btn.setGeometry(QtCore.QRect(20, 460, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.set_active_btn.setFont(font)
        self.set_active_btn.setStyleSheet(
            "            QPushButton:hover:!pressed\n"
            "            {\n"
            "              border: 1px solid rgb(231, 109, 109);\n"
            "              background-color:rgb(255, 255, 255);\n"
            "              color: rgb(231, 109, 109);\n"
            "            }\n"
            "            QPushButton{\n"
            "            background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "            }"
        )
        self.set_active_btn.setObjectName("set_active_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionFilters = QtWidgets.QAction(MainWindow)
        self.actionFilters.setObjectName("actionFilters")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit_2 = QtWidgets.QAction(MainWindow)
        self.actionQuit_2.setObjectName("actionQuit_2")
        self.menuFile.addAction(self.actionFilters)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit_2)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bloodmoon"))
        self.label.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#ffffff;">Setup your account</span></p></body></html>',
            )
        )
        self.private_key_input.setPlaceholderText(
            _translate("MainWindow", "Enter your private key...")
        )
        self.ronin_add_input.setPlaceholderText(
            _translate("MainWindow", "Enter your ronin address...")
        )
        self.gas_price_input.setPlaceholderText(
            _translate("MainWindow", "Gas price(leave blank for default value)")
        )
        self.save_ronin_btn.setText(_translate("MainWindow", "Save"))
        self.cancel_btn.setText(_translate("MainWindow", "Cancel"))
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; font-weight:600; color:#ffffff;">Ronin Accounts</span></p></body></html>',
            )
        )
        self.edit_btn.setText(_translate("MainWindow", "Edit"))
        self.delete_btn.setText(_translate("MainWindow", "Delete"))
        self.set_active_btn.setText(_translate("MainWindow", "Set as active"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFilters.setText(_translate("MainWindow", "Axie Filters"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit_2.setText(_translate("MainWindow", "Quit"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Accounts_gui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())