from project.generator.GeneratorI import GeneratorI
from project.utils.Utils import write_array_json_to_file, generate_random_radar_plots


class Radar(GeneratorI):
    def generateDataset(self, payload: dict, output: str) -> list:
        for conf in payload:
            data = generate_random_radar_plots(**conf)
            write_array_json_to_file(data, output)
