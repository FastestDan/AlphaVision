# Created by X-Corporation
import math


class EngineException(Exception):
    # Code 0: Wrong input data
    INIT_ERROR = "Error 0: Wrong initialization data"
    VECTOR_LIST_ERROR = "Error 0: Non-vector instance in the list of vectors"

    # Code 1: Wrong matrix size
    ADDITION_ERROR = "Error 1: Wrong matrix size for addition"
    SUBTRACTION_ERROR = "Error 1: Wrong matrix size for subtraction"
    MULTIPLICATION_ERROR = "Error 1: Wrong matrix size for multiplication"
    DIVISION_ERROR = "Error 1: Wrong matrix size for division"
    DETERMINANT_ERROR = "Error 1: Wrong matrix size for determinant to be found"
    INVERSION_ERROR = "Error 1: Wrong matrix size for the inversion"

    # Code 2: Wrong vector size
    SCALAR_PRODUCT_ERROR = "Error 2: Wrong vector size for scalar product"
    VECTOR_PRODUCT_ERROR = "Error 2: Wrong vector size for vector product"
    DIFFERENCE_ERROR = "Error 2: Different size of vectors in a list of vectors"

    # Code 3: Wrong values
    ZERO_ERROR = "Error 3: Division by zero impossible"
    INVERSION_DETERMINANT_ERROR = "Error 3: Wrong determinant value for the inversion"
    VECTOR_LIST_SIZE_ERROR = "Error 3: Wrong size of list of vectors"
    INDEX_ERROR = "Error 3: Wrong indexes"
    ROTATOR_SIZE_ERROR = "Error 3: Wrong value for the size of the rotation matrix"
    STATE_ERROR = "Error 3: Vector states are not the same"
    ANGLE_ERROR = "Error 3: Wrong angle values"

    # Code 4: Wrong operators
    POINT_SUBTRACTION_ERROR = "Error 4: Point can not be subtracted"
    POINT_MULTIPLICATION_ERROR = "Error 4: Point can not be a multiplier"
    POINT_DIVISION_ERROR = "Error 4: Point can not be a part of division"


class Matrix:
    ep = 5

    def __init__(self, val, val2=None):
        if val2 is not None:

            if not(isinstance(val2, int)) or not(isinstance(val, int)):
                raise EngineException(EngineException.INIT_ERROR)

            if val2 == 0 or val == 0:
                raise EngineException(EngineException.INIT_ERROR)

            self.floatlist = []
            for i in range(0, val):
                line = []
                for j in range(0, val2):
                    line.append(0.0)
                self.floatlist.append(line)
            self.m = val
            self.n = val2

        elif isinstance(val, int):
            if val == 0:
                raise EngineException(EngineException.INIT_ERROR)

            self.floatlist = []
            for i in range(0, val):
                line = []
                for j in range(0, val):
                    line.append(0.0)
                self.floatlist.append(line)
            self.m = val
            self.n = val

        elif isinstance(val, list):
            self.floatlist = val
            self.m = len(val)
            n = len(val[0])
            for i in range(0, self.m):
                if len(val[i]) != n:
                    raise EngineException(EngineException.INIT_ERROR)

                for j in range(0, n):
                    if isinstance(val[i][j], float):
                        val[i][j] = round(val[i][j], self.ep)

                n = len(val[i])
            self.n = n

        else:
            raise EngineException(EngineException.INIT_ERROR)

    def __add__(self, mat):
        return self.addition(mat)

    def __radd__(self, mat):
        return self.addition(mat)

    def __sub__(self, mat):
        return self.subtraction(mat)

    def __mul__(self, elem):
        return self.multiplication(elem)

    def __truediv__(self, elem):
        return self.division(elem)

    def __eq__(self, elem):
        return self.floatlist == elem.floatlist

    def addition(self, mat):
        if isinstance(mat, (int, float)) and mat == 0:
            mat = Matrix(self.m, self.n)

        if (self.m != mat.m) or (self.n != mat.n):
            raise EngineException(EngineException.ADDITION_ERROR)

        for i in range(0, self.m):
            for j in range(0, self.n):
                self.floatlist[i][j] += mat.floatlist[i][j]
        return self

    def subtraction(self, mat):
        if isinstance(mat, Point):
            raise EngineException(EngineException.POINT_SUBTRACTION_ERROR)

        if (self.m != mat.m) or (self.n != mat.n):
            raise EngineException(EngineException.SUBTRACTION_ERROR)

        return self + (mat * -1)

    def multiplication(self, elem):
        if isinstance(elem, Point):
            raise EngineException(EngineException.POINT_MULTIPLICATION_ERROR)

        if isinstance(elem, Matrix):
            if self.n != elem.m:
                raise EngineException(EngineException.MULTIPLICATION_ERROR)

            mat = list()
            line = list()
            count1 = 0
            count2 = 0
            while count1 < self.m:
                num = 0
                for j in range(0, elem.m):
                    num += self.floatlist[count1][j] * elem.floatlist[j][count2]
                line.append(num)
                count2 += 1
                if count2 == elem.n:
                    count1 += 1
                    count2 = 0
                    mat.append(line)
                    line = list()
            return Matrix(mat)

        else:
            for i in range(0, self.m):
                for j in range(0, self.n):
                    self.floatlist[i][j] *= elem
                    self.floatlist[i][j] = round(self.floatlist[i][j], self.ep)
            return self

    def division(self, elem):
        if isinstance(elem, Point):
            raise EngineException(EngineException.POINT_DIVISION_ERROR)

        if isinstance(elem, Matrix):
            mele = elem.inverse()
            if self.n != mele.m:
                raise EngineException(EngineException.DIVISION_ERROR)

            return mele * self

        else:
            if elem == 0:
                raise EngineException(EngineException.ZERO_ERROR)

            return self * (1 / elem)

    def minor(self, linelist, columnlist):
        mat2 = list()
        for i in range(0, self.m):
            if i in linelist:
                continue
            line2 = list()
            for j in range(0, self.m):
                if j in columnlist:
                    continue
                line2.append(self.floatlist[i][j])
            mat2.append(line2)
        return Matrix(mat2)

    def determinant(self):  # By Arios Jentu
        if self.m != self.n:
            raise EngineException(EngineException.DETERMINANT_ERROR)

        size = self.n
        if size == 1:
            return self.floatlist[0][0]

        res = 0
        for i in range(size):
            minor = self.minor([0], [i])
            minordet = minor.determinant()
            res += self.floatlist[0][i] * ((-1) ** i) * minordet

        return res

    def inverse(self):
        if self.m != self.n:
            raise EngineException(EngineException.INVERSION_ERROR)

        det = self.determinant()

        if det == 0:
            raise EngineException(EngineException.INVERSION_DETERMINANT_ERROR)

        matf = list()
        if self.m == 2:
            matf = [[self.floatlist[1][1], self.floatlist[1][0]], [self.floatlist[0][1], self.floatlist[0][0]]]

        else:
            line1 = list()
            count1 = 0
            count2 = 0
            while count1 < self.m:
                mat2 = self.minor([count1], [count2])
                elem = mat2.determinant()
                line1.append(elem)
                count2 += 1
                if count2 >= self.m:
                    count2 = 0
                    count1 += 1
                    matf.append(line1)
                    line1 = list()
        res = Matrix(matf).transpose()
        res *= (1 / det)
        return res

    def transpose(self):
        mat = list()
        for i in range(0, self.n):
            line = list()
            for j in range(0, self.m):
                line.append(self.floatlist[j][i])
            mat.append(line)
        if isinstance(self, Vector):
            return Vector(mat)
        else:
            return Matrix(mat)

    @staticmethod
    def identity(n):
        mat = list()
        for i in range(0, n):
            line = list()
            for j in range(0, n):
                if i == j:
                    line.append(1.0)
                else:
                    line.append(0.0)
            mat.append(line)
        return Matrix(mat)

    @staticmethod
    def gram(veclist):
        prevn = None
        prevm = None

        for i in range(0, len(veclist)):
            if not isinstance(veclist[i], Vector) or isinstance(veclist[i], Point):
                raise EngineException(EngineException.VECTOR_LIST_ERROR)

            mv = veclist[i].m
            nv = veclist[i].n
            if prevm is None:
                prevm = mv
                prevn = nv
                continue
            elif (prevm != mv) or (prevn != nv):
                raise EngineException(EngineException.DIFFERENCE_ERROR)

        mat = list()
        count = 0
        for i in range(0, len(veclist)):
            res = list()
            for j in range(0, len(veclist)):
                res.append(veclist[i] % veclist[j])
            count += 1
            mat.append(res)
        return Matrix(mat)

    @staticmethod
    def n_rotator(angle, indexes: [int, int], n):
        if not(isinstance(indexes, list)) or len(indexes) != 2:
            raise EngineException(EngineException.INDEX_ERROR)

        if indexes[0] == indexes[1]:
            raise EngineException(EngineException.INDEX_ERROR)

        if n < 2:
            raise EngineException(EngineException.ROTATOR_SIZE_ERROR)

        m1 = Matrix.identity(n).floatlist
        i, j = indexes[0], indexes[1]

        m1[i][i] = math.cos(math.radians(angle))
        m1[j][j] = math.cos(math.radians(angle))
        m1[i][j] = math.sin(math.radians(angle)) * ((-1) ** (i + j))
        m1[j][i] = math.sin(math.radians(angle)) * ((-1) ** (i + j + 1))
        res = Matrix(m1)
        if i > j:
            res = res.transpose()
        return res

    @staticmethod
    def xyz_rotator(angles: [float, float, float]):
        if not isinstance(angles, list):
            raise EngineException(EngineException.ANGLE_ERROR)

        if len(angles) > 3:
            raise EngineException(EngineException.ANGLE_ERROR)

        while len(angles) < 3:
            angles.append(0.0)

        return Matrix.n_rotator(angles[0], [1, 2], 3) * \
               Matrix.n_rotator(angles[1], [0, 2], 3) * \
               Matrix.n_rotator(angles[2], [0, 1], 3)


class Vector(Matrix):
    def __init__(self, val):
        if isinstance(val, list):
            if isinstance(val[0], list):

                super().__init__(val)
            else:

                temp = list()
                temp.append(val)
                super().__init__(temp)

        elif isinstance(val, int):
            temp1 = list()
            temp2 = list()
            for i in range(0, val):
                temp2.append(0.0)
            temp1.append(temp2)
            super().__init__(temp1)

        else:
            raise EngineException(EngineException.INIT_ERROR)

        self.is_column = len(self.floatlist[0]) == 1

    def scalar_product(self, vec):
        v2 = self
        if not self.is_column:
            v2 = self.transpose()
        return BilinearForm(Matrix.identity(v2.m), v2, vec)

    def vector_product(self, vec):
        if self.is_column != vec.is_column:
            raise EngineException(EngineException.STATE_ERROR)

        v1 = self
        v2 = vec
        if self.is_column:
            v1 = v1.transpose()
            v2 = v2.transpose()

        if not((v1.m == 1 and v1.n == 3) and (v2.m == 1 and v2.n == 3)):
            raise EngineException(EngineException.VECTOR_PRODUCT_ERROR)

        i_vec = Vector([[1.0], [0.0], [0.0]])
        j_vec = Vector([[0.0], [1.0], [0.0]])
        k_vec = Vector([[0.0], [0.0], [1.0]])

        mat = Matrix([[i_vec, j_vec, k_vec],
                      v1.floatlist[0],
                      v2.floatlist[0]])
        res = mat.determinant()
        return res

    def __pow__(self, vec):
        return self.vector_product(vec)

    def length(self):
        return math.sqrt(self.scalar_product(self))

    def __mod__(self, vec):
        return self.scalar_product(vec)

    def dim(self):
        if self.is_column:
            return len(self.floatlist)
        else:
            return len(self.floatlist[0])


def BilinearForm(mat, vec1, vec2):
    res = 0

    if not vec2.is_column:
        vec2 = vec2.transpose()

    for i in range(0, len(vec1.floatlist)):
        for j in range(0, len(vec2.floatlist)):
            res += mat.floatlist[i][j] * vec1.floatlist[i][0] * vec2.floatlist[j][0]

    return res


class VectorSpace:
    def __init__(self, veclist):
        size = len(veclist)
        for vec in veclist:
            if not isinstance(vec, Point) and isinstance(vec, Vector):
                if vec.dim() != size:
                    raise EngineException

        self.veclist = veclist

    def scalar_product(self, vec1, vec2):
        return vec1.transpose() * Matrix.gram(self.veclist) * vec2

    def vector_form(self, pt):
        res = None
        if pt.m != len(self.veclist):
            raise EngineException(EngineException.VECTOR_LIST_SIZE_ERROR)

        for i in range(0, pt.m):
            vec = self.veclist[i]
            vec *= pt.floatlist[i][0]
            if res is None:
                res = vec
            else:
                res += vec
        return res


class Point(Vector):
    def __init__(self, val):
        if isinstance(val, Vector):
            super().__init__(val.floatlist)
        else:
            super().__init__(val)

    def __add__(self, vec):
        return Point(super().__add__(vec).floatlist)

    def __sub__(self, vec):
        return self + (vec * -1)


class CoordinateSystem:
    def __init__(self, pt, vs):
        self.point = pt
        self.vecspace = vs
