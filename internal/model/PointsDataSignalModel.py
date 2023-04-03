
from dataclasses import dataclass
from typing import Union

@dataclass
class PointsDataSignalModel:
    
    input_signal: Union[str, None] = None
    judge1_point: int = 0
    judge2_point: int = 0
    judge3_point: int = 0