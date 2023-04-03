
from internal.model.PointsDataSignalModel import PointsDataSignalModel

class PointsDataSignalService:

    def parse_signal(self, input_signal: str) -> PointsDataSignalModel:
        try:
            print("PointsDataSignalService parse_signal input_signal: " + input_signal)
            parsed_input = input_signal.strip(';').split(',')
            print("len(parsed_input): " + str(len(parsed_input)))
            if len(parsed_input) != 4:
                return None
            judge1_point: int = int(parsed_input[1])
            judge2_point: int = int(parsed_input[2])
            judge3_point: int = int(parsed_input[3])

            return PointsDataSignalModel(
                input_signal=input_signal,
                judge1_point=judge1_point,
                judge2_point=judge2_point,
                judge3_point=judge3_point
            )
        except Exception:
            print("PointsDataSignalService parse_signal ОШИБКА!")
        return None