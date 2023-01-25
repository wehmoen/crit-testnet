from PyQt5 import QtCore, QtGui, QtWidgets
import modules.create_filter as create_filter
from modules import main
from modules.ronin_accounts import Accounts_gui
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QDoubleValidator

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1010, 736)
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
        self.frame_left = QtWidgets.QFrame(self.centralwidget)
        self.frame_left.setGeometry(QtCore.QRect(0, 0, 441, 721))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_left.setFont(font)
        self.frame_left.setStyleSheet("background-color:rgb(81, 79, 108)")
        self.frame_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.name_input = QtWidgets.QLineEdit(self.frame_left)
        self.name_input.setGeometry(QtCore.QRect(30, 100, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_input.setFont(font)
        self.name_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.name_input.setObjectName("name_input")
        self.buy_price_input = QtWidgets.QLineEdit(self.frame_left)
        self.buy_price_input.setGeometry(QtCore.QRect(30, 150, 371, 31))
        onlyInt = QDoubleValidator()
        onlyInt.setRange(0.0, 1000,4)
        self.buy_price_input.setValidator(onlyInt)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buy_price_input.setFont(font)
        self.buy_price_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.buy_price_input.setObjectName("buy_price_input")

        self.num_axie_input = QtWidgets.QLineEdit(self.frame_left)
        self.num_axie_input.setGeometry(QtCore.QRect(30, 200, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.num_axie_input.setFont(font)
        self.num_axie_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.num_axie_input.setObjectName("num_axie_input")
        self.num_axie_input.setValidator(onlyInt)
        self.marketplace_link_input = QtWidgets.QLineEdit(self.frame_left)
        self.marketplace_link_input.setGeometry(QtCore.QRect(30, 250, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.marketplace_link_input.setFont(font)
        self.marketplace_link_input.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.marketplace_link_input.setObjectName("marketplace_link_input")
        self.bot_name = QtWidgets.QLabel(self.frame_left)
        self.bot_name.setGeometry(QtCore.QRect(50, 20, 321, 61))
        self.bot_name.setObjectName("bot_name")
        self.save_filter_btn = QtWidgets.QPushButton(self.frame_left)
        self.save_filter_btn.setGeometry(QtCore.QRect(30, 300, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.save_filter_btn.setFont(font)
        self.save_filter_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_filter_btn.setToolTipDuration(1)
        self.save_filter_btn.setStyleSheet(
            "QPushButton:hover:!pressed\n"
            "{\n"
            "  border: 1px solid rgb(231, 109, 109);\n"
            "  background-color:rgb(255, 255, 255);\n"
            "  color: rgb(231, 109, 109);\n"
            "}\n"
            "QPushButton{\n"
            "background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "}"
        )
        self.save_filter_btn.setObjectName("save_filter_btn")
        self.save_filter_btn.clicked.connect(self.save_filter)

        self.cancel_btn = QtWidgets.QPushButton(self.frame_left)
        self.cancel_btn.setGeometry(QtCore.QRect(220, 300, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_btn.setStyleSheet(
            "QPushButton:hover:!pressed\n"
            "{\n"
            "  border: 1px solid rgb(231, 109, 109);\n"
            "  background-color:rgb(255, 255, 255);\n"
            "  color: rgb(231, 109, 109);\n"
            "}\n"
            "QPushButton{\n"
            "background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "}"
        )
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.clear_inputs)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(440, 0, 571, 721))
        self.frame.setStyleSheet("background-color:rgb(53, 52, 88)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(30, 30, 511, 621))
        self.frame_2.setStyleSheet(
            "background-color:rgb(81, 79, 108);border-radius:5px;"
        )
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(20, 20, 471, 511))
        self.frame_3.setStyleSheet(
            "background-color:rgb(111, 108, 143);border-radius:5px;"
        )
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(20, 20, 431, 51))
        self.label.setStyleSheet(
            "background-color:rgb(231, 109, 109);color:rgb(255, 255, 255);border-radius:5px;"
        )
        self.label.setObjectName("label")
        self.sniping_list_view = QtWidgets.QListView(self.frame_3)
        self.sniping_list_view.setGeometry(QtCore.QRect(20, 90, 431, 281))
        self.sniping_list_view.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.sniping_list_view.setObjectName("sniping_list_view")
        self.model = QtGui.QStandardItemModel()
        self.sniping_list_view.setModel(self.model)

        self.get_list()

        self.edit_btn = QtWidgets.QPushButton(self.frame_3)
        self.edit_btn.setGeometry(QtCore.QRect(20, 380, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.edit_btn.setFont(font)
        self.edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_btn.setStyleSheet(
            "QPushButton:hover:!pressed\n"
            "{\n"
            "  border: 1px solid rgb(231, 109, 109);\n"
            "  background-color:rgb(255, 255, 255);\n"
            "  color: rgb(231, 109, 109);\n"
            "}\n"
            "QPushButton{\n"
            "background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "}"
        )
        self.edit_btn.setObjectName("edit_btn")
        self.edit_btn.clicked.connect(self.edit_filter)

        self.delete_btn = QtWidgets.QPushButton(self.frame_3)
        self.delete_btn.setGeometry(QtCore.QRect(250, 380, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.delete_btn.setFont(font)
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_btn.setStyleSheet(
            "QPushButton:hover:!pressed\n"
            "{\n"
            "  border: 1px solid rgb(231, 109, 109);\n"
            "  background-color:rgb(255, 255, 255);\n"
            "  color: rgb(231, 109, 109);\n"
            "}\n"
            "QPushButton{\n"
            "background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "}"
        )
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.delete_filter)

        self.run_btn = QtWidgets.QPushButton(self.frame_3)
        self.run_btn.setGeometry(QtCore.QRect(20, 440, 431, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.run_btn.setFont(font)
        self.run_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.run_btn.setStyleSheet(
            "QPushButton:hover:!pressed\n"
            "{\n"
            "  border: 1px solid rgb(231, 109, 109);\n"
            "  background-color:rgb(255, 255, 255);\n"
            "  color: rgb(231, 109, 109);\n"
            "}\n"   
            "QPushButton{\n"
            "background-color:rgb(231, 109, 109); color: rgb(255, 255, 255);border-radius: 5px;\n"
            "}"
        )
        self.run_btn.setObjectName("run_btn")
        self.run_btn.clicked.connect(self.start_bot)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1010, 26))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionRonin_Accounts = QtWidgets.QAction(MainWindow)
        self.actionRonin_Accounts.setObjectName("actionRonin_Accounts")
        self.actionRonin_Accounts.triggered.connect(lambda: self.ronin_window())

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(QtWidgets.qApp.quit)
        self.menuFIle.addAction(self.actionRonin_Accounts)

        self.menuFIle.addSeparator()
        self.menuFIle.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CRIT"))
        self.name_input.setWhatsThis(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Name your axie sniper...</p></body></html>",
            ) 
        )

        self.name_input.setPlaceholderText(
            _translate("MainWindow", "Name your axie sniper...  ")
        )

        self.buy_price_input.setPlaceholderText(
            _translate("MainWindow", "Set the buy price...  ")
        )

        self.num_axie_input.setPlaceholderText(
            _translate(
                "MainWindow", "How many axie's should it buy before stopping...  "
            )
        )

        self.marketplace_link_input.setPlaceholderText(
            _translate("MainWindow", "Paste the marketplace filter link here...  ")
        )
        self.bot_name.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; font-weight:600; color:#ffffff;">QU3ST Axie Sniper</span></p></body></html>',
            )
        )
        self.save_filter_btn.setText(_translate("MainWindow", "Save My Filter"))
        self.cancel_btn.setText(_translate("MainWindow", "Cancel"))
        self.label.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; font-weight:600;">My Sniping List</span></p></body></html>',
            )
        )
        self.edit_btn.setText(_translate("MainWindow", "Edit"))
        self.delete_btn.setText(_translate("MainWindow", "Delete"))
        self.run_btn.setText(_translate("MainWindow", "Run Axie Sniper"))
        self.menuFIle.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionRonin_Accounts.setText(_translate("MainWindow", "Ronin Accounts"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def clear_inputs(self):
        """Clear GUI Inputs"""
        self.name_input.clear()
        self.buy_price_input.clear()
        self.num_axie_input.clear()
        self.marketplace_link_input.clear()

    def save_filter(self):
        """Save filter from GUI"""

        filter_name = self.name_input.text()
        check_name = create_filter.get_filter_by_name(filter_name)
        buy_price = self.buy_price_input.text()
        num_axie = self.num_axie_input.text()
        axie_filter = self.marketplace_link_input.text()
        if filter_name =="" or check_name == "" or buy_price =="" or num_axie=="" or axie_filter=="":
            print("Please add a valid data...") 
        else:
            if len(check_name) >= 1:
                create_filter.gui_update(filter_name, buy_price, axie_filter, num_axie)
                print(f"Filter {filter_name} is updated...")
                self.clear_inputs()
            else:
                print(f"Filter {filter_name} is added...")
                self.clear_inputs()
                return (
                    create_filter.create_filter(
                        1, filter_name, buy_price, num_axie, axie_filter
                    ),
                    self.get_list(),
                )

    def get_list(self):
        """Get Sniping List"""
        snipe_list = create_filter.get_snipe_list()
        self.model.removeRows(0, self.model.rowCount())
        for i in snipe_list:
            item = QtGui.QStandardItem(i[0])
            self.model.appendRow(item)

    def delete_filter(self):
        """Delete filter on GUI"""
        try:
            for index in self.sniping_list_view.selectedIndexes():
                item = self.model.itemFromIndex(index)
                filter_name = item.text()
            create_filter.delete_filter(filter_name)
            self.get_list()
            print(f"Filter {filter_name} is deleted...")
        except:
            print("Select a filter to delete on the list above...")

    def edit_filter(self):
        """Edit filter on GUI"""
        try:
            for index in self.sniping_list_view.selectedIndexes():
                item = self.model.itemFromIndex(index)
                filter_name = item.text()
            filter_data = create_filter.get_filter_by_name(filter_name)
            self.name_input.setText(filter_data[0][0])
            self.buy_price_input.setText(str(filter_data[0][1]))
            self.num_axie_input.setText(str(filter_data[0][3]))
            self.marketplace_link_input.setText(filter_data[0][4])
        except:
            print("Select a filter to edit on the list above...")

    def start_bot(self):
        """Start BOT on GUI"""
        self.search_axie = WorkerThread()
        self.search_axie.start()

    def ronin_window(self):
        """Open Ronin Accounts Window"""
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Accounts_gui()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

class WorkerThread(QThread):
    def run(self):
        main.init()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
