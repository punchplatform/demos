from project.generator.GeneratorI import GeneratorI
from project.utils.Utils import write_array_json_to_file, generate_linear_values


class LinearValues(GeneratorI):
    def generateDataset(self, payload: dict, output: str) -> list:
        for conf in payload:
            data = generate_linear_values(**conf)
            write_array_json_to_file(data, output)
