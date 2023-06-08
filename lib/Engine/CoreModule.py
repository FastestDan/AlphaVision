# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Exceptions.EngineExceptionModule as eem
import lib.Engine.ConfigurationModule as config
import lib.Engine.EventsModule as event
import math


class Ray:
    def __init__(self, cs, initpt, direction):
        self.cs = cs
        self.initpt = initpt
        self.direction = direction

    def normalize(self):
        return self.direction.normalize()


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
            raise eem.EngineException(eem.EngineException.PROP_OF_PROPS_ERROR)

        self.__dict__[prop] = val
        self.__dict__["properties"].add(prop)

    def get_property(self, prop):
        if prop not in self.__dict__["properties"]:
            raise eem.EngineException(eem.EngineException.PROPERTY_NOT_EXIST_ERROR)

        return self.__dict__[prop]

    def remove_property(self, prop):
        if prop == "properties":
            raise eem.EngineException(eem.EngineException.PROP_OF_PROPS_ERROR)

        if prop not in self.__dict__["properties"]:
            raise eem.EngineException(eem.EngineException.PROPERTY_NOT_EXIST_ERROR)

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
            raise eem.EngineException(eem.EngineException.ENTITY_NOT_EXIST_ERROR)

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
        # self.es = es  # {}

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    # def apply_configuration(self, configuration):
    #     pass
    #
    # def get_event_system(self):
    #     return self.es.EventSystem

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
                    raise eem.EngineException(eem.EngineException.VEC_PT_DIM_ERROR)

                meself.dim = direction.dim()
                meself.set_position(pos)
                meself.set_direction(direction)

            def move(meself, direction: dm.Vector) -> None:
                meself.position += direction

            def planar_rotate(meself, indices: [int, int], angle: float):
                result = dm.Matrix.n_rotator(angle, indices, meself.dim) * meself.direction.transpose()
                meself.set_direction(result)

            def rotate_3d(meself, angles: [float, float, float]):
                result = dm.Matrix.xyz_rotator(angles) * meself.direction.transpose()
                meself.set_direction(result)

            def set_position(meself, pos: dm.Point):
                meself.set_property("position", pos)

            def set_direction(meself, direction: dm.Vector):
                meself.set_property("direction", direction)

            @classmethod
            def intersection_distance(cls, ray: Ray):
                return 0

        return GameObject

    def get_camera_class(self):

        if hasattr(self, "camera_class"):
            return self.camera_class

        class GameCamera(self.get_object_class()):
            def __init__(meself, pos, fov, drawdist, dirlook, vfov=None):
                super().__init__(pos, dirlook)
                if vfov is None:
                    # vfov = math.atan((16/9) * math.tan(math.radians(fov)/2))
                    vfov = fov
                meself.set_property("fov", math.radians(fov))
                meself.set_property("vfov", math.radians(vfov))
                meself.set_property("drawdist", drawdist)

                if isinstance(dirlook, dm.Point):
                    meself.remove_property("direction")
                    meself.set_property("look_at", dirlook)

            def planar_rotate(meself, indices: [int, int], angle: float):
                if meself.is_property_exist("look_at"):
                    raise eem.EngineException(eem.EngineException.NO_DIR_ERROR)
                super().planar_rotate(indices, angle)

            def rotate_3d(meself, angles: [float, float, float]):
                if meself.is_property_exist("look_at"):
                    raise eem.EngineException(eem.EngineException.NO_DIR_ERROR)
                super().rotate_3d(angles)

            def get_rays_matrix(meself, n, m):
                raylist = []
                alpha, beta = meself.fov, meself.vfov
                dalpha, dbeta = alpha/n, beta/m

                for i in range(0, n):
                    ai = dalpha * i - (alpha / 2)
                    helper = []

                    for j in range(0, m):
                        bi = dbeta * j - (beta / 2)

                        if meself.is_property_exist("look_at"):
                            ray = dm.Matrix.n_rotator(ai, [0, 1], 3) * dm.Matrix.n_rotator(bi, [0, 2], 3)\
                                  * meself.cs.vecspace.vector_form(meself.look_at - meself.pos).transpose()
                        else:
                            ray = dm.Matrix.n_rotator(ai, [0, 1], 3) * dm.Matrix.n_rotator(bi, [0, 2], 3)\
                                  * meself.direction.transpose()

                        helper.append(ray)
                    raylist.append(helper)

                return dm.Matrix(raylist)
                # if meself.is_property_exist("look_at"):
                #     raise eem.EngineException(eem.EngineException.NO_DIR_ERROR)
        return GameCamera

    def get_hyper_plane_class(self):

        if hasattr(self, "hyper_plane_class"):
            return self.hyper_plane_class

        class GameHyperPlane(self.get_object_class()):
            def __init__(meself, position: dm.Point, normal: dm.Vector):
                super().__init__(position, normal)

            def intersection_distance(meself, ray):
                rpt = ray.initpt  # Point   x^1 {x^1 1, x^1 2, x^1 n}

                dirvec = ray.direction  # Vector  r {delta x1, delta x2, delta xn}
                abc = meself.direction  # Vector   n {A1, A2, An}
                pos = meself.position  # Point   x^0 {x^0 1, x^0 2, x^0 n}

                if abc % dirvec == 0:
                    if abc % (rpt - pos) == 0:
                        return 0
                    else:
                        raise eem.EngineException("Parallel ray")
                else:
                    t = -(abc % (rpt - pos))/(abc % dirvec)
                    if t < 0:
                        return -1
                    else:
                        return (dirvec * t).length()

        return GameHyperPlane

    def get_hyper_ellipsoid_class(self):

        if hasattr(self, "hyper_ellipsoid_class"):
            return self.hyper_ellipsoid_class

        class GameHyperEllipsoid(self.get_object_class()):
            def __init__(meself, position: dm.Point, direction: dm.Vector, semiaxes: list[float]):
                super().__init__(position, direction)
                meself.set_property("semiaxes", semiaxes)

            def planar_rotate(meself, indices: [int, int], angle: float):
                super().planar_rotate(indices, angle)

            def rotate_3d(meself, angles: [float, float, float]):
                super().rotate_3d(angles)

            def intersection_distance(meself, ray):
                rpt = ray.initpt  # Point

                dirvec = ray.direction  # Vector
                abc = meself.direction  # Vector

                alpha = 0
                beta = 0
                gamma = 0

                for i in range(0, len(abc)):
                    alpha += (rpt[i] ** 2) / (abc[i] ** 2)
                    beta += (dirvec[i] * rpt[i]) / (abc[i] ** 2)
                    gamma += (dirvec[i] * rpt[i]) / (abc[i] ** 2)

                beta *= 2
                gamma -= 1

                disc = beta ** 2 - 4 * alpha * gamma  # float
                if disc < 0:
                    return -1

                elif disc >= 0:
                    t1 = (-beta + math.sqrt(disc)) / (2 * alpha)  # float
                    t2 = (-beta - math.sqrt(disc)) / (2 * alpha)  # float

                    v1 = dirvec * t1  # Vector
                    v2 = dirvec * t2  # Vector

                    if (t1 > 0) and (t2 > 0):
                        return min(v1.length(), v2.length())

                    elif (t1 > 0) and (t2 <= 0):
                        return v1.length()

                    elif (t1 <= 0) and (t2 < 0):
                        return v2.length()

                    else:
                        return -1

        return GameHyperEllipsoid

# alpha = (rpt[0] ** 2) / (abc[0] ** 2) + (rpt[1] ** 2) / (abc[1] ** 2) + (rpt[2] ** 2) / (
#         abc[2] ** 2)  # float
# beta = 2 * ((dirvec[0] * rpt[0]) / (abc[0] ** 2) + (dirvec[1] * rpt[1]) / (abc[1] ** 2) + (
#             dirvec[2] * rpt[2]) / (abc[2] ** 2))  # float
# gamma = (dirvec[0] ** 2)/(abc[0] ** 2) + (dirvec[1] ** 2)/(abc[1] ** 2) + (dirvec[2] ** 2)/(abc[2] ** 2) - 1 # float


# print(f"\n{alpha} {beta} {gamma}")

