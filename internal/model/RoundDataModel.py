
from dataclasses import dataclass
from typing import Union

@dataclass
class RoundDataModel:

    #round_number: int = 0
    name: Union[str, None] = None
    judge_1_point: int = 0
    judge_2_point: int = 0
    judge_3_point: int = 0
    judge_points_ammount: int = 0