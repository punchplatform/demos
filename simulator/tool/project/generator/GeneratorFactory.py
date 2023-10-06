import importlib
from project.generator.GeneratorI import GeneratorI


class GeneratorFactory:
    @staticmethod
    def GeneratorBuild(module: str, class_name: str) -> GeneratorI:
        dynamic_node = getattr(importlib.import_module(module), class_name)
        return dynamic_node()
