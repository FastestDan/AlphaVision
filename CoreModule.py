# Created by X-Corporation

import DimensionModule as dm
import ExceptionModule as em
import VisualisationModule as vm

class Ray:
    def __init__(self, cs, initpt, direction):
        self.cs = cs
        self.initpt = initpt
        self.direction = direction

    def normalize(self):
        return dm.Vector.normalize()


class Identifier:  # By Arios Jentu
    ids = list()
    i = -1

    def __init__(self, value=None):
        self.value = value

        if value is None:
            self.value = Identifier.__generate__()
            Identifier.ids.append(self.value)

    @classmethod
    def __generate__(cls):
        cls.i += 1
        while cls.i in cls.ids:
            cls.i += 1
        return cls.i

    def get_value(self):
        return self.value

    @classmethod
    def get_last_value(cls):
        return cls.ids[-1]

    def set_value(self, value):
        self.value = value


class Entity:  # By Arios Jentu

    def __init__(self, cs):
        self.__dict__["properties"] = set()
        self.set_property("cs", cs)
        self.set_property("identifier", Identifier())

    def set_property(self, prop, val):
        if prop == "properties":
            raise em.EngineException(em.EngineException.PROP_OF_PROPS_ERROR)

        self.__dict__[prop] = val
        self.__dict__["properties"].add(prop)

    def get_property(self, prop):
        if prop not in self.__dict__["properties"]:
            raise em.EngineException(em.EngineException.PROPERTY_NOT_EXIST_ERROR)

        return self.__dict__[prop]

    def remove_property(self, prop):
        if prop == "properties":
            raise em.EngineException(em.EngineException.PROP_OF_PROPS_ERROR)

        if prop not in self.__dict__["properties"]:
            raise em.EngineException(em.EngineException.PROPERTY_NOT_EXIST_ERROR)

        self.__delattr__(prop)
        self.__dict__["properties"].remove(prop)

    def __getattr__(self, item):
        return self.get_property(item)

    def __setattr__(self, item, value):
        return self.set_property(item, value)

    def is_property_exist(self, item: str):
        return item in self.__dict__["properties"]

    def __getitem__(self, item):
        return self.get_property(item)

    def __setitem__(self, item, value):
        return self.set_property(item, value)


class EntitiesList(list):
    pass

    def get(self, identifier: Identifier):
        for val in self:
            if val.identifier.get_value() == identifier.get_value():
                return val
        else:
            raise em.EngineException(em.EngineException.ENTITY_NOT_EXIST_ERROR)

    def exec(self, f, *args, **kwargs):
        for i in self:
            f(i, *args, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, Identifier):
            return self.get(item)
        super().__getitem__(item)

    def __getattr__(self, item):
        return self.__getitem__(item)


class Game:
    def __init__(self, cs, entities):
        self.cs = cs
        self.entities = entities
        self.entity_class = self.get_entity_class()
        self.ray_class = self.get_ray_class()
        self.object_class = self.get_object_class()
        self.camera_class = self.get_camera_class()
        self.hyper_plane_class = self.get_hyper_plane_class()
        self.hyper_ellipsoid_class = self.get_hyper_ellipsoid_class()

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    def get_entity_class(self):

        if hasattr(self, "entity_class") and (self.entity_class is not None):
            return self.entity_class

        class GameEntity(Entity):
            def __init__(meself):
                super().__init__(self.cs)
                self.entities.append(meself)

        return GameEntity

    def get_ray_class(self):

        if hasattr(self, "ray_class"):
            return self.ray_class

        class GameRay(Ray):
            def __init__(meself, pt, direction):
                super().__init__(self.cs, pt, direction)
                pass

        return GameRay

    def get_object_class(self):

        if hasattr(self, "object_class"):
            return self.object_class

        class GameObject(self.get_entity_class()):
            def __init__(meself, pos: dm.Point, direction: dm.Vector):
                super().__init__()
                if pos.dim() != direction.dim():
                    raise em.EngineException(em.EngineException.VEC_PT_DIM_ERROR)

                meself.dim = direction.dim()
                meself.set_position(pos)
                meself.set_direction(direction)

            def move(meself, direction: dm.Vector) -> None:
                meself.position += direction

            def planar_rotate(meself, indices: [int, int], angle: float):
                result = meself.direction * dm.Matrix.n_rotator(angle, indices, meself.dim)
                meself.set_direction(result)

            def rotate_3d(meself, angles: [float, float, float]):
                result = meself.direction * dm.Matrix.xyz_rotator(angles)
                meself.set_direction(result)

            def set_position(meself, pos: dm.Point):
                meself.set_property("position", pos)

            def set_direction(meself, direction: dm.Vector):
                meself.set_property("direction", direction)

            def intersection_distance(meself, ray: Ray):
                pass

        return GameObject

    def get_camera_class(self):

        if hasattr(self, "camera_class"):
            return self.camera_class

        class GameCamera(self.get_object_class()):
            def __init__(meself, pos, fov, drawdist, dirlook):
                super().__init__(pos, dirlook)
                # meself.set_position(pos)
                meself.set_property("fov", fov)
                meself.set_property("drawdist", drawdist)

                if isinstance(dirlook, dm.Point):
                    meself.remove_property("direction")
                    meself.set_property("look_at", dirlook)

            def planar_rotate(meself, indices: [int, int], angle: float):
                if meself.is_property_exist("look_at"):
                    raise em.EngineException(em.EngineException.NO_LOOK_ERROR)
                super().planar_rotate(angle, indices, meself.dim)

            def rotate_3d(meself, angles: [float, float, float]):
                if meself.is_property_exist("look_at"):
                    raise em.EngineException(em.EngineException.NO_LOOK_ERROR)
                super().rotate_3d(angles)

            def get_rays_matrix(meself, n, m):  # Matrix n*m {[Ray]}
                pass

        return GameCamera

    def get_hyper_plane_class(self):

        if hasattr(self, "hyper_plane_class"):
            return self.hyper_plane_class

        class GameHyperPlane(self.get_object_class()):
            def __init__(meself, position, normal):
                super().__init__(position, normal)

            def planar_rotate(meself, indices: [int, int], angle: float):
                pass

            def rotate_3d(meself, angles: [float, float, float]):
                pass

            def intersection_distance(meself, ray):
                pass

        return GameHyperPlane

    def get_hyper_ellipsoid_class(self):
        if hasattr(self, "hyper_ellipsoid_class"):
            return self.hyper_ellipsoid_class

        class GameHyperEllipsoid(self.get_hyper_plane_class()):
            def __init__(meself, position, direction):
                super().__init__(position, direction)

            def planar_rotate(meself, indices: [int, int], angle: float):
                pass

            def rotate_3d(meself, angles: [float, float, float]):
                pass

            def intersection_distance(meself, ray):
                pass

        return GameHyperEllipsoid



# if __name__ == "__main__":
#     basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
#     g1 = Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), EntitiesList())
#     NewGameRay = g1.get_ray_class()
#     ray = NewGameRay(dm.Point([0, 0, 0]), dm.Vector([0, 0, 1]))
#     print(ray.initpt)
#     print(ray.dir)
#     print(ray.cs)
#     NGen = g1.get_entity_class()
#     entity = NGen()
#     print(entity.identifier)
#     exit()


# class GameObject(GameEntity):  # Assistance required!
#     def __init__(self, pos: dm.Point, dir: dm.Vector):
#         self.pos = pos
#         self.set_property("direction", dir)
#
#     def move(self, dir: dm.Vector) -> None:
#         pass
#
#     def planer_rotate(self, indices: (int, int), angle: float):
#         pass
#
#     def rotate_3d(self, angles: (float, float, float)):
#         pass
#
#     def set_position(self, pos: dm.Point):
#         pass
#
#     def set_direction(self, dir: dm.Vector):
#         pass
#
# class GameCamera(GameObject):
#     def __init__(self, pos, dirlook, fov, drawdist):
#         self.pos = pos
#         self.fov = fov
#         self.drawdist = drawdist
#
#         if isinstance(dirlook, dm.Point):
#             self.remove_property("direction")
#             self.set_property("look_at", self.look_at)
#         else setprop("dist", dirlook)
