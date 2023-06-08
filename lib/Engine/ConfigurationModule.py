# Created by X-Corporation

import lib.Exceptions.EngineExceptionModule as eem


class GameConfiguration:
    def __init__(self, filepath=None):
        if filepath is None or filepath == "":
            self.filepath = None
            file = open("config/default.txt", "r")
        else:
            self.filepath = filepath
            file = open(self.filepath, "r")
        # print(os.path.abspath("config/default.txt"))
        self.configuration = dict()
        a = file.readlines()
        for elem in a:
            self.configuration[elem.split(': ')[0]] = (elem.split(': ')[1]).split('\n')[0]
            # print(f"{elem.split(': ')[0]}: {elem.split(': ')[1]}")
        file.close()

    def set_variable(self, var, value=None):
        self.configuration.update({var: value})

    def get_variable(self, var):
        return self.configuration.get(var)

    def execute_file(self, filepath):
        if filepath is None:
            raise eem.EngineException("Can't load: No file")

        a = filepath
        try:
            file = open(a, "r")
            for elem in file.readlines():
                self.configuration[elem.split(': ')[0]] = (elem.split(': ')[1]).split('\n')[0]
            file.close()
        except Exception:
            raise eem.EngineException("Can't load: File doesn't exist")

    def save(self, filepath=None):
        if (filepath is None) and (self.filepath is None):
            raise eem.EngineException("Can't save: No file")

        if filepath is not None:
            a = filepath
        else:
            a = self.filepath
        try:
            file = open(a, "w")
            for key in self.configuration.keys():
                file.write(f"{key}: {self.configuration[key]}\n")
            file.close()
        except Exception:
            raise eem.EngineException("Can't save: File doesn't exist")

    def __getitem__(self, item):
        return self.get_variable(item)

    def __setitem__(self, key, value):
        self.set_variable(key, value)