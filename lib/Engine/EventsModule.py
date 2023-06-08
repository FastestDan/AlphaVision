# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Exceptions.EngineExceptionModule as eem
import lib.Engine.VisualisationModule as vm


class EventSystem:
    def __init__(self, events: dict):
        self.events = events

    def add(self, name):
        if name not in list(self.events.keys()):
            self.events.update({name: list()})

    def remove(self, name):
        if name in list(self.events.keys()):
            self.events.pop(name)
        else:
            raise eem.EngineException("There is no name")

    def handle(self, name, function):
        if name not in self.events.keys():
            raise eem.EngineException("There is no name")

        self.events[name].append(function)

    def remove_handled(self, name, function):
        if name not in self.events.keys():
            raise eem.EngineException("There is no name")

        if function not in self.events[name]:
            raise eem.EngineException("There is no function")

        self.events[name].remove(function)

    def trigger(self, name, *args):
        if name not in self.events.keys():
            raise eem.EngineException("There is no name")

        for elem in self.events[name]:
            elem(*args)

    def get_handled(self, name):
        if name not in self.events.keys():
            raise eem.EngineException("There is no name")

        return self.events.get(name)

    def __getitem__(self, item):
        return self.get_handled(item)



