
from typing import List
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton
from internal.facade.TablePointsMainFacade import TablePointsMainFacade


class DialogWindowEditCell(QDialog):

    def __init__(self, row: int, column: int, cell_content: str, tablePointsMainFacade: TablePointsMainFacade) -> None:
        super().__init__()

        uic.loadUi('internal/view/ReactionBattleEditTableWidgetItem.ui', self)
        self.setWindowIcon(QtGui.QIcon('assets/images/reaction_battle_logo.png'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Edit cell")

        self.lineEditCellContent: QLineEdit = self.findChild(QLineEdit, "lineEditCellContent")
        self.btnSaveCellContent: QPushButton = self.findChild(QPushButton, "btnSaveCellContent")
        self.btnSaveCellContent.clicked.connect(self.update_cell_content)
        self.btnCanselSaveCellContent: QPushButton = self.findChild(QPushButton, "btnCanselSaveCellContent")
        self.btnCanselSaveCellContent.clicked.connect(self.close_action)
        self.tablePointsMainFacade = tablePointsMainFacade
        self.row = row
        self.column = column

        ...
        

    def update_cell_content(self) -> None:
        if self.tablePointsMainFacade is None:
            return
        self.tablePointsMainFacade.update_cell_content(
            row=self.row, 
            column=self.column, 
            cell_content=self.lineEditCellContent.text()
        )
        self.close()
    
    def close_action(self) -> None:
        self.close()