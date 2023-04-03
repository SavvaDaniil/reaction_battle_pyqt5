from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QLabel, QPushButton, QTableWidget, QComboBox, QTableWidgetItem, QMenu, QStatusBar, QAction
import sys
from internal.facade.TablePointsMainFacade import TablePointsMainFacade
from internal.facade.BlockPortConnectionFacade import BlockPortConnectionFacade
from internal.component.GlobalCurrentStateOfProgram import GlobalCurrentStateOfProgram
from internal.component.AlertMessageComponent import AlertMessageComponent
from internal.component.DialogWindowEditCell import DialogWindowEditCell
from internal.component.DialogWindowRoundDeletePrepare import DialogWindowRoundDeletePrepare
from dataclasses import dataclass
from threading import Thread
import time
from datetime import datetime, timedelta


portstatus = False
rxBuf: str = ""
COMport: QSerialPort = None

labelStatusData = None
tableWidgetMain: QTableWidget = None
tablePointsMain: QTableWidget = None
tablePointsMainFacade: TablePointsMainFacade = None
blockPortConnectionFacade: BlockPortConnectionFacade = None
comboBoxPorts: QComboBox = None
btnStartRound: QPushButton = None
btnStopRound: QPushButton = None
btnAddRound: QPushButton = None
thread_checking_port_connection: Thread = None



def ComRead():
    global rxBuf
    global labelStatusData
    global tablePointsMainFacade
    rx = COMport.readLine()
    print("COMport.readLine(): ", rx)
    try:
        rxs = str(rx, 'utf-8').strip()
        
        rxBuf += rxs
        GlobalCurrentStateOfProgram.comPortLastConnect = datetime.now()

        if (rxBuf[len(rxBuf) - 1] == ';'):
            print("buffer full")
            tablePointsMainFacade.upload_input_signal(input_signal=str(rxBuf))
            if labelStatusData is not None:
                labelStatusData.setText("Got signal: " + str(rxBuf))
            rxBuf = ""
    except Exception:
        print("Error reading signal from microcontroller")

def com_port_connect(port_name):
    com_connect(COMport, port_name)
    if(portstatus):
        print("Port connected")
    else:
        print("Error connection")
        AlertMessageComponent.show_message_box("Error connection")

def com_connect(serial, portname):
    global filename
    global portstatus
    serial.setPortName(portname)
    portstatus = serial.open(QIODevice.ReadWrite)


class DashboardUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(DashboardUI, self).__init__()
        uic.loadUi('internal/view/ReactionBattleDashboard.ui', self)
        self.setWindowIcon(QtGui.QIcon('assets/images/reaction_battle_logo.png'))
        self.setWindowTitle("Reaction Battle")
        global labelStatusData
        labelStatusData = self.findChild(QLabel, "labelStatusData")
        if labelStatusData is None:
            print("labelStatusData не найден!!!")

        global tablePointsMainFacade
        tablePointsMainFacade = TablePointsMainFacade(parent=self)
        tablePointsMainFacade.setup_ui()

        self.setStatusBar(QStatusBar(self))
        saveFileAction: QAction = QAction("&Save as", self)
        saveFileAction.setStatusTip('Save as')
        openFileAction: QAction = QAction("&Open", self)
        openFileAction.setStatusTip('Open')
        exportToExcelAction: QAction = QAction("&Export to excel", self)
        exportToExcelAction.setStatusTip('Export to excel')
        exitAction: QAction = QAction("&Exit", self)
        exitAction.setStatusTip('Exit')
        saveFileAction.triggered.connect(lambda: tablePointsMainFacade.save_as_custom_file())
        openFileAction.triggered.connect(lambda: tablePointsMainFacade.try_load_from_custom_file())
        exportToExcelAction.triggered.connect(lambda: tablePointsMainFacade.try_export_to_excel_file())
        exitAction.triggered.connect(self.close)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(exportToExcelAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        tablePointsMainFacade.tablePointsMain.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        tablePointsMainFacade.tablePointsMain.customContextMenuRequested.connect(self.right_mouse_menu)
        tablePointsMainFacade.tablePointsMain.selectionModel().selectionChanged.connect(self.onTableWidgetMainSelectionChanged)
        tablePointsMainFacade.tablePointsMain.itemDoubleClicked.connect(self.tableWidgetMainDoubleClickListener)
        tablePointsMainFacade.btnJudge1Update.clicked.connect(lambda: self.btn_update_judge_name_click_listener(1))
        tablePointsMainFacade.btnJudge2Update.clicked.connect(lambda: self.btn_update_judge_name_click_listener(2))
        tablePointsMainFacade.btnJudge3Update.clicked.connect(lambda: self.btn_update_judge_name_click_listener(3))
        tablePointsMainFacade.btnStartRound.clicked.connect(lambda: self.btn_round_control_listener(value=True))
        tablePointsMainFacade.btnStopRound.clicked.connect(lambda: self.btn_round_control_listener(value=False))


        global blockPortConnectionFacade
        blockPortConnectionFacade = BlockPortConnectionFacade(parent=self)
        blockPortConnectionFacade.btnStartPortListening.clicked.connect(lambda: self.reading_port_change_listener(value=True))
        blockPortConnectionFacade.btnStopPortListening.clicked.connect(lambda: self.reading_port_change_listener(value=False))


        global btnAddRound
        btnAddRound = self.findChild(QPushButton, "btnAddRound")
        btnAddRound.clicked.connect(self.btnAddRoundClickListener)

    def reading_port_change_listener(self, value: bool) -> None:
        global thread_checking_port_connection, COMport, portstatus, blockPortConnectionFacade, tablePointsMainFacade
        portNameNew: str = blockPortConnectionFacade.comboBoxPorts.currentText()
        if portNameNew == "- не выбрано":
            AlertMessageComponent.show_message_box("Выберите пожалуйста порт")
            return
        if value:
            
            COMport = QSerialPort()
            COMport.setBaudRate(115200)
            
            ...
            
            print("portstatus: " + str(portstatus))
            if not portstatus:
                return
            
            GlobalCurrentStateOfProgram.is_port_connected = True
            if thread_checking_port_connection is not None:
                thread_checking_port_connection = None
            thread_checking_port_connection = Thread(target=checking_port_connection, name="checking_port_connection")
            thread_checking_port_connection.start()
        else:
            COMport.close()
            GlobalCurrentStateOfProgram.pointsDataSignalModelLast = None
            GlobalCurrentStateOfProgram.is_port_connected = False
            GlobalCurrentStateOfProgram.is_round_started = False
            GlobalCurrentStateOfProgram.comPortLastConnect = None

        blockPortConnectionFacade.set_state_is_active(value=value)
        tablePointsMainFacade.update_table()


    def onTableWidgetMainSelectionChanged(self, selected, deselected) -> None:
        if len(selected.indexes()) > 1:
            return
        for ix in selected.indexes():
            print("onTableWidgetMainSelectionChanged Selected Item on: {0}x{1}".format(ix.row(), ix.column()))
            if ix.column() > 3:
                return
            GlobalCurrentStateOfProgram.selected_cell_coordinates = (ix.row(), ix.column())
            GlobalCurrentStateOfProgram.selected_cell_content = ix.data()
             

    def right_mouse_menu(self, pos) -> None:
        if GlobalCurrentStateOfProgram.selected_cell_coordinates is None:
            return
        print("right_mouse_menu")
        x = pos.x()
        y = pos.y()
        menu = QMenu()
        edit_option = menu.addAction('Edit cell')
        delete_option = menu.addAction('Delete cell')
        
        cell_content: str = GlobalCurrentStateOfProgram.selected_cell_content
        edit_option.triggered.connect(lambda: self.open_window_to_edit_tableWidgetItem(
                row=GlobalCurrentStateOfProgram.selected_cell_coordinates[0], 
                column=GlobalCurrentStateOfProgram.selected_cell_coordinates[1], 
                cell_content=cell_content
            )
        )
        delete_option.triggered.connect(lambda: self.open_window_to_round_delete_prepare(row=GlobalCurrentStateOfProgram.selected_cell_coordinates[0]))
        menu.exec_(self.mapToGlobal(QtCore.QPoint(x + 25, y + 180)))
        GlobalCurrentStateOfProgram.selected_cell_coordinates = None

    def open_window_to_edit_tableWidgetItem(self, row: int, column: int, cell_content: str) -> None:
        global tablePointsMainFacade
        dialog = DialogWindowEditCell(row=row, column=column, cell_content=cell_content, tablePointsMainFacade=tablePointsMainFacade)
        dialog.exec_()

    def open_window_to_round_delete_prepare(self, row: int) -> None:
        global tablePointsMainFacade
        dialog = DialogWindowRoundDeletePrepare(row=row, tablePointsMainFacade=tablePointsMainFacade)
        dialog.exec_()

    @QtCore.pyqtSlot(QtWidgets.QTableWidgetItem)
    def tableWidgetMainDoubleClickListener(self, item):
        global tablePointsMainFacade
        print("tableWidgetMainDoubleClickListener clicked on {0}x{1}".format(item.row(), item.column()))
        tablePointsMainFacade.set_row_round_active(row_index=item.row())


    def btn_update_judge_name_click_listener(self, judge_index: int) -> None:
        global tablePointsMainFacade
        tablePointsMainFacade.change_judge_name(judge_index=judge_index)

    def btnAddRoundClickListener(self):
        global tablePointsMainFacade
        tablePointsMainFacade.add_round()

    def btn_round_control_listener(self, value: bool):
        global tablePointsMainFacade
        GlobalCurrentStateOfProgram.is_round_started = value
        tablePointsMainFacade.update_table()

    def try_load_last_autosave(self) -> bool:
        global tablePointsMainFacade
        return tablePointsMainFacade.try_load_last_autosave()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        GlobalCurrentStateOfProgram.is_port_connected = False
        global thread_checking_port_connection, tablePointsMainFacade
        thread_checking_port_connection = None
        if len(tablePointsMainFacade.roundDataModels) > 0:
            tablePointsMainFacade.auto_save_current_state()
        return super().closeEvent(a0)

def checking_port_connection() -> None:
    global portstatus, COMport, window
    while GlobalCurrentStateOfProgram.is_port_connected:
        print("checking_port_connection")
        print("portstatus: " + str(portstatus))
        date_now: datetime = datetime.now()
        if GlobalCurrentStateOfProgram.comPortLastConnect is None:
            GlobalCurrentStateOfProgram.comPortLastConnect = date_now
            time.sleep(10)
            continue
        elif GlobalCurrentStateOfProgram.comPortLastConnect + timedelta(seconds=3) < datetime.now():
            print("EMERGENCY TURN OFF")
            window.reading_port_change_listener(value=False)
            break
        if len(tablePointsMainFacade.roundDataModels) > 0:
            tablePointsMainFacade.auto_save_current_state()
            tablePointsMainFacade.init_save_on_api()
        time.sleep(3)




window: DashboardUI = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    portList = []
    portList.append("- не выбрано")
    ports = QSerialPortInfo().availablePorts()
    for port in ports:
        portList.append(port.portName())
        print(port.portName())



    window = DashboardUI()
    blockPortConnectionFacade.set_list_of_ports(portList)

    if not window.try_load_last_autosave():
        datetime_now: datetime = datetime.now()
        GlobalCurrentStateOfProgram.current_session = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
        print("Failed autoload GlobalCurrentStateOfProgram.current_session: " + GlobalCurrentStateOfProgram.current_session)

    window.show()
    app.exec_()

