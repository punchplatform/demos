from project.generator.Aircraft import Aircraft
from project.generator.Airspace import Airspace
from project.generator.GeneratorI import GeneratorI
from project.generator.LinearValues import LinearValues
from project.generator.Radar import Radar
from project.generator.Usage import Usage


class GeneratorFactory:
    @staticmethod
    def GeneratorBuild(generator_type: str) -> GeneratorI:
        if generator_type == "airspace":
            return Airspace()
        elif generator_type == "radar":
            return Radar()
        elif generator_type == "aircraft":
            return Aircraft()
        elif generator_type == "usage_monitoring":
            return Usage()
        elif generator_type == "linear":
            return LinearValues()
