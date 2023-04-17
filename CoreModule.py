# Created by X-Corporation

import namespace as namespace
import random
import DimensionModule as dm


class Ray:
    def __init__(self, cs, initpt, dir):
        self.cs = cs
        self.initpt = initpt
        self.dir = dir


class Identifier:
    ids = list()

    def __init__(self):
        v = Identifier.__generate__
        Identifier.ids.append(v)

    @staticmethod
    def __generate__():
        return random.random()


class Entity:
    def __init__(self, cs):
        self.cs = cs
        self.id = Identifier()
        self.properties = {}

    def set_property(self, prop, val):
        self.properties[prop] = val

    def get_property(self, prop):
        return self.properties.get(prop)

    def remove_property(self, prop):
        self.properties.pop(prop)

    def __getattr__(self, item):
        return self.get_property(item)

    def __getitem__(self, item):
        return self.get_property(item)


class EntitiesList(list):
    def __init__(self, enlist):
        self.entities = enlist

    def append(self, entity: Entity) -> None:
        super().append(entity)

    def remove(self, entity) -> None:
        super().remove(entity)

    def get(self, id: Identifier):
        pass

    def exec(self, f):
        pass

    def __getitem__(self, id):
        return self.get(id)


class Game:
    def __init__(self, cs, entities: EntitiesList):
        self.cs = cs
        self.entities = entities

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    def get_entity_class(self):
        class GameEntity(Entity):
            def __init__(meself):
                super().__init__(self.cs)
                self.entities.append(meself)
        return GameEntity

    def get_entity_ray(self):
        class GameRay(Ray):
            def __init__(meself):
                super.__init__(self.cs)
                pass
        return GameRay


class GameObject(GameEntity):
    def __init__(self, pos: dm.Point, dir: dm.Vector):
        self.pos = pos
        self.dir = dir

    def move(self, dir: dm.Vector) -> None:
        pass

    def planer_rotate(self, indices: (int, int), angle: float):
        pass

    def rotate_3d(self, angles: (float, float, float)):
        pass

    def set_position(self, pos: dm.Point):
        pass

    def set_direction(self, dir: dm.Vector):
        pass


class GameCamera(GameObject):
    def __init__(self, pos, dirlook, fov, drawlist):
        self.pos = pos
        self.fov = fov
        self.drawlist = drawlist
        if isinstance(dirlook, dm.Point):
            self.look_at = dirlook
            pass
        else:
            self.dir = dirlook
