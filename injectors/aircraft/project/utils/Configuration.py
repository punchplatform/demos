import json


class Configuration:
    __Configuration = None

    class __Conf:
        def __init__(self, conf_file_path: str):
            self.__conf = []
            with open(conf_file_path, "r") as file:
                self.__conf = json.loads(file.read())

        def getConf(self) -> list(dict()):
            return self.__conf

    @staticmethod
    def getConfiguration():
        """ Static access method. """
        if Configuration.__Configuration == None:
            raise Exception("You must init an instance")

        return Configuration.__Configuration

    @staticmethod
    def setUp(conf_file_path: str):
        """ Virtually private constructor. """
        if Configuration.__Configuration != None:
            raise Exception("This class is already instancied")
        else:
            Configuration.__Configuration = Configuration.__Conf(conf_file_path)
