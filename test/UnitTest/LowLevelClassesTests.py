import lib.Math.DimensionModule as av
import lib.Exceptions.MathExceptionModule as mem
import pytest


class TestsMatrix:
    def test_init_zero_nn(self=None):
        m1 = av.Matrix(3)

        res = av.Matrix([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

        assert res == m1

    def test_init_zero_nm(self=None):
        m1 = av.Matrix(2, 3)

        res = av.Matrix([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

        assert res == m1

    def test_addition(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        m3 = av.Matrix([[11, 13, 15], [17, 19, 21], [23, 25, 27]])

        res = m1 + m2

        assert res == m3

    def test_addition_error(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])

        with pytest.raises(mem.MathException):
            m1 + m2

    def test_subtraction(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        m3 = av.Matrix([[9, 9, 9], [9, 9, 9], [9, 9, 9]])

        res = m2 - m1

        assert res == m3

    def test_subtraction_error(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        m2 = av.Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])

        with pytest.raises(mem.MathException):
            m1 - m2

    def test_determinant(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        det = 0

        assert m1.determinant() == det

    def test_inversion_error(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

        with pytest.raises(mem.MathException):
            m1.inverse()

    def test_determinant_for_inversion_error(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        with pytest.raises(mem.MathException):
            m1.inverse()

    def test_multiplication(self=None):
        m1 = av.Matrix([[1, 2, 3], [3, 2, 1]])
        m2 = av.Matrix([[4, 5], [6, 7], [8, 9]])
        m3 = av.Matrix([[40, 46], [32, 38]])

        res = m1 * m2

        assert res == m3

    def test_multiplication_error(self=None):
        m1 = av.Matrix([[1, 2, 3, 4], [4, 3, 2, 1]])
        m2 = av.Matrix([[4, 5], [6, 7], [8, 9]])

        with pytest.raises(mem.MathException):
            m1 * m2

    def test_zero_error(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        with pytest.raises(mem.MathException):
            m1 / 0

    def test_transposition(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = av.Matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]])

        res = m1.transpose()

        assert res.floatlist == m2.floatlist

    def test_n_rotator(self=None):
        m1 = av.Matrix.n_rotator(90, [1, 2], 3)
        m2 = av.Matrix([[1.0, 0.0, 0.0],
                        [0.0, 0.0, -1.0],
                        [0.0, 1.0, 0.0]])
        assert m1 == m2

    def test_n_rotator_index_error(self=None):
        with pytest.raises(mem.MathException):
            av.Matrix.n_rotator(90, "ЫЫЫ", 2)

    def test_n_rotator_size_error(self=None):
        with pytest.raises(mem.MathException):
            av.Matrix.n_rotator(90, [1, 2], 1)

    def test_minor(self=None):
        m1 = av.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        minor = m1.minor([0], [0])

        m2 = av.Matrix([[5, 6], [8, 9]])

        assert m2 == minor

    def test_gram(self=None):
        v1 = av.Vector([[1], [0], [0]])
        v2 = av.Vector([[0], [1], [0]])
        v3 = av.Vector([[0], [0], [1]])
        m1 = av.Matrix.gram([v1, v2, v3])

        m2 = av.Matrix([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

        assert m1 == m2

    def test_gram_error_vector_list(self=None):
        v1 = av.Matrix([[1], [0], [0]])
        v2 = av.Vector([[0], [1], [0]])
        v3 = av.Vector([[0], [0], [1]])

        with pytest.raises(mem.MathException):
            av.Matrix.gram([v1, v2, v3])

    def test_gram_error_vector_size(self=None):
        v1 = av.Vector([[1], [0]])
        v2 = av.Vector([[0], [1], [0]])
        v3 = av.Vector([[0], [0], [1]])

        with pytest.raises(mem.MathException):
            av.Matrix.gram([v1, v2, v3])


class TestsVector:
    def test_init_error(self=None):
        with pytest.raises(mem.MathException):
            av.Vector([[1], [2], [3, 4]])

    def test_init_states(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([1, 2, 3])

        res1 = True
        res2 = False

        assert v1.is_column == res1
        assert v2.is_column == res2

    def test_init_zero(self=None):
        v1 = av.Vector(3)

        res = av.Vector([0, 0, 0])

        assert res == v1

    def test_scalar_product_rows(self=None):
        v1 = av.Vector([1, 2, 3])
        v2 = av.Vector([4, 5, 6])
        v12 = 32.0

        res = v1 % v2

        assert res == v12

    def test_scalar_product_columns(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        v12 = 32.0

        res = v1 % v2

        assert res == v12

    def test_vector_product(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        v3 = av.Vector([[-3], [6], [-3]])

        res = v1 ** v2

        assert res == v3


class TestsVectorSpace:
    def test_init_err(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Matrix([[4], [5], [6]])

        with pytest.raises(mem.MathException):
            av.VectorSpace([v1, v2])

    def test_vector_form(self=None):
        v1 = av.Vector([[1], [2], [3]])
        v2 = av.Vector([[4], [5], [6]])
        v3 = av.Vector([[7], [8], [9]])
        vs = av.VectorSpace([v1, v2, v3])
        pt = av.Point([[10], [11], [12]])
        v123 = av.Vector([[138], [171], [204]])

        res = vs.vector_form(pt)

        assert res == v123

    def test_scalar_product(self=None):
        v1 = av.Vector([[1], [0], [0]])
        v2 = av.Vector([[0], [1], [0]])
        v3 = av.Vector([[0], [0], [1]])
        vs = av.VectorSpace([v1, v2, v3])
        v01 = av.Vector([[1], [0], [1]])
        v02 = av.Vector([[1], [1], [0]])
        vs0 = vs.scalar_product(v01, v02)

        res = av.Matrix([[1.0]])

        assert vs0 == res


class TestsPoint:
    def test_addition(self=None):
        p = av.Point([[1], [2], [3]])
        v = av.Vector([[4], [5], [6]])
        pv = p + v

        res = av.Point([[5], [7], [9]])

        assert pv.floatlist == res.floatlist
        assert isinstance(pv, av.Point) is True

    def test_subtraction(self=None):
        v = av.Vector([[1], [2], [3]])
        p = av.Point([[4], [5], [6]])
        pv = p - v

        res = av.Point([[3], [3], [3]])

        assert pv.floatlist == res.floatlist
        assert isinstance(pv, av.Point) is True
