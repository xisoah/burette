# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 850)
        self.container = QtWidgets.QWidget(MainWindow)
        self.container.setObjectName("container")
        self.tabs = QtWidgets.QTabWidget(self.container)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 1200, 825))
        self.tabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabs.setObjectName("tabs")
        self.tabPricing = QtWidgets.QWidget()
        self.tabPricing.setObjectName("tabPricing")
        self.memGroup = QtWidgets.QGroupBox(self.tabPricing)
        self.memGroup.setGeometry(QtCore.QRect(10, 660, 1180, 141))
        self.memGroup.setObjectName("memGroup")
        self.memBtn = QtWidgets.QPushButton(self.memGroup)
        self.memBtn.setGeometry(QtCore.QRect(810, 40, 161, 31))
        self.memBtn.setObjectName("memBtn")
        self.comboBox = QtWidgets.QComboBox(self.memGroup)
        self.comboBox.setGeometry(QtCore.QRect(12, 40, 181, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.memGroup)
        self.comboBox_2.setGeometry(QtCore.QRect(210, 40, 181, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.lineEdit = QtWidgets.QLineEdit(self.memGroup)
        self.lineEdit.setGeometry(QtCore.QRect(410, 40, 181, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.memBtn_2 = QtWidgets.QPushButton(self.memGroup)
        self.memBtn_2.setGeometry(QtCore.QRect(810, 100, 161, 31))
        self.memBtn_2.setObjectName("memBtn_2")
        self.label = QtWidgets.QLabel(self.memGroup)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.memGroup)
        self.label_2.setGeometry(QtCore.QRect(220, 20, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.memGroup)
        self.label_3.setGeometry(QtCore.QRect(420, 20, 91, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.memGroup)
        self.lineEdit_2.setGeometry(QtCore.QRect(610, 40, 181, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.memGroup)
        self.label_4.setGeometry(QtCore.QRect(620, 20, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.memGroup)
        self.label_5.setGeometry(QtCore.QRect(620, 80, 91, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.memGroup)
        self.lineEdit_3.setGeometry(QtCore.QRect(610, 100, 181, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.tableView = QtWidgets.QTableView(self.tabPricing)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 1180, 641))
        self.tableView.setObjectName("tableView")
        self.tabs.addTab(self.tabPricing, "")
        MainWindow.setCentralWidget(self.container)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Burette"))
        self.memGroup.setTitle(_translate("MainWindow", "Panel"))
        self.memBtn.setText(_translate("MainWindow", "Launch"))
        self.memBtn_2.setText(_translate("MainWindow", "Terminate"))
        self.label.setText(_translate("MainWindow", "Instance Type"))
        self.label_2.setText(_translate("MainWindow", "Availability Zone"))
        self.label_3.setText(_translate("MainWindow", "Pricing"))
        self.label_4.setText(_translate("MainWindow", "Token"))
        self.label_5.setText(_translate("MainWindow", "InstanceID"))
        self.tabs.setTabText(self.tabs.indexOf(self.tabPricing), _translate("MainWindow", "Pricing"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
