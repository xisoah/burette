from PyQt5 import QtCore, QtGui, QtWidgets
import Data.master as DataMaster
import Creation.master as CreateMaster
import pandas as pd
import sys

# insObj = DataMaster.process()
# master_dt = pd.DataFrame.from_dict(insObj, orient='index')
# col = ['pretty_name', 'instanceFamily', 'currentGeneration', 'memory', 'physicalProcessor', 'clockSpeed', 'vCPU',
# 'storage', 'ebs_iops', 'ECU', 'GPU', 'GPU_memory', 'GPU_model', 'processorFeatures', 'networkPerformance',
# 'dedicatedEbsThroughput', 'enhancedNetworking', 'us-east', 'us-east-2', 'us-west-2', 'us-west', 'ca-central-1',
# 'eu-ireland', 'eu-central-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'apac-sin', 'apac-syd', 'apac-tokyo',
# 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'sa-east-1', 'ap-east-1', 'me-south-1']
# master_dt = master_dt[col]

excel = 'D:\\Users\\sohai\\Desktop\\burette\\barebones\\Data\\df.xlsx'
df = pd.read_excel(excel)

# ip = CreateMaster.startInstance('ledgerformat', 't2.micro', 'eu-central-1a', '0.005')


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

    @staticmethod
    def addToList():
        memListTem = []
        dfList = df.memory.unique()
        for item in dfList:
            memListTem.append(str(item))
        memListTem.remove('nan')
        for index, item in enumerate(memListTem):
            memListTem[index] = item.replace(',', '')
        for index, item in enumerate(memListTem):
            if item.endswith('GiB'):
                memListTem[index] = float(item[:-4])
        memListTem.sort()
        for index, item in enumerate(memListTem):
            memListTem[index] = str(item) + ' GiB'
        memListTem.insert(0, 'nan')
        memListTem.insert(0, 'All')
        for index, entry in enumerate(memListTem):
            item = QtWidgets.QListWidgetItem()
            ui.memList.addItem(item)
            item = ui.memList.item(index)
            item.setText(str(entry))

    @staticmethod
    def populate():
        selection = [QtWidgets.QListWidgetItem.text(item) for item in ui.memList.selectedItems()]
        choice = selection[0]
        if choice == 'nan':  # Doesn't work
            print('You selected nan')
            model = PandasModel(df[(df.memory.isna())])
            ui.tableView.setModel(model)
        if choice == 'All':  # Doesn't work
            model = PandasModel(df)
            ui.tableView.setModel(model)
        if choice[:-4].endswith('.0'):
            choice = choice[:-6] + ' GiB'
            model = PandasModel(df[(df.memory == choice)])
            ui.tableView.setModel(model)
        if not choice[:-4].endswith('.0'):
            model = PandasModel(df[(df.memory == choice)])
            ui.tableView.setModel(model)
        print(choice)
        return choice

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 850)
        MainWindow.setWindowTitle("Burette")
        MainWindow.setWindowIcon(QtGui.QIcon('D:\\Users\\sohai\\Desktop\\burette\\app\\icon.png'))

        self.container = QtWidgets.QWidget(MainWindow)
        self.container.setObjectName("container")

        self.tabs = QtWidgets.QTabWidget(self.container)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 1200, 825))
        self.tabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabs.setObjectName("tabs")

        self.tabPricing = QtWidgets.QWidget()
        self.tabPricing.setObjectName("tabPricing")
        self.tabInstances = QtWidgets.QWidget()
        self.tabPricing.setObjectName("tabInstances")

        self.memGroup = QtWidgets.QGroupBox(self.tabPricing)
        self.memGroup.setGeometry(QtCore.QRect(10, 660, 1180, 141))
        self.memGroup.setObjectName("memGroup")
        self.memGroup.setTitle("Memory")

        self.memList = QtWidgets.QListWidget(self.memGroup)
        self.memList.setGeometry(QtCore.QRect(10, 20, 221, 111))
        self.memList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.memList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.memList.setObjectName("memList")
        Ui_MainWindow.addToList()
        self.memList.setSortingEnabled(True)

        self.memBtn = QtWidgets.QPushButton(self.memGroup)
        self.memBtn.setGeometry(QtCore.QRect(240, 20, 161, 31))
        self.memBtn.setObjectName("memBtn")
        self.memBtn.setText("Populate")
        self.memBtn.clicked.connect(ui.populate)

        initmodel = PandasModel(df)
        self.tableView = QtWidgets.QTableView(self.tabPricing)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 1180, 641))
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(initmodel)

        self.tabs.addTab(self.tabPricing, "")
        MainWindow.setCentralWidget(self.container)
        self.tabs.setTabText(self.tabs.indexOf(self.tabPricing), "Pricing")
        self.tabs.addTab(self.tabInstances, "")
        MainWindow.setCentralWidget(self.container)
        self.tabs.setTabText(self.tabs.indexOf(self.tabInstances), "Instances")

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
