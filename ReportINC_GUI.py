
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QLabel, QGridLayout, QFileDialog, QSplashScreen
from PyQt5.QtWidgets import QPushButton, QStyleFactory
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
import os, sys
import ReportINC_base


import pkg_resources.py2_warn
import traceback
try:
    class Ui_MainWindow(object):
        def calc_func(self):
            ReportINC_base.generate_report(self)

        def logoooo(self):
            ReportINC_base.logo_choose(self)

    #Survey 1 Input
        def onInputFileButtonClicked1(self):
            options1 = QFileDialog.Options()
            filename1, filter1 = QFileDialog.getOpenFileName(None, caption='Open file',
                                                             filter='CSV files (*.csv)', options=options1)
            if filename1:
                 self.lineEdit_8.setText(filename1)

    # Survey 2 Input
        def onInputFileButtonClicked2(self):
            options2 = QFileDialog.Options()
            filename2, filter2 = QFileDialog.getOpenFileName(None, caption='Open file',
                                                             filter='CSV files (*.csv)', options=options2)
            if filename2:
                 self.lineEdit_9.setText(filename2)


    # Message Box
        def show_popup(self):
            msg = QMessageBox()
            msg.setWindowTitle("Done!")
            msg.setText("Check the Output folder!")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()


    #clear all
        def clear_all(self):
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
            self.lineEdit_8.clear()
            self.lineEdit_9.clear()
            self.lineEdit_17.clear()

            #when button is pressed this method is being called
        def do_action(self):
                # setting for loop to set value of progress bar
            for i in range(101):
                    # slowing down the loop
                time.sleep(0.05)

                    # setting value to progress bar
                self.pbar.setValue(i)



        #popup error message
        def popup_error(self):
            msg = QMessageBox()
            msg.setWindowTitle("Reportinc")
            msg.setText("Please, fill all the fields!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)

            x = msg.exec_()

        def check(self, list, val):
            return (all(x > val for x in list))

        def length_of_input(self):
            all_inputs = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
                          self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit_8.text(),
                          self.lineEdit_9.text(), self.lineEdit_10.text(), self.lineEdit_11.text(), self.lineEdit_12.text(),
                          self.lineEdit_13.text(), self.lineEdit_17.text()]

            length = [len(i) for i in all_inputs]
            return length


    # Pop up required field message
        def fill_all_fields(self):
            #a = self.lineEdit_2.text()
            #length = int(len(a))
            val=0
            length = self.length_of_input()
            if(self.check(length, val)):
                self.do_action()
                self.calc_func()
                self.show_popup()
                self.clear_all()


            else:
                self.popup_error()


        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(472, 345)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
            MainWindow.setSizePolicy(sizePolicy)
            MainWindow.setMouseTracking(False)
            MainWindow.setAnimated(True)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_7.setGeometry(QtCore.QRect(20, 10, 191, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_7.setFont(font)
            self.label_7.setObjectName("label_7")
            self.label_8 = QtWidgets.QLabel(self.centralwidget)
            self.label_8.setGeometry(QtCore.QRect(270, 10, 191, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_8.setFont(font)
            self.label_8.setObjectName("label_8")
            self.label_9 = QtWidgets.QLabel(self.centralwidget)
            self.label_9.setGeometry(QtCore.QRect(20, 230, 171, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_9.setFont(font)
            self.label_9.setObjectName("label_9")
            self.label_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_10.setGeometry(QtCore.QRect(20, 272, 43, 16))
            self.label_10.setObjectName("label_10")
            self.label_11 = QtWidgets.QLabel(self.centralwidget)
            self.label_11.setGeometry(QtCore.QRect(20, 302, 43, 16))
            self.label_11.setObjectName("label_11")
            self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3.setGeometry(QtCore.QRect(290, 270, 140, 41))
            self.pushButton_3.setObjectName("pushButton_3")
            #self.pushButton_3.clicked.connect(self.popup_error)
            self.pushButton_3.clicked.connect(self.fill_all_fields)
            #self.pushButton_3.clicked.connect(self.do_action)
            #self.pushButton_3.clicked.connect(self.calc_func)
            #self.pushButton_3.clicked.connect(self.show_popup)
            #self.pushButton_3.clicked.connect(self.clear_all)
            #self.pushButton_3.clicked.connect(self.lineEdit_6.clear)
            self.widget = QtWidgets.QWidget(self.centralwidget)
            self.widget.setGeometry(QtCore.QRect(20, 51, 121, 171))
            self.widget.setObjectName("widget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")

            self.label_17 = QtWidgets.QLabel(self.widget)
            self.label_17.setObjectName("label_17")
            self.verticalLayout.addWidget(self.label_17)

            self.label_1 = QtWidgets.QLabel(self.widget)
            self.label_1.setObjectName("label_1")
            self.verticalLayout.addWidget(self.label_1)
            self.label_2 = QtWidgets.QLabel(self.widget)
            self.label_2.setObjectName("label_2")
            self.verticalLayout.addWidget(self.label_2)
            self.clabel_3 = QtWidgets.QLabel(self.widget)
            self.clabel_3.setObjectName("clabel_3")
            self.verticalLayout.addWidget(self.clabel_3)
            self.label_4 = QtWidgets.QLabel(self.widget)
            self.label_4.setObjectName("label_4")
            self.verticalLayout.addWidget(self.label_4)
            self.label_5 = QtWidgets.QLabel(self.widget)
            self.label_5.setObjectName("label_5")
            self.verticalLayout.addWidget(self.label_5)
            self.label_6 = QtWidgets.QLabel(self.widget)
            self.label_6.setObjectName("label_6")
            self.verticalLayout.addWidget(self.label_6)

            self.label_16 = QtWidgets.QLabel(self.widget)
            self.label_16.setObjectName("label_16")
            self.verticalLayout.addWidget(self.label_16)


            self.widget1 = QtWidgets.QWidget(self.centralwidget)
            self.widget1.setGeometry(QtCore.QRect(110, 51, 121, 171))
            self.widget1.setObjectName("widget1")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
            self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.lineEdit_17 = QtWidgets.QLineEdit(self.widget1)
            self.lineEdit_17.setObjectName("lineEdit_17")
            self.verticalLayout_2.addWidget(self.lineEdit_17)
            self.lineEdit = QtWidgets.QLineEdit(self.widget1)
            self.lineEdit.setObjectName("lineEdit")
            self.verticalLayout_2.addWidget(self.lineEdit)
            self.lineEdit_2 = QtWidgets.QLineEdit(self.widget1)
            self.lineEdit_2.setObjectName("lineEdit_2")
            self.verticalLayout_2.addWidget(self.lineEdit_2)
            self.lineEdit_3 = QtWidgets.QLineEdit(self.widget1)
            self.lineEdit_3.setObjectName("lineEdit_3")
            self.verticalLayout_2.addWidget(self.lineEdit_3)
            self.lineEdit_4 = QtWidgets.QLineEdit(self.widget1)
            self.lineEdit_4.setObjectName("lineEdit_4")
            self.verticalLayout_2.addWidget(self.lineEdit_4)
            self.lineEdit_5 = QtWidgets.QLineEdit(self.widget1)
            self.lineEdit_5.setObjectName("lineEdit_5")
            self.verticalLayout_2.addWidget(self.lineEdit_5)
            self.dateEdit = QtWidgets.QDateEdit(self.widget1)
            self.dateEdit.setDate(QDate.currentDate())
            self.dateEdit.setCalendarPopup(True)
            self.dateEdit.setObjectName("dateEdit")
            self.verticalLayout_2.addWidget(self.dateEdit)

            self.comboBox = QtWidgets.QComboBox(self.centralwidget)
            self.comboBox.setObjectName("comboBox")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.verticalLayout_2.addWidget(self.comboBox)
            self.comboBox.currentIndexChanged.connect(self.logoooo)


            self.widget2 = QtWidgets.QWidget(self.centralwidget)
            self.widget2.setGeometry(QtCore.QRect(210, 270, 21, 51))
            self.widget2.setObjectName("widget2")
            self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget2)
            self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_7.setObjectName("verticalLayout_7")
            self.toolButton = QtWidgets.QToolButton(self.widget2)
            self.toolButton.setObjectName("toolButton")
            self.verticalLayout_7.addWidget(self.toolButton)
            self.toolButton.clicked.connect(self.onInputFileButtonClicked1)
            self.toolButton_2 = QtWidgets.QToolButton(self.widget2)
            self.toolButton_2.setObjectName("toolButton_2")
            self.toolButton_2.clicked.connect(self.onInputFileButtonClicked2)
            self.verticalLayout_7.addWidget(self.toolButton_2)
            self.widget3 = QtWidgets.QWidget(self.centralwidget)
            self.widget3.setGeometry(QtCore.QRect(74, 270, 131, 51))
            self.widget3.setObjectName("widget3")
            self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget3)
            self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_6.setObjectName("verticalLayout_6")
            self.lineEdit_8 = QtWidgets.QLineEdit(self.widget3)
            self.lineEdit_8.setObjectName("lineEdit_8")
            self.verticalLayout_6.addWidget(self.lineEdit_8)
            self.lineEdit_9 = QtWidgets.QLineEdit(self.widget3)
            self.lineEdit_9.setObjectName("lineEdit_9")
            self.verticalLayout_6.addWidget(self.lineEdit_9)
            self.widget4 = QtWidgets.QWidget(self.centralwidget)
            self.widget4.setGeometry(QtCore.QRect(270, 51, 77, 151))
            self.widget4.setObjectName("widget4")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget4)
            self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_3.setObjectName("verticalLayout_3")
            self.label = QtWidgets.QLabel(self.widget4)
            self.label.setObjectName("label")
            self.verticalLayout_3.addWidget(self.label)
            self.label_3 = QtWidgets.QLabel(self.widget4)
            self.label_3.setObjectName("label_3")
            self.verticalLayout_3.addWidget(self.label_3)
            self.label_12 = QtWidgets.QLabel(self.widget4)
            self.label_12.setObjectName("label_12")
            self.verticalLayout_3.addWidget(self.label_12)
            self.label_13 = QtWidgets.QLabel(self.widget4)
            self.label_13.setObjectName("label_13")
            self.verticalLayout_3.addWidget(self.label_13)
            self.label_14 = QtWidgets.QLabel(self.widget4)
            self.label_14.setObjectName("label_14")
            self.verticalLayout_3.addWidget(self.label_14)
            self.label_15 = QtWidgets.QLabel(self.widget4)
            self.label_15.setObjectName("label_15")
            self.verticalLayout_3.addWidget(self.label_15)
            self.widget5 = QtWidgets.QWidget(self.centralwidget)
            self.widget5.setGeometry(QtCore.QRect(350, 51, 101, 151))
            self.widget5.setObjectName("widget5")
            self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget5)
            self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.lineEdit_6 = QtWidgets.QLineEdit(self.widget5)
            self.lineEdit_6.setObjectName("lineEdit_6")
            self.lineEdit_6.setValidator(QDoubleValidator(-90, 90, 2))
            self.verticalLayout_4.addWidget(self.lineEdit_6)
            self.lineEdit_7 = QtWidgets.QLineEdit(self.widget5)
            self.lineEdit_7.setEnabled(True)
            self.lineEdit_7.setObjectName("lineEdit_7")
            self.lineEdit_7.setValidator(QDoubleValidator(-360, 360, 2))
            self.verticalLayout_4.addWidget(self.lineEdit_7)
            self.lineEdit_10 = QtWidgets.QLineEdit(self.widget5)
            self.lineEdit_10.setEnabled(True)
            self.lineEdit_10.setObjectName("lineEdit_10")
            self.lineEdit_10.setText("96.0")
            self.verticalLayout_4.addWidget(self.lineEdit_10)
            self.lineEdit_11 = QtWidgets.QLineEdit(self.widget5)
            self.lineEdit_11.setEnabled(True)
            self.lineEdit_11.setObjectName("lineEdit_11")
            self.lineEdit_11.setText("Wireline")
            self.verticalLayout_4.addWidget(self.lineEdit_11)
            self.lineEdit_12 = QtWidgets.QLineEdit(self.widget5)
            self.lineEdit_12.setEnabled(True)
            self.lineEdit_12.setObjectName("lineEdit_12")
            self.lineEdit_12.setText("Degree")
            self.verticalLayout_4.addWidget(self.lineEdit_12)
            self.lineEdit_13 = QtWidgets.QLineEdit(self.widget5)
            self.lineEdit_13.setEnabled(True)
            self.lineEdit_13.setObjectName("lineEdit_13")
            self.lineEdit_13.setText("Meter")
            self.verticalLayout_4.addWidget(self.lineEdit_13)
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 473, 21))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)




            self.pbar = QtWidgets.QProgressBar(self.centralwidget)
            self.pbar.setGeometry(290, 310, 141, 10)



        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "ReportINC"))
            self.label_7.setText(_translate("MainWindow", "General Information"))
            self.label_8.setText(_translate("MainWindow", "Drilling Parameters"))
            self.label_9.setText(_translate("MainWindow", "Import Survey Data"))
            self.label_10.setText(_translate("MainWindow", "Survey 1"))
            self.label_11.setText(_translate("MainWindow", "Survey 2"))
            self.pushButton_3.setText(_translate("MainWindow", "Generate Quality Report"))
            self.label_1.setText(_translate("MainWindow", "Borehole ID:"))
            self.label_2.setText(_translate("MainWindow", "Project Location:"))
            self.clabel_3.setText(_translate("MainWindow", "Client:"))
            self.label_4.setText(_translate("MainWindow", "Surveyor:"))
            self.label_5.setText(_translate("MainWindow", "Reporter:"))
            self.label_6.setText(_translate("MainWindow", "Survey Date:"))
            self.toolButton.setText(_translate("MainWindow", "..."))
            self.toolButton_2.setText(_translate("MainWindow", "..."))
            self.label.setText(_translate("MainWindow", "Dip:"))
            self.label_3.setText(_translate("MainWindow", "Azimuth:"))
            self.label_12.setText(_translate("MainWindow", "Drill Diameter:"))
            self.label_13.setText(_translate("MainWindow", "Survey Run on:"))
            self.label_14.setText(_translate("MainWindow", "Angular Units:"))
            self.label_15.setText(_translate("MainWindow", "Linear Units:"))
            self.label_16.setText(_translate("MainWindow", "Contractor:"))
            self.label_17.setText(_translate("MainWindow", "Project ID:"))
            self.comboBox.setItemText(0, _translate("MainWindow", "AT-Geotech"))
            self.comboBox.setItemText(1, _translate("MainWindow", "Az-Dagh Meden"))
            self.comboBox.setItemText(2, _translate("MainWindow", "Blasto"))
            self.comboBox.setItemText(3, _translate("MainWindow", "ATG"))


    class MyWindow(QtWidgets.QMainWindow):
        def closeEvent(self, event):
            result = QtWidgets.QMessageBox.question(self, "Close", "Are you sure you want to close the program ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            event.ignore()

            if result == QtWidgets.QMessageBox.Yes:
                event.accept()


    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        # Create and display the splash screen
        script_dir1 = os.path.dirname(__file__)
        rel_path5 = "logo\\reportinc-intro.png"
        intro = os.path.join(script_dir1, rel_path5)
        splash_pix = QPixmap(intro)
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()

        # Simulate something that takes time
        time.sleep(2)


        app.setStyle(QStyleFactory.create('Fusion'))
        rel_path6 = "logo\\taskbar-icon.png"
        taskbar_icon = os.path.join(script_dir1, rel_path6)
        app.setWindowIcon(QtGui.QIcon(taskbar_icon))
        #MainWindow = QtWidgets.QMainWindow()
        MainWindow = MyWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        splash.finish(MainWindow)
        status = app.exec_()
        sys.exit(status)


except Exception:
    traceback.print_exc()
    while(True):
        pass


