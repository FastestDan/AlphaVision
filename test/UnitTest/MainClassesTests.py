import math

import lib.Math.DimensionModule as dm
import lib.Engine.CoreModule as cm
import lib.Exceptions.EngineExceptionModule as em
import lib.Engine.EventsModule as es
import pytest


class TestsEntity:
    def test_get_property_error(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        entity = cm.Entity(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis))  # id = 0
        prop = "Power Up"

        with pytest.raises(em.EngineException):
            res = entity.prop

    def test_remove_property_error(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        entity = cm.Entity(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis))  # id = 1
        prop = "Power Up"

        with pytest.raises(em.EngineException):
            entity.remove_property(prop)


class TestsEntitiesList:
    def test_get_entity_error(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        cs0 = dm.CoordinateSystem(dm.Point([0, 0, 0]), basis)
        cs1 = dm.CoordinateSystem(dm.Point([1, 1, 1]), basis)

        entity1 = cm.Entity(cs0)  # id = 2
        entity2 = cm.Entity(cs1)  # id = 3
        enlist = cm.EntitiesList()
        enlist.append(entity1)

        with pytest.raises(em.EngineException):
            enlist.get(cm.Identifier(4))

    def test_exec(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        cs0 = dm.CoordinateSystem(dm.Point([0, 0, 0]), basis)
        cs1 = dm.CoordinateSystem(dm.Point([1, 1, 1]), basis)
        entity1 = cm.Entity(cs0)  # id = 4
        entity2 = cm.Entity(cs1)  # id = 5

        enlist = cm.EntitiesList()

        enlist.append(entity1)
        enlist.append(entity2)
        prop = "Power Up"
        val = "That DAMN 4th Chaos Emerald"

        enlist.exec(cm.Entity.set_property, prop, val)

        res = "That DAMN 4th Chaos Emerald"

        assert entity1.get_property(prop) == res
        assert entity2.get_property(prop) == res


class TestsGameObject:
    def test_move(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_object_class()
        gobject = go_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]))
        vec = dm.Vector([5, 4, 3])
        gobject.move(vec)

        res = dm.Point([6, 5, 4])

        assert gobject.position == res

    def test_planar_rotate(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_object_class()
        gobject = go_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]))
        gobject.planar_rotate([0, 1], 90.0)

        res = dm.Vector([[-1.0], [2.0], [0.0]])

        assert gobject.direction == res

    def test_rotate_3d(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_object_class()
        gobject = go_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]))
        gobject.rotate_3d([90.0, 0, 90.0])

        res = dm.Vector([[-1.0], [0.0], [2.0]])

        assert gobject.direction == res


class TestsGameCamera:
    def test_init_direction(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_camera_class()
        gobject = go_class(dm.Point([1, 1, 1]), 90.0, 50.0, dm.Vector([2, 1, 0]))

        res = True

        assert gobject.is_property_exist("direction") == res

    def test_init_look_at(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_camera_class()
        gobject = go_class(dm.Point([1, 1, 1]), 90.0, 50.0, dm.Point([2, 1, 0]))

        res = False

        assert gobject.is_property_exist("direction") == res

    def test_planar_rotate_error(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_camera_class()
        gobject = go_class(dm.Point([1, 1, 1]), 90.0, 50.0, dm.Point([2, 1, 0]))

        with pytest.raises(em.EngineException):
            gobject.planar_rotate([0, 1], 90.0)

    def test_rotate_3d_error(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_camera_class()
        gobject = go_class(dm.Point([1, 1, 1]), 90.0, 50.0, dm.Point([2, 1, 0]))

        with pytest.raises(em.EngineException):
            gobject.rotate_3d([90.0, 0, 90.0])

    def test_get_rays_matrix(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        go_class = g.get_camera_class()
        gobject = go_class(dm.Point([1, 1, 1]), 90.0, 50.0, dm.Vector([1, 1, 1]))

        camray = gobject.get_rays_matrix(3, 3)

        res = dm.Matrix([[dm.Vector([[0.99982], [0.98639], [1.01362]]), dm.Vector([[1.00904], [0.98626], [1.00456]]), dm.Vector([[1.01818], [0.98614], [0.99542]])],
                        [dm.Vector([[0.99076], [0.99548], [1.01362]]), dm.Vector([[0.99998], [0.99544], [1.00456]]), dm.Vector([[1.00912], [0.9954], [0.99542]])],
                        [dm.Vector([[0.98162], [1.0045], [1.01362]]), dm.Vector([[0.99084], [1.00454], [1.00456]]), dm.Vector([[0.99998], [1.00458], [0.99542]])]])

        assert res == camray


class TestsGameHyperPlane:
    def test_intersection(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        ghyper_class = g.get_hyper_plane_class()
        hyper = ghyper_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]))
        ray = cm.Ray(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), dm.Point([2, 2, 2]), dm.Vector([-1, -1, -1]))

        res = math.sqrt(3)

        assert hyper.intersection_distance(ray) == res

    def test_intersection_parallel(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        ghyper_class = g.get_hyper_plane_class()
        hyper = ghyper_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]))
        ray = cm.Ray(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), dm.Point([2, 2, 2]), dm.Vector([0, 0, 0]))

        with pytest.raises(em.EngineException):
            hyper.intersection_distance(ray)


class TestsGameHyperEllipsoid:
    def test_intersection(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        ghyper_class = g.get_hyper_ellipsoid_class()
        hyper = ghyper_class(dm.Point([1, 1, 1]), dm.Vector([1, 1, 1]), [1, 1, 1])
        ray = cm.Ray(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), dm.Point([1, 1, 1]), dm.Vector([1, 1, 1]))

        res = math.sqrt(3)

        assert res == hyper.intersection_distance(ray)

    def test_planar_rotate(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        ghyper_class = g.get_hyper_ellipsoid_class()
        hyper = ghyper_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]), [2, 1, 0])

        hyper.planar_rotate([0, 1], 90.0)

        res = dm.Vector([[-1.0], [2.0], [0.0]])

        assert hyper.direction == res

    def test_3d_rotate(self=None):
        basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
        g = cm.Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList(), es.EventSystem(dict({})))
        ghyper_class = g.get_hyper_ellipsoid_class()
        hyper = ghyper_class(dm.Point([1, 1, 1]), dm.Vector([2, 1, 0]), [2, 1, 0])
        hyper.rotate_3d([90.0, 0, 90.0])

        res = dm.Vector([[-1.0], [0.0], [2.0]])

        assert res == hyper.direction
