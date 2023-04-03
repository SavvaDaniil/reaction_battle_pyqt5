
from typing import List
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from internal.facade.TablePointsMainFacade import TablePointsMainFacade


class DialogWindowRoundDeletePrepare(QDialog):

    def __init__(self, row: int, tablePointsMainFacade: TablePointsMainFacade) -> None:
        super().__init__()

        uic.loadUi('internal/view/ReactionBattleDeleteRowPrepare.ui', self)
        self.setWindowIcon(QtGui.QIcon('assets/images/reaction_battle_logo.png'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Delete round")

        self.labelRoundDeletePrepareTitle: QLabel = self.findChild(QLabel, "labelRoundDeletePrepareTitle")
        self.labelRoundDeletePrepareTitle.setText("Вы уверены, что хотите удалить\nраунд №" + str(row + 1) + "?")
        self.btnDeleteRound: QPushButton = self.findChild(QPushButton, "btnDeleteRound")
        self.btnDeleteRound.clicked.connect(self.delete_round)
        self.btnCanselDeleteRound: QPushButton = self.findChild(QPushButton, "btnCanselDeleteRound")
        self.btnCanselDeleteRound.clicked.connect(self.close_action)
        self.tablePointsMainFacade = tablePointsMainFacade
        self.row = row
        #print("row: {0} column: {1}".format(row, column))

    def delete_round(self) -> None:
        
        ...
        self.close()
    
    def close_action(self) -> None:
        self.close()