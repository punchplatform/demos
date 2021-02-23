import numpy as np
import datetime
import uuid

from project.generator.GeneratorI import GeneratorI
from project.utils.Utils import write_array_json_to_file

def generate_degenerative_time_series_forecasting_prediction(past_weeks: int, min_count_user: int, max_count_user: int, projects: str, tools: str) -> list(dict()):
    result = []
    start_timestamp = datetime.datetime.utcnow()

    for project in projects:
        for tool in tools:
            all_expected_values = np.random.uniform(min_count_user, max_count_user, past_weeks+1)
            all_expected_values = np.array([[int(all_expected_values[i])] for i in range(0, past_weeks+1)])
            all_expected_values = all_expected_values[:, 0]

            all_timestamp = [start_timestamp - datetime.timedelta(7*i) for i in range(1, past_weeks+1)]
            all_timestamp.append(start_timestamp)

            for week in range(0, past_weeks+1):
                current_timestamp_delta = np.linspace(0, 604800, all_expected_values[week])
                for delta_timestamp in current_timestamp_delta:
                    current_record = {
                                "event_timestamp" : (all_timestamp[week] + datetime.timedelta(seconds=delta_timestamp)).strftime(
    "%Y-%m-%dT%H:%M:%S.000Z"
),
                                "user" : str(uuid.uuid1()),
                                "project" : project,
                                "tool" : tool
                                }
                    result.append(current_record)
    return result

class LicenceUsage(GeneratorI):
    def generateDataset(self, payload: dict, output: str) -> list:
        for conf in payload:
            data = generate_degenerative_time_series_forecasting_prediction(**conf)
            write_array_json_to_file(data, output)
