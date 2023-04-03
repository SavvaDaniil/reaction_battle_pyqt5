from dataclasses import dataclass, field
from typing import List, Union
from internal.model.RoundDataModel import RoundDataModel
from datetime import datetime

@dataclass
class StateOfProgramSavingModel:

    last_session: Union[str, None] = None
    judge1Name: Union[str, None] = None
    judge2Name: Union[str, None] = None
    judge3Name: Union[str, None] = None
    roundDataModels: List[RoundDataModel] = field(default_factory=[])