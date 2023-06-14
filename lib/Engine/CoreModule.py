# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Exceptions.EngineExceptionModule as eem
import lib.Exceptions.MathExceptionModule as mem
import lib.Engine.ConfigurationModule as config
import lib.Engine.EventsModule as event
import math

PRECISION = 20

class Ray:
    def __init__(self, cs, initpt, direction):
        ep = 4
        for i in range(0, len(initpt.floatlist[0])):
            initpt.floatlist[0][i] = round(initpt.floatlist[0][i], ep)
        for i in range(0, len(direction.floatlist[0])):
            direction.floatlist[0][i] = round(direction.floatlist[0][i], ep)
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
    def __init__(self, cs, entities, es=None):
        self.cs = cs
        self.entities = entities
        self.entity_class = self.get_entity_class()
        self.ray_class = self.get_ray_class()
        self.object_class = self.get_object_class()
        self.camera_class = self.get_camera_class()
        self.hyper_plane_class = self.get_hyper_plane_class()
        self.hyper_ellipsoid_class = self.get_hyper_ellipsoid_class()
        self.es = es  # {}

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    def apply_configuration(self, cfg: config.GameConfiguration):
        self.camera_class.m, self.camera_class.n = int(list(cfg.configuration.values())[0]), int(list(cfg.configuration.values())[1])

    def get_event_system(self):
        return self.es.EventSystem

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
                dir = direction.normalize()
                meself.set_property("direction", dir)

            @classmethod
            def intersection_distance(cls, ray: Ray):
                return 0

        return GameObject

    def get_camera_class(self):

        if hasattr(self, "camera_class"):
            return self.camera_class

        class GameCamera(self.get_object_class()):
            m = None
            n = None

            def __init__(meself, pos: dm.Point, fov, drawdist, dirlook, vfov=None):
                super().__init__(pos, dirlook)
                fov = round((fov * math.pi) / 180, PRECISION)
                if vfov is None:
                    vfov = round(math.atan((int(GameCamera.m)/int(GameCamera.n)) * math.tan(fov/2)), PRECISION)
                    meself.set_property("vfov", vfov)
                else:
                    vfov = round(vfov, PRECISION)
                    meself.set_property("vfov", math.radians(vfov))
                    # vfov = fov
                meself.set_property("fov", fov)
                meself.set_property("drawdist", drawdist)
                meself.set_property("look_at", None)
                if isinstance(dirlook, dm.Point):
                    meself.set_direction(None)
                    meself.set_property("look_at", dirlook)

            def planar_rotate(meself, indices: [int, int], angle: float):
                if meself.look_at is not None:
                    raise eem.EngineException(eem.EngineException.NO_DIR_ERROR)
                super().planar_rotate(indices, angle)
                meself.set_direction(meself.direction.transpose())

            def rotate_3d(meself, angles: [float, float, float]):
                if meself.look_at is not None:
                    raise eem.EngineException(eem.EngineException.NO_DIR_ERROR)
                super().rotate_3d(angles)

            def get_rays_matrix(meself, n, m):
                result = dm.Matrix(n, m)
                if meself.direction is not None:

                    alpha, beta = meself.fov, meself.vfov
                    dalpha, dbeta = alpha / n, beta / m
                    vec = meself.direction

                    for i in range(n):
                        for j in range(m):
                            temp_vec = dm.Vector(vec.floatlist)
                            temp_vec = temp_vec.n_rotator(dalpha * i - alpha / 2, [0, 1], temp_vec.n) * temp_vec.transpose()
                            temp_vec = temp_vec.n_rotator(dbeta * j - beta / 2, [0, 2], temp_vec.m) * temp_vec
                            if (vec % temp_vec) == 0:
                                raise mem.MathException(mem.MathException.ZERO_ERROR)
                            temp_vec = (temp_vec * (vec.length() ** 2 / (vec % temp_vec)))
                            result.floatlist[i][j] = Ray(meself.cs, meself.position, temp_vec.transpose())

                    return result

                if meself.look_at is not None:
                    look_at_vec = dm.Vector(meself.look_at.floatlist)
                    position_vec = dm.Vector(meself.position.floatlist)

                    vec = (look_at_vec - position_vec).normalize()

                    alpha, beta = meself.fov, meself.vfov
                    dalpha, dbeta = alpha / n, beta / m

                    for i in range(n):
                        for j in range(m):
                            temp_vec = vec.copy()
                            temp_vec = temp_vec.n_rotator(dalpha * i - alpha / 2, [0, 1], temp_vec.n) * temp_vec.transpose()
                            temp_vec = temp_vec.n_rotator(dbeta * j - beta / 2, [0, 2], temp_vec.m) * temp_vec
                            if (vec % temp_vec) == 0:
                                raise mem.MathException(mem.MathException.ZERO_ERROR)
                            temp_vec = (temp_vec * (vec.length() ** 2 / (vec % temp_vec)))
                            temp_vec = dm.Vector(temp_vec.floatlist)
                            result[i][j] = Ray(meself.cs, meself.position, temp_vec)

                    return result

        return GameCamera

    def get_hyper_plane_class(self):

        if hasattr(self, "hyper_plane_class"):
            return self.hyper_plane_class

        class GameHyperPlane(self.get_object_class()):
            def __init__(meself, position: dm.Point, normal: dm.Vector):
                super().__init__(position, normal)

            def intersection_distance(meself, ray):
                rpt = dm.Point(ray.initpt.floatlist)  # Point   x^1 {x^1 1, x^1 2, x^1 n}

                dirvec = dm.Vector(ray.direction.floatlist)  # Vector  r {delta x1, delta x2, delta xn}
                abc = dm.Vector(meself.direction.floatlist)  # Vector   n {A1, A2, An}
                pos = dm.Point(meself.position.floatlist)  # Point   x^0 {x^0 1, x^0 2, x^0 n}

                if abc % dirvec == 0:
                    if abc % (rpt - pos) == 0:
                        return 0
                    else:
                        raise eem.EngineException("Parallel ray")
                else:
                    t = -(abc % (rpt - pos))/(abc % dirvec)
                    if t <= 0:
                        return 0
                    else:
                        return round(((rpt + dirvec) * t).length(), PRECISION) / 2

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
                pos = meself.position
                dirvec = ray.direction  # Vector
                abc = meself.direction  # Vector

                alpha = 0
                beta = 0
                gamma = 0
                delta = 0

                for i in range(0, len(abc.floatlist[0])):
                    alpha += dirvec[i] ** 2
                    beta += dirvec[i] * (rpt[i] - pos[i])
                    gamma += (rpt[i] - pos[i]) ** 2
                    delta += meself.semiaxes[i] ** 2

                beta *= 2
                gamma -= delta

                disc = beta ** 2 - 4 * alpha * gamma  # float
                if disc < 0:
                    return 0

                elif disc >= 0:
                    t1 = (-beta - math.sqrt(disc)) / (2 * alpha)  # float
                    t2 = (-beta + math.sqrt(disc)) / (2 * alpha)  # float

                    if t1 < 0:
                        if t2 < 0:
                            return 0
                        return t2
                    if t2 < 0:
                        return t1
                    return round(min(t1, t2), PRECISION)

        return GameHyperEllipsoid
