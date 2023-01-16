import json


DATA_FOLDER_PATH = "data"
CONFIG_FOLDER_PATH = f"{DATA_FOLDER_PATH}/configs"


class JSONDAO:
    """
    Generic class for loading data json files
    related to PokeBot
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = json.load(open(file_path))

    def save(self):
        with open(self.file_path, "w") as jsonfile:
            json.dump(self.data, jsonfile, indent=2)


class ConfigDAO(JSONDAO):
    """
    Generic class for loading config json files
    related to PokeBot
    """
    def __init__(self, file_name):
        super().__init__(f"{CONFIG_FOLDER_PATH}/{file_name}")


class DataDAO(JSONDAO):
    """
    Generic class for loading data json files
    related to PokeBot
    """
    def __init__(self, file_name):
        super().__init__(f"{DATA_FOLDER_PATH}/{file_name}")
