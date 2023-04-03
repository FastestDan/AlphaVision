import Alpha_Vision as av
import pytest


class TestsMatrix():
    def testsum(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        res = m1 + m2
        m3 = av.Matrix([[11, 13, 15], [17, 19, 21], [23, 25, 27]])
        assert res.floatlist == m3.floatlist

    def testdet(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        det = 0
        assert m1.determinant() == det

    def testinv(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(av.EngineException) as error:
            m1.inverse()
        assert "Error 3: Wrong determinant value for the inversion" in str(error.value)

    def testmul(self=None):
        m1 = av.Matrix([[1, 2, 3], [3, 2, 1]])
        m2 = av.Matrix([[4, 5], [6, 7], [8, 9]])
        m3 = av.Matrix([[40, 46], [32, 38]])
        res = m1 * m2
        assert res.floatlist == m3.floatlist

    def testzero(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(av.EngineException) as error:
            m1 / 0
        assert "Error 3: Division by zero impossible" in str(error.value)

    def testtrans(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        res = m1.transpose()
        assert res.floatlist == m2.floatlist