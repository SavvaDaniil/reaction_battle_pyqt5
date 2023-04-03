from datetime import datetime
from dataclasses import dataclass
from typing import Union
from internal.model.PointsDataSignalModel import PointsDataSignalModel

@dataclass
class GlobalCurrentStateOfProgram:
    state: int = 0
    ...
    is_port_connected: bool = False
    pointsDataSignalModelLast: PointsDataSignalModel = None
    comPortLastConnect: Union[datetime, None] = None
    current_round_index: int = 0
    session_last_update: Union[datetime, None] = None
    is_round_started: bool = False
    selected_cell_content: Union[str, None] = None
    selected_cell_coordinates: Union[tuple, None] = None
    current_session: Union[str, None] = None
    is_saving_in_process: bool = False
    is_export_to_excel_in_process: bool = False
    is_async_sending_to_api_in_process: bool = False