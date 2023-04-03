from typing import List
from internal.model.StateOfProgramSavingModel import StateOfProgramSavingModel
from internal.model.RoundDataModel import RoundDataModel
from internal.component.GlobalCurrentStateOfProgram import GlobalCurrentStateOfProgram

class StateOfProgramSavingModelFactory:

    def create(
        self, 
        judge1Name: str,
        judge2Name: str,
        judge3Name: str,
        roundDataModels: List[RoundDataModel]
    ) -> StateOfProgramSavingModel:
        return StateOfProgramSavingModel(
            ...
        )