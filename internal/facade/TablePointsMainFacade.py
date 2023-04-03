from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QTableWidget, QComboBox, QTableWidgetItem, QFrame, QLineEdit, QFileDialog
from typing import List
import threading
from threading import Thread
import copy
from datetime import datetime
from internal.model.RoundDataModel import RoundDataModel
from internal.component.GlobalCurrentStateOfProgram import GlobalCurrentStateOfProgram
from internal.component.AlertMessageComponent import AlertMessageComponent
from internal.service.PointsDataSignalService import PointsDataSignalService
from internal.service.StateOfProgramSavingService import StateOfProgramSavingService
from internal.factory.StateOfProgramSavingModelFactory import StateOfProgramSavingModelFactory
from internal.model.StateOfProgramSavingModel import StateOfProgramSavingModel
from internal.model.PointsDataSignalModel import PointsDataSignalModel

class TablePointsMainFacade(QWidget):

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__()
        self.pointsDataSignalService: PointsDataSignalService = PointsDataSignalService()
        self.stateOfProgramSavingService: StateOfProgramSavingService = StateOfProgramSavingService()
        self.stateOfProgramSavingModelFactory: StateOfProgramSavingModelFactory = StateOfProgramSavingModelFactory()
        self.parent: QMainWindow = parent
        self.tablePointsMain: QTableWidget = parent.findChild(QTableWidget, "tableWidgetMain")
        if self.tablePointsMain is None:
            print("tablePointsMain NOT FOUND!")

        self.labelCurrentRoundNumber: QLabel = parent.findChild(QLabel, "labelCurrentRoundNumber")
        self.labelCurrentRoundNumber.setText("Текущий номер раунда: -")
        self.roundDataModels: List[RoundDataModel] = []

        self.inputJudge1Name: QLineEdit = parent.findChild(QLineEdit, "inputJudge1Name")
        self.judge1Name: str = "1-ый Судья"
        self.inputJudge1Name.setText(self.judge1Name)
        self.btnJudge1Update: QPushButton = parent.findChild(QPushButton, "btnJudge1Update")

        
        ...
        self.__fill_table_by_data()


    def setup_ui(self) -> None:
        if self.tablePointsMain is None:
            print("tablePointsMain NOT FOUND!")
            return
        
        ...
        self.tablePointsMain.setHorizontalHeaderLabels(["Раунд", self.judge1Name, self.judge2Name, self.judge3Name, "Сумма баллов"])

        
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.tablePointsMain:
            print("Call menu")
        return True

    def upload_input_signal(self, input_signal: str) -> None:
        pointsDataSignalModel: PointsDataSignalModel = self.pointsDataSignalService.parse_signal(input_signal=input_signal)
        if pointsDataSignalModel is None:
            print("pointsDataSignalModel is None")
            return
        print("pointsDataSignalModel получили")
        #нужно сохранить последний сигнал

        if GlobalCurrentStateOfProgram.is_round_started and GlobalCurrentStateOfProgram.is_port_connected and self.tablePointsMain.rowCount() > 0:
            if len(self.roundDataModels) - 1 < GlobalCurrentStateOfProgram.current_round_index:
                return
            roundDataModel: RoundDataModel = self.roundDataModels[GlobalCurrentStateOfProgram.current_round_index]
            judge_1_points: int = 0
            judge_2_points: int = 0
            judge_3_points: int = 0
            if GlobalCurrentStateOfProgram.pointsDataSignalModelLast is not None:
                print("Вычитаем значения с прошлой записи")
                judge_1_points = pointsDataSignalModel.judge1_point - GlobalCurrentStateOfProgram.pointsDataSignalModelLast.judge1_point
                judge_2_points = pointsDataSignalModel.judge2_point - GlobalCurrentStateOfProgram.pointsDataSignalModelLast.judge2_point
                judge_3_points = pointsDataSignalModel.judge3_point - GlobalCurrentStateOfProgram.pointsDataSignalModelLast.judge3_point
                if judge_1_points < 0:
                    judge_1_points = 1
                if judge_2_points < 0:
                    judge_2_points = 1
                if judge_3_points < 0:
                    judge_3_points = 1
            print("Добавляем judge_1_points: {0}, judge_2_points: {1}, judge_3_points: {2}".format(judge_1_points, judge_2_points, judge_3_points))
            
            ...
            
            self.__fill_table_by_data()

        GlobalCurrentStateOfProgram.pointsDataSignalModelLast = copy.copy(pointsDataSignalModel)
        


    
    def __add_row(self) -> None:
        rowCount: int = self.tablePointsMain.rowCount()
        self.tablePointsMain.insertRow(rowCount)
    
    def add_round(self) -> None:
        self.roundDataModels.append(
            RoundDataModel(
                name="Раунд",
                judge_1_point=0,
                judge_2_point=0,
                judge_3_point=0
            )
        )
        self.__fill_table_by_data()
        if self.tablePointsMain.rowCount() == 1:
            #GlobalCurrentStateOfProgram.current_round = 1
            self.set_row_round_active(0)

    def set_row_round_active(self, row_index: int) -> None:
        GlobalCurrentStateOfProgram.current_round_index = row_index
        self.labelCurrentRoundNumber.setText("Текущий номер раунда: " + str(row_index + 1))
        for index in range(self.tablePointsMain.rowCount()):
            for i in range(0, 5):
                self.tablePointsMain.item(index, i).setBackground(QtGui.QColor(255, 255, 255, 100))
        for i in range(0, 5):
            self.tablePointsMain.item(row_index, i).setBackground(QtGui.QColor(50, 50, 50, 50))

    def change_judge_name(self, judge_index: int) -> None:
        
        ...
        self.tablePointsMain.setHorizontalHeaderLabels(["Раунд", self.judge1Name, self.judge2Name, self.judge3Name])
    
    def update_cell_content(self, row: int, column: int, cell_content: str) -> None:
        if row > len(self.roundDataModels) - 1 or column > 3:
            return
        roundDataModel: RoundDataModel = self.roundDataModels[row]
        if column == 0:
            roundDataModel.name = cell_content
        elif column == 1:
            roundDataModel.judge_1_point = int(cell_content)
        elif 

        ...

        self.__fill_table_by_data()

    def delete_round_by_index(self, row: int) -> None:
        if row > len(self.roundDataModels) - 1:
            return
        self.roundDataModels.pop(row)
        if len(self.roundDataModels) == 0:
            GlobalCurrentStateOfProgram.current_round_index = 0
            self.labelCurrentRoundNumber.setText("Текущий номер раунда: -")
        elif GlobalCurrentStateOfProgram.current_round_index == row:
            self.set_row_round_active(row_index=0)
        self.__fill_table_by_data()


    def update_table(self) -> None:
        self.__fill_table_by_data()

    def __fill_table_by_data(self) -> None:
        
        list_of_rows_for_delete: List[str] = ["-"]
        self.tablePointsMain.setRowCount(0)
        if len(self.roundDataModels) == 0 or not GlobalCurrentStateOfProgram.is_port_connected:
            self.__set_btn_start_round_is_active(False)
            self.__set_btn_stop_round_is_active(False)
            self.__set_panel_round_status(label="- no connection -", is_active=False)
        elif GlobalCurrentStateOfProgram.is_round_started:
            ...

        for round_index in range(len(self.roundDataModels)):
            #добавляем модель в массив, если индекс строки не существует в массиве
            if self.tablePointsMain.rowCount() < (round_index + 1):
                self.__add_row()
            
            #qTableWidgetItemName: QTableWidgetItem = QTableWidgetItem(self.roundDataModels[round_index].name)
            self.tablePointsMain.setItem(round_index, 0, QTableWidgetItem(str(round_index + 1) + ". " + self.roundDataModels[round_index].name))
            self.tablePointsMain.setItem(round_index, 1, QTableWidgetItem(str(self.roundDataModels[round_index].judge_1_point)))
            
            ...

            if GlobalCurrentStateOfProgram.current_round_index == round_index:
                self.set_row_round_active(row_index=round_index)
            list_of_rows_for_delete.append(str(round_index + 1) + ". Раунд")
        
        #возможно в отдельную функцию
        #self.comboBoxListOfRows.clear()
        #self.comboBoxListOfRows.addItems(list_of_rows_for_delete)
    
    def __set_btn_start_round_is_active(self, value: bool) -> None:
        if value:
            self.btnStartRound.setStyleSheet("QPushButton"
                "{"
                    "background-color:green;"
                    "border-radius:4;"
                    "color:#252525;"
                "}"
            )
        else:
            self.btnStartRound.setStyleSheet("QPushButton"
                "{"
                    "background-color: rgba(50, 50, 50, 50);"
                    "border-radius:4;"
                    "color:#000000;"
                "}"
            )
        ...

    def __set_btn_stop_round_is_active(self, value: bool) -> None:
        if value:
            self.btnStopRound.setStyleSheet("QPushButton"
                "{"
                    "background-color:red;"
                    "border-radius:4;"
                    "color:#ffffff;"
                "}"
            )
        else:
            self.btnStopRound.setStyleSheet("QPushButton"
                "{"
                    "background-color: rgba(50, 50, 50, 50);"
                    "border-radius:4;"
                    "color:#000000;"
                "}"
            )
        ...

    def __set_panel_round_status(self, label: str, is_active: bool) -> None:
        if is_active:
            self.viewRoundStatus.setStyleSheet("QFrame"
                "{"
                    "background-color:green;"
                "}"
            )
        else:
            self.viewRoundStatus.setStyleSheet("QFrame"
                "{"
                    "background-color:red;"
                "}"
            )
        ...

    
    def save_as_custom_file(self):
        file_path_data = QFileDialog.getSaveFileName(self.parent, 'Save File')
        self.stateOfProgramSavingService.save_as_file(
            file_path_data=file_path_data,
            stateOfProgramSavingModel=self.stateOfProgramSavingModelFactory.create(
                judge1Name=self.judge1Name,
                judge2Name=self.judge2Name,
                judge3Name=self.judge3Name,
                roundDataModels=self.roundDataModels
            )
        )

    def try_load_from_custom_file(self) -> bool:
        file_path = QFileDialog.getOpenFileName(self, 'Open File')
        if file_path is None:
            AlertMessageComponent.show_message_box("Не удалось загрузить состояние программы из файла")
            return False
        if file_path[0] == "":
            return False
        print("try_load_from_custom_file file_path: " + str(file_path))
        
        stateOfProgramSavingModel: StateOfProgramSavingModel = self.stateOfProgramSavingService.load_from_file(file_path=file_path[0])
        if stateOfProgramSavingModel is None:
            AlertMessageComponent.show_message_box("Не удалось загрузить состояние программы из файла")
            return False
        if stateOfProgramSavingModel.last_session is None or stateOfProgramSavingModel.last_session == "":
            return False
        self.__get_data_from_loaded_model(stateOfProgramSavingModel=stateOfProgramSavingModel)
        self.__fill_table_by_data()
        return True
        
        

    def auto_save_current_state(self) -> None:
        print("auto_save_current_state")
        self.stateOfProgramSavingService.auto_save(
            self.stateOfProgramSavingModelFactory.create(
                judge1Name=self.judge1Name,
                judge2Name=self.judge2Name,
                judge3Name=self.judge3Name,
                roundDataModels=self.roundDataModels
            )
        )

    def try_load_last_autosave(self) -> bool:
        stateOfProgramSavingModel: StateOfProgramSavingModel = self.stateOfProgramSavingService.load_last_auto_save()
        if stateOfProgramSavingModel is None:
            #print("try_load_last_autosave stateOfProgramSavingModel is none")
            return False
        if stateOfProgramSavingModel.last_session is None or stateOfProgramSavingModel.last_session == "":
            return False
        self.__get_data_from_loaded_model(stateOfProgramSavingModel=stateOfProgramSavingModel)
        self.__fill_table_by_data()
        return True
    
    def __get_data_from_loaded_model(self, stateOfProgramSavingModel: StateOfProgramSavingModel) -> None:
        GlobalCurrentStateOfProgram.current_session = stateOfProgramSavingModel.last_session
        self.judge1Name = stateOfProgramSavingModel.judge1Name
        self.judge2Name = stateOfProgramSavingModel.judge2Name
        self.judge3Name = stateOfProgramSavingModel.judge3Name
        self.roundDataModels = stateOfProgramSavingModel.roundDataModels

    def try_export_to_excel_file(self) -> bool:
        file_path_data: tuple = QFileDialog.getSaveFileName(self.parent, 'Save File')
        if file_path_data is None or file_path_data[0] == "":
            return
        file_path: str = file_path_data[0]
        self.stateOfProgramSavingService.export_to_excel(
            file_path=file_path,
            stateOfProgramSavingModel=self.stateOfProgramSavingModelFactory.create(
                judge1Name=self.judge1Name,
                judge2Name=self.judge2Name,
                judge3Name=self.judge3Name,
                roundDataModels=self.roundDataModels
            )
        )

    def init_save_on_api(self) -> None:
        if GlobalCurrentStateOfProgram.is_async_sending_to_api_in_process:
            return
        thread_saving_on_api: Thread = Thread(
            target=self.__save_on_api,
            name="save_on_api"
        )
        thread_saving_on_api.start()

    def __save_on_api(self) -> None:
        GlobalCurrentStateOfProgram.is_async_sending_to_api_in_process = True
        try:
            self.stateOfProgramSavingService.save_on_api(
                stateOfProgramSavingModel=self.stateOfProgramSavingModelFactory.create(
                    judge1Name=self.judge1Name,
                    judge2Name=self.judge2Name,
                    judge3Name=self.judge3Name,
                    roundDataModels=self.roundDataModels
                ))
        finally:
            GlobalCurrentStateOfProgram.is_async_sending_to_api_in_process = False