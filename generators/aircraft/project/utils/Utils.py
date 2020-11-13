from mlflow.sklearn import load_model
import numpy as np
import copy
import datetime
import json
import uuid


def write_array_json_to_file(input_data: list(), output_path: str):
    with open(output_path, "w") as file:
        for record in input_data:
            file.write(json.dumps(record))
            file.write("\n")


def generate_linear_aircraft_sensor_values(
    aircraft_number: int, max_cycle_number: int, cycle_schedule_s: int, model_path: str
) -> list():
    regression_best_model = load_model(model_path)
    to_return = []
    meta = {"cycle": {"schedule": cycle_schedule_s}}
    all_aircraft_cycles = (max_cycle_number - 1) * np.random.random(aircraft_number) + 1
    all_aircraft_id = [uuid.uuid1() for i in range(0, aircraft_number)]

    for i in range(0, aircraft_number):
        current_cycle_number = int(all_aircraft_cycles[i])
        current_aircraft_id = all_aircraft_id[i]

        start_timestamp = datetime.datetime.utcnow()

        all_timestamp = [
            start_timestamp + datetime.timedelta(seconds=(i * cycle_schedule_s))
            for i in range(0, current_cycle_number)
        ]
        all_cycles = [i for i in range(1, current_cycle_number + 1)]
        all_sensor_values = np.linspace(0, 1.0, current_cycle_number)
        all_sensor_life_percent = regression_best_model.predict(
            all_sensor_values.reshape(-1, 1)
        ).tolist()
        all_death_counter = [
            int((all_cycles[i] / all_sensor_life_percent[i]) - all_cycles[i])
            for i in range(0, current_cycle_number)
        ]
        all_predicted_death_timestamp = [
            start_timestamp
            + datetime.timedelta(seconds=(cycle_left * cycle_schedule_s))
            for cycle_left in all_death_counter
        ]

        for timestamp, cycle, sensor, life, cycle_left, death_timestamp in zip(
            all_timestamp,
            all_cycles,
            all_sensor_values,
            all_sensor_life_percent,
            all_death_counter,
            all_predicted_death_timestamp,
        ):
            current_record = copy.deepcopy(meta)
            current_record["aircraft"] = {}
            current_record["aircraft"]["id"] = str(current_aircraft_id)
            current_record["@timestamp"] = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            current_record["cycle"]["number"] = cycle
            current_record["sensor"] = sensor
            current_record["life"] = life
            current_record["cycle"]["left"] = cycle_left
            current_record["death_timestamp"] = death_timestamp.strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            )

            to_return.append(current_record)

    return to_return
