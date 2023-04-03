from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QComboBox, QTableWidgetItem, QFrame
from typing import List

class BlockPortConnectionFacade:

    def __init__(self, parent: QMainWindow) -> None:
        self.parent: QMainWindow = parent
        self.viewPortListeningStatus: QFrame = parent.findChild(QFrame, "viewPortListeningStatus")
        self.labelPortListeningStatus: QLabel = parent.findChild(QLabel, "labelPortListeningStatus")
        self.btnStartPortListening: QPushButton = parent.findChild(QPushButton, "btnStartPortListening")
        self.btnStopPortListening: QPushButton = parent.findChild(QPushButton, "btnStopPortListening")
        self.comboBoxPorts: QComboBox = parent.findChild(QComboBox, "comboBoxPorts")
        self.set_state_is_active(value=False)

    def set_list_of_ports(self, port_list: List[int]) -> None:
        if self.comboBoxPorts is None:
            return
        self.comboBoxPorts.addItems(port_list)

    def set_state_is_active(self, value: bool) -> None:
        if value:
            self.viewPortListeningStatus.setStyleSheet("QFrame"
                "{"
                    "background-color:green;"
                "}"
            )
            self.labelPortListeningStatus.setText("listening active")
            
            ...
        else:
            self.viewPortListeningStatus.setStyleSheet("QFrame"
                "{"
                    "background-color:red;"
                "}"
            )
            self.labelPortListeningStatus.setText("listening stopped")
            
            ...
    
