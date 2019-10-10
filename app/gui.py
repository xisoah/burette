from PyQt5 import QtCore, QtGui, QtWidgets
import Data.master as DataMaster
import Data.acdetails as Account
import Creation.master as CreateMaster
import Creation.instanceTools as iTools
import pandas as pd
import sys

insObj = DataMaster.process()
master_dt = pd.DataFrame.from_dict(insObj, orient='index')
insList = list(master_dt.index.values)
master_dt['PID'] = insList
col = ['PID', 'pretty_name', 'instanceFamily', 'currentGeneration', 'memory', 'physicalProcessor', 'clockSpeed', 'vCPU',
'storage', 'ebs_iops', 'ECU', 'GPU', 'GPU_memory', 'GPU_model', 'processorFeatures', 'networkPerformance',
'dedicatedEbsThroughput', 'enhancedNetworking', 'us-east', 'us-east-2', 'us-west-2', 'us-west', 'ca-central-1',
'eu-ireland', 'eu-central-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'apac-sin', 'apac-syd', 'apac-tokyo',
'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'sa-east-1', 'ap-east-1', 'me-south-1']
master_dt = master_dt[col]
df = master_dt

# excel = 'D:\\Users\\sohai\\Desktop\\burette\\barebones\\Data\\df.xlsx'
# df = pd.read_excel(excel)


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


class Ui_MainWindow(object):

    def addTo_memList(self):
        memListTem = []
        dfList = df.memory.unique()
        for item in dfList:
            memListTem.append(str(item))
        for index, item in enumerate(memListTem):
            memListTem[index] = item.replace(',', '')
        for index, item in enumerate(memListTem):
            if item.endswith('GiB'):
                memListTem[index] = float(item[:-4])
        memListTem.sort()
        for index, item in enumerate(memListTem):
            memListTem[index] = str(item) + ' GiB'
        memListTem.insert(0, 'All')
        for index, entry in enumerate(memListTem):
            item = QtWidgets.QListWidgetItem()
            self.memList.addItem(item)
            item = self.memList.item(index)
            item.setText(str(entry))

    def populate(self):
        selection = [QtWidgets.QListWidgetItem.text(item) for item in self.memList.selectedItems()]
        choice = selection[0]
        if choice == 'All':  # Doesn't work
            model = PandasModel(df)
            self.tableView.setModel(model)
        if choice[:-4].endswith('.0'):
            choice = choice[:-6] + ' GiB'
            model = PandasModel(df[(df.memory == choice)])
            self.tableView.setModel(model)
        if not choice[:-4].endswith('.0'):
            model = PandasModel(df[(df.memory == choice)])
            self.tableView.setModel(model)
        return choice

    def listInstancesTable(self):
        activeInstDict = iTools.listInstances()
        activeInstDF = pd.DataFrame.from_dict(activeInstDict, orient='index')
        insIDList = list(activeInstDF.index.values)
        activeInstDF['InstanceID'] = insIDList
        initmodel = PandasModel(activeInstDF)
        self.tableView2.setModel(initmodel)

    def addTo_instTypeComboBox(self):
        self.instTypeComboBox.clear()
        self.instTypeComboBox.addItems(insList)

    def addTo_zoneComboBox(self):
        zoneList = []
        self.zoneComboBox.clear()
        response = Account.getAll()
        for key, value in response.items():
            for zone in value['zones']:
                zoneList.append(zone['aZone'])
        self.zoneComboBox.addItems(zoneList)

    def launch(self):
        iType = str(self.instTypeComboBox.currentText())
        zone = str(self.zoneComboBox.currentText())
        price = self.pricingTextBox.text()
        token = self.tokenTextBox.text()
        print('Now launching ' + iType + ' instance in ' + zone + ' as ' + token + ' for ' + price)
        ip = CreateMaster.startInstance(token, iType, zone, price)

    def terminate(self):
        insID = self.instIdTextBox.text()
        activeInstDict = iTools.listInstances()
        iTools.cancelReq(activeInstDict[insID]['SpotID'])
        iTools.stopInstance(insID)
        print('Instance ' + insID + ' terminated')

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 850)
        MainWindow.setWindowTitle("Burette")
        MainWindow.setWindowIcon(QtGui.QIcon('D:\\Users\\sohai\\Desktop\\burette\\app\\icon.png'))

        self.container = QtWidgets.QWidget(MainWindow)

        self.tabs = QtWidgets.QTabWidget(self.container)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 1200, 825))
        self.tabs.setTabShape(QtWidgets.QTabWidget.Triangular)

        self.tabPricing = QtWidgets.QWidget()
        self.tabInstances = QtWidgets.QWidget()

        # Pricing Tab
        initmodel = PandasModel(df)
        self.tableView = QtWidgets.QTableView(self.tabPricing)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 1180, 641))
        self.tableView.setModel(initmodel)

        self.memGroup = QtWidgets.QGroupBox(self.tabPricing)
        self.memGroup.setGeometry(QtCore.QRect(10, 660, 1180, 141))
        self.memGroup.setTitle("Memory")

        self.memList = QtWidgets.QListWidget(self.memGroup)
        self.memList.setGeometry(QtCore.QRect(10, 20, 221, 111))
        self.memList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.memList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.addTo_memList()
        self.memList.setSortingEnabled(True)

        self.memBtn = QtWidgets.QPushButton(self.memGroup)
        self.memBtn.setGeometry(QtCore.QRect(240, 20, 161, 31))
        self.memBtn.setText("Populate")
        self.memBtn.clicked.connect(self.populate)

        self.tabs.addTab(self.tabPricing, "")
        MainWindow.setCentralWidget(self.container)
        self.tabs.setTabText(self.tabs.indexOf(self.tabPricing), "Pricing")
        # End

        # Instances Tab
        self.tableView2 = QtWidgets.QTableView(self.tabInstances)
        self.tableView2.setGeometry(QtCore.QRect(10, 10, 1180, 641))
        self.listInstancesTable()

        self.panelGroup = QtWidgets.QGroupBox(self.tabInstances)
        self.panelGroup.setGeometry(QtCore.QRect(10, 660, 1180, 141))
        self.panelGroup.setTitle("Panel")

        self.instTypeLabel = QtWidgets.QLabel(self.panelGroup)
        self.instTypeLabel.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.instTypeLabel.setText("Instance Type")

        self.instTypeComboBox = QtWidgets.QComboBox(self.panelGroup)
        self.instTypeComboBox.setGeometry(QtCore.QRect(12, 40, 181, 31))
        self.addTo_instTypeComboBox()

        self.zoneLabel = QtWidgets.QLabel(self.panelGroup)
        self.zoneLabel.setGeometry(QtCore.QRect(220, 20, 101, 16))
        self.zoneLabel.setText("Availability Zone")

        self.zoneComboBox = QtWidgets.QComboBox(self.panelGroup)
        self.zoneComboBox.setGeometry(QtCore.QRect(210, 40, 181, 31))
        self.addTo_zoneComboBox()

        self.pricingLabel = QtWidgets.QLabel(self.panelGroup)
        self.pricingLabel.setGeometry(QtCore.QRect(420, 20, 91, 16))
        self.pricingLabel.setText("Pricing")

        self.pricingTextBox = QtWidgets.QLineEdit(self.panelGroup)
        self.pricingTextBox.setGeometry(QtCore.QRect(410, 40, 181, 31))

        self.tokenLabel = QtWidgets.QLabel(self.panelGroup)
        self.tokenLabel.setGeometry(QtCore.QRect(620, 20, 91, 16))
        self.tokenLabel.setText("Token")

        self.tokenTextBox = QtWidgets.QLineEdit(self.panelGroup)
        self.tokenTextBox.setGeometry(QtCore.QRect(610, 40, 181, 31))

        self.launchBtn = QtWidgets.QPushButton(self.panelGroup)
        self.launchBtn.setGeometry(QtCore.QRect(810, 40, 161, 31))
        self.launchBtn.setText("Launch")
        self.launchBtn.clicked.connect(self.launch)

        self.instIdLabel = QtWidgets.QLabel(self.panelGroup)
        self.instIdLabel.setGeometry(QtCore.QRect(620, 80, 91, 16))
        self.instIdLabel.setText("InstanceID")

        self.instIdTextBox = QtWidgets.QLineEdit(self.panelGroup)
        self.instIdTextBox.setGeometry(QtCore.QRect(610, 100, 181, 31))

        self.terminateBtn = QtWidgets.QPushButton(self.panelGroup)
        self.terminateBtn.setGeometry(QtCore.QRect(810, 100, 161, 31))
        self.terminateBtn.setText("Terminate")
        self.terminateBtn.clicked.connect(self.terminate)

        self.tabs.addTab(self.tabInstances, "")
        MainWindow.setCentralWidget(self.container)
        self.tabs.setTabText(self.tabs.indexOf(self.tabInstances), "Instances")
        # End

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
