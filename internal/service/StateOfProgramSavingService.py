import pickle
import os
import os.path
import platform
import pandas
import requests
from requests import Session
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import HTTPError
from typing import List
from pandas import DataFrame
import json
from internal.model.StateOfProgramSavingModel import StateOfProgramSavingModel
from internal.component.GlobalCurrentStateOfProgram import GlobalCurrentStateOfProgram


class StateOfProgramSavingService:

    FILE_NAME: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.pkl"

    def save_as_file(self, file_path_data: tuple, stateOfProgramSavingModel: StateOfProgramSavingModel) -> None:
        if GlobalCurrentStateOfProgram.is_saving_in_process:
            return
        GlobalCurrentStateOfProgram.is_saving_in_process = True
        if file_path_data[0] == "":
            return
        try:
            print("StateOfProgramSavingService save_as_file file_name: " + file_path_data[0])
            file_name: str = file_path_data[0]
            
            ...

            with open(file_name, "wb") as state_last_file:
                pickle.dump(stateOfProgramSavingModel, state_last_file)
        except Exception:
            print("StateOfProgramSavingService save_as_file ошибка сохранения")
        GlobalCurrentStateOfProgram.is_saving_in_process = False

    def auto_save(self, stateOfProgramSavingModel: StateOfProgramSavingModel) -> None:
        if GlobalCurrentStateOfProgram.is_saving_in_process:
            return
        GlobalCurrentStateOfProgram.is_saving_in_process = True
        try:
            with open(StateOfProgramSavingService.FILE_NAME, "wb") as state_last_file:
                pickle.dump(stateOfProgramSavingModel, state_last_file)
        except Exception:
            print("StateOfProgramSavingService auto_save ошибка сохранения")
        GlobalCurrentStateOfProgram.is_saving_in_process = False

    def load_from_file(self, file_path: str) -> StateOfProgramSavingModel:
        stateOfProgramSavingModel: StateOfProgramSavingModel = None
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    stateOfProgramSavingModel = pickle.load(f)
            else:
                print("StateOfProgramSavingService load_from_file file not found")
        except Exception:
            return None
        finally:
            return stateOfProgramSavingModel
        

    def load_last_auto_save(self) -> StateOfProgramSavingModel:
        stateOfProgramSavingModel: StateOfProgramSavingModel = None
        try:
            if os.path.exists(StateOfProgramSavingService.FILE_NAME):
                with open(StateOfProgramSavingService.FILE_NAME, 'rb') as f:
                    stateOfProgramSavingModel = pickle.load(f)
            else:
                print("StateOfProgramSavingService load_last_auto_save file not found")
        except Exception:
            return None
        finally:
            return stateOfProgramSavingModel

    def export_to_excel(self, file_path: str, stateOfProgramSavingModel: StateOfProgramSavingModel) -> None:
        if file_path is None or file_path == "" or stateOfProgramSavingModel is None:
            return
        if GlobalCurrentStateOfProgram.is_export_to_excel_in_process:
            return
        GlobalCurrentStateOfProgram.is_export_to_excel_in_process = True
        try:
            list_data_to_data_frame: List = []
            schetchik: int = 0
            for roundDataModel in stateOfProgramSavingModel.roundDataModels:
                
                ...
                list_data_to_data_frame.append(round_data_row)

            ...

            dataFrame = pandas.DataFrame(
                data=list_data_to_data_frame,
                columns=[
                    "Наименование",
                    stateOfProgramSavingModel.judge1Name,
                    stateOfProgramSavingModel.judge2Name,
                    stateOfProgramSavingModel.judge3Name,
                    "Сумма баллов"
                ]
            )
            dataFrame.to_excel(file_path, index=False)
        except Exception:
            print("StateOfProgramSavingService export_to_excel ошибка экспорта")
        GlobalCurrentStateOfProgram.is_export_to_excel_in_process = False


    def save_on_api(self, stateOfProgramSavingModel: StateOfProgramSavingModel) -> None:

        try:
            url = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            roundDataModels_data = []
            for roundDataModel in stateOfProgramSavingModel.roundDataModels:
                roundDataModels_data.append(
                    {
                        "name" : roundDataModel.name,
                        ...
                    }
                )
            json_data = json.dumps({
                "session_name": os.getlogin() + " (" + platform.node() + ") - " + stateOfProgramSavingModel.last_session,
                ...
                "roundDataModels" : roundDataModels_data
            })

            headers = {'Content-type': 'application/json'}
            session: Session = requests.Session()
            session.verify = False
            session.headers = headers
            response = session.post(url, data=json_data, headers=headers, verify=False)

        except HTTPError:
            print("StateOfProgramSavingService save_on_api HTTPError error")
        except requests.exceptions.SSLError as sslError:
            print("StateOfProgramSavingService save_on_api SSLError: " + str(sslError))
        except Exception as exception:
            print("StateOfProgramSavingService save_on_api Failed: " + str(exception))