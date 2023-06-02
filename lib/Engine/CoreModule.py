# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Exceptions.EngineExceptionModule as eem
import lib.Engine.VisualisationModule as vm
import math

PRECISION = 3


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
                # k = ((meself.direction.length()) ** 2) / (ray.direction % meself.direction)
                # projection = k * ray.direction
                # return projection.length()

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
                            ray = dm.Matrix.n_rotator([0, 1], ai, 3) * dm.Matrix.n_rotator([0, 2], bi, 3)\
                                  * meself.look_at
                        else:
                            ray = dm.Matrix.n_rotator([0, 1], ai, 3) * dm.Matrix.n_rotator([0, 2], bi, 3)\
                                  * meself.direction
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

                # d = -abc[0] * pos[0] - abc[1] * pos[1] - abc[2] * pos[2] # int
                # mat_m = dm.Matrix([[abc[0], abc[1], abc[2]], [1/dirvec[0], -1/dirvec[1], 0], [1/dirvec[0], 0, -1/dirvec[2]]])  # Matrix
                #
                # if mat_m.determinant() == 0:
                #     if (abc[0] * rpt[0] + abc[1] * rpt[1] + abc[2] * rpt[2]) == -d:
                #         return 0
                #     else:
                #         raise eem.EngineException("Parallel ray")
                #
                # elif mat_m.determinant() != 0:
                #
                #     m_tam = mat_m.inverse()  # Matrix
                #     lpt = dm.Vector([-d, ((pos[0]/dirvec[0]) - (pos[1]/dirvec[1])), ((pos[0]/dirvec[0]) - (pos[2]/dirvec[2]))])  # Vector
                #     xyz = m_tam * lpt  # Vector
                #     v = xyz - rpt  # Vector
                #
                #     if (dirvec[0]/v[0]) > 0:
                #         return v.length()
                #     else:
                #         return -1  # Negative direction

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

                alpha = (dirvec[0] ** 2)/(abc[0] ** 2) + (dirvec[1] ** 2)/(abc[1] ** 2) + (dirvec[2] ** 2)/(abc[2] ** 2)  # float
                beta = 2 * ((dirvec[0] * rpt[0])/(abc[0] ** 2) + (dirvec[1] * rpt[1])/(abc[1] ** 2) + (dirvec[2] * rpt[2])/(abc[2] ** 2))  # float
                gamma = (rpt[0] ** 2)/(abc[0] ** 2) + (rpt[1] ** 2)/(abc[1] ** 2) + (rpt[2] ** 2)/(abc[2] ** 2)  # float

                # print(f"\n{alpha} {beta} {gamma}")

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
                #
                # if disc == 0:
                #     t = -beta/(2 * alpha)  # float
                #
                #     xyz = dirvec*t + rpt #dm.Vector([dirvec[0] * t + rpt[0], dirvec[1] * t + rpt[1], dirvec[2] * t + rpt[2]])
                #
                #     v = xyz - rpt  # Vector  <==> v = dirvec * t
                #
                #     if t > 0:
                #     # if (dirvec[0] / v[0]) > 0:
                #         return v.length()
                #     else:
                #         return -1  # Negative direction
                #     # return t

        return GameHyperEllipsoid
