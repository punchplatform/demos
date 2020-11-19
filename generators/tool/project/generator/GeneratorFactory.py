from project.generator.Aircraft import Aircraft
from project.generator.Airspace import Airspace
from project.generator.GeneratorI import GeneratorI
from project.generator.Radar import Radar


class GeneratorFactory:
    @staticmethod
    def GeneratorBuild(generator_type: str) -> GeneratorI:
        if generator_type == "airspace":
            return Airspace()
        elif generator_type == "radar":
            return Radar()
        elif generator_type == "aircraft":
            return Aircraft()
