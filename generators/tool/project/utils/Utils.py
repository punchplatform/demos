import copy
import datetime
import json
import numpy as np
import uuid
import math
import random


def write_array_json_to_file(input_data: list(), output_path: str):
    with open(output_path, "a") as file:
        for record in input_data:
            file.write(json.dumps(record))
            file.write("\n")


def load_json_file(path):
    data = []
    file = open(path, "r")
    for line in file.readlines():
        data.append(json.loads(line))
    return data


def generate_random_radar_plots(sample_size_by_radar, radar_number, frequency_s):
    max_distance = (1000 - 10) * np.random.random(radar_number) + 10
    max_altitude = (10000 - 0) * np.random.random(radar_number) + 0

    result = []
    for radar in range(0, radar_number):

        current_max_radar_distance = max_distance[radar]
        current_max_radar_altitude = max_altitude[radar]
        degrees = (360 - 0) * np.random.random(sample_size_by_radar)
        distances = (current_max_radar_distance - 10) * np.random.random(
            sample_size_by_radar
        ) + 10

        altitudes = (current_max_radar_altitude - 0) * np.random.random(
            sample_size_by_radar
        ) + 0
        start_timestamp = datetime.datetime.utcnow()
        all_timestamp = [
            start_timestamp + datetime.timedelta(seconds=(i * frequency_s))
            for i in range(0, sample_size_by_radar)
        ]
        radar_id = uuid.uuid1()
        for degree, distance, altitude, timestamp in zip(
                degrees, distances, altitudes, all_timestamp
        ):
            plots_id = uuid.uuid1()

            result.append(
                {
                    "coord": {
                        "degree": degree,
                        "distance": distance,
                        "altitude": altitude,
                    },
                    "plots": {"id": str(plots_id)},
                    "radar": {
                        "id": str(radar_id),
                        "coverage": {
                            "distance": current_max_radar_distance,
                            "altitude": current_max_radar_altitude,
                        },
                    },
                    "@timestamp": str(timestamp),
                }
            )
    return result


def generate_random_linear_points(
        x_start, x_end, y_start, y_end, duration_h, frequency_s, aeronef_ID
):
    duration_s = duration_h * 3600
    max_track_point = int(duration_s / frequency_s)
    x_tracks = np.linspace(x_start, x_end, max_track_point)
    y_tracks = np.linspace(y_start, y_end, max_track_point)
    x_altitude = np.linspace(0, math.pi, max_track_point)
    y_altitude = [10000 * math.sin(i) for i in x_altitude]
    track_id = uuid.uuid1()
    start_timestamp = datetime.datetime.utcnow()
    all_timestamp = [
        start_timestamp + datetime.timedelta(seconds=(i * frequency_s))
        for i in range(0, max_track_point)
    ]

    return [
        {
            "@timestamp": str(timestamp),
            "aeronef": {"id": aeronef_ID},
            "coord": {"longitude": x, "latitude": y, "altitude": a},
            "plots": {"id": str(uuid.uuid1())},
            "tracks": {"id": str(track_id)},
        }
        for x, y, a, timestamp in zip(x_tracks, y_tracks, y_altitude, all_timestamp)
    ]


def generate_random_curvy_points(
        x_start, x_end, y_start, y_end, duration_h, frequency_s, aeronef_ID
):
    duration_s = duration_h * 3600
    max_track_point = int(duration_s / frequency_s)
    x_tracks = np.linspace(x_start, x_end, max_track_point)
    x_curve = np.linspace(-3, 3, max_track_point)
    y_tracks = np.linspace(y_start, y_end, max_track_point)
    y_curve = [-(x * x) + 10 for x in x_curve]
    x_altitude = np.linspace(0, math.pi, max_track_point)
    y_altitude = [10000 * math.sin(i) for i in x_altitude]
    track_id = uuid.uuid1()
    start_timestamp = datetime.datetime.utcnow()
    all_timestamp = [
        start_timestamp + datetime.timedelta(seconds=(i * frequency_s))
        for i in range(0, max_track_point)
    ]

    return [
        {
            "@timestamp": str(timestamp),
            "aeronef": {"id": aeronef_ID},
            "coord": {"longitude": x1, "latitude": y1 + y2, "altitude": a},
            "plots": {"id": str(uuid.uuid1())},
            "tracks": {"id": str(track_id)},
        }
        for x1, x2, y1, y2, a, timestamp in zip(
            x_tracks, x_curve, y_tracks, y_curve, y_altitude, all_timestamp
        )
    ]


def generate_random_shape_points(
        x_start, x_end, y_start, y_end, duration_h, frequency_s, aeronef_ID, shape="linear"
):
    if shape == "linear":
        tracks = generate_random_linear_points(
            x_start, x_end, y_start, y_end, duration_h, frequency_s, aeronef_ID
        )
    elif shape == "curvy":
        tracks = generate_random_curvy_points(
            x_start, x_end, y_start, y_end, duration_h, frequency_s, aeronef_ID
        )
    else:
        print("Unknown Shape TYPE, default linear")
        tracks = generate_random_linear_points(
            x_start, x_end, y_start, y_end, duration_h, frequency_s, aeronef_ID
        )
    return tracks


def generate_linear_aircraft_sensor_values(
        aircraft_number: int, max_cycle_number: int, cycle_schedule_s: int
) -> list():
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

        for timestamp, cycle, sensor in zip(
                all_timestamp, all_cycles, all_sensor_values
        ):
            current_record = copy.deepcopy(meta)
            current_record["aircraft"] = {}
            current_record["aircraft"]["id"] = str(current_aircraft_id)
            current_record["event_timestamp"] = timestamp.strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            )
            current_record["cycle"]["number"] = cycle
            current_record["sensor"] = sensor

            to_return.append(current_record)

    return to_return


def generate_random_tool_user(iteration_number, schedule_time_s, average_life_esperancy_s, average_flow_rate):
    all_new_users = np.random.poisson(average_flow_rate, iteration_number)
    all_users = []
    to_return = []

    for current_iteration in range(0, iteration_number):

        start_timestamp = datetime.datetime.utcnow()
        new_users = all_new_users[current_iteration]

        # Add new Users
        for i in range(0, new_users):
            current_user = {"@timestamp": start_timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                            "user": {"id": str(uuid.uuid1())},
                            "life": int(random.expovariate(1 / average_life_esperancy_s))}
            if current_user["life"] > 0:
                all_users.append(current_user.copy())
                to_return.append(current_user.copy())

        # Decrease users life counter
        for user in all_users:
            user["life"] = user["life"] - 1

            if user["life"] > 0:
                user["@timestamp"] = (datetime.datetime.strptime(user["@timestamp"],
                                                                 "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(
                    seconds=schedule_time_s)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                to_return.append(user.copy())

    return to_return
