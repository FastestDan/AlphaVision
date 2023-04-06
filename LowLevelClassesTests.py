import Alpha_Vision as av
import pytest


class TestsMatrix():
    def testadd(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        res = m1 + m2
        m3 = av.Matrix([[11, 13, 15], [17, 19, 21], [23, 25, 27]])
        assert res.floatlist == m3.floatlist

    def testadderr(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        with pytest.raises(av.EngineException) as error:
            res = m1 + m2
        assert av.EngineException.AddErr in str(error.value)

    def testsub(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        res = m2 - m1
        m3 = av.Matrix([[9, 9, 9], [9, 9, 9], [9, 9, 9]])
        assert res.floatlist == m3.floatlist

    def testsuberr(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        with pytest.raises(av.EngineException) as error:
            m1 - m2
        assert av.EngineException.SubErr in str(error.value)

    def testdet(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        det = 0
        assert m1.determinant() == det

    def testinverr(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        with pytest.raises(av.EngineException) as error:
            m1.inverse()
        assert av.EngineException.InvErr in str(error.value)

    def testdetinverr(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(av.EngineException) as error:
            m1.inverse()
        assert av.EngineException.DetInvErr in str(error.value)

    def testmul(self=None):
        m1 = av.Matrix([[1, 2, 3], [3, 2, 1]])
        m2 = av.Matrix([[4, 5], [6, 7], [8, 9]])
        m3 = av.Matrix([[40, 46], [32, 38]])
        res = m1 * m2
        assert res.floatlist == m3.floatlist

    def testmulerr(self=None):
        m1 = av.Matrix([[1, 2, 3, 4], [4, 3, 2, 1]])
        m2 = av.Matrix([[4, 5], [6, 7], [8, 9]])
        with pytest.raises(av.EngineException) as error:
            m1 * m2
        assert av.EngineException.MulErr in str(error.value)

    def testzeroerr(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(av.EngineException) as error:
            m1 / 0
        assert av.EngineException.ZeroErr in str(error.value)

    def testtrans(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        res = m1.transpose()
        assert res.floatlist == m2.floatlist

    def testrot(self=None):
        m1 = av.Matrix.rotator(90, "x")
        m2 = [[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]]
        assert m1.floatlist == m2

    def testroterr(self=None):
        with pytest.raises(av.EngineException) as error:
            av.Matrix.rotator(180, "Ы")
        assert av.EngineException.AxErr in str(error.value)


class TestsVector():
    def testiniterr(self=None):
        with pytest.raises(av.EngineException) as error:
            av.Vector([[1], [2], [3, 4]])
        assert av.EngineException.InitErr in str(error.value)

    def testscal(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        res = v1.scalmul(v2)
        v12 = 32
        assert res == v12

    def testvec(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        res = v1 ** v2
        v3 = av.Vector([[-3], [6], [-3]])
        assert res.floatlist == v3.floatlist

    def testmod(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        res = v1 % v2
        v12 = 32.0
        assert res == v12


class TestsVectorSpace():
    def testiniterr(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Matrix([[4], [5], [6]])
        with pytest.raises(av.EngineException) as error:
            av.VectorSpace([v1, v2])
        assert av.EngineException.VecListErr in str(error.value)

    def testvecform(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        v3 = av.Vector([[7], [8], [9]])
        vs = av.VectorSpace([v1, v2, v3])
        pt = av.Point([[10], [11], [12]])
        res = vs.vecform(pt)
        v123 = av.Vector([[138], [171], [204]])
        assert res.floatlist == v123.floatlist
