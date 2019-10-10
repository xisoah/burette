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
        MainWindow.setWindowOpacity(0.0)
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
        self.memList = QtWidgets.QListWidget(self.memGroup)
        self.memList.setGeometry(QtCore.QRect(10, 20, 221, 111))
        self.memList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.memList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.memList.setMovement(QtWidgets.QListView.Static)
        self.memList.setObjectName("memList")
        item = QtWidgets.QListWidgetItem()
        self.memList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.memList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.memList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.memList.addItem(item)
        self.memBtn = QtWidgets.QPushButton(self.memGroup)
        self.memBtn.setGeometry(QtCore.QRect(240, 20, 161, 31))
        self.memBtn.setObjectName("memBtn")
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
        self.memGroup.setTitle(_translate("MainWindow", "Memory"))
        __sortingEnabled = self.memList.isSortingEnabled()
        self.memList.setSortingEnabled(False)
        item = self.memList.item(0)
        item.setText(_translate("MainWindow", "a"))
        item = self.memList.item(1)
        item.setText(_translate("MainWindow", "b"))
        item = self.memList.item(2)
        item.setText(_translate("MainWindow", "c"))
        item = self.memList.item(3)
        item.setText(_translate("MainWindow", "d"))
        self.memList.setSortingEnabled(__sortingEnabled)
        self.memBtn.setText(_translate("MainWindow", "Populate"))
        self.tabs.setTabText(self.tabs.indexOf(self.tabPricing), _translate("MainWindow", "Pricing"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
