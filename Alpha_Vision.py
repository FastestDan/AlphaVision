# Created by X-Corporation
import math


class EngineException(Exception):
    # Code 0: Wrong input data
    InitErr = "Error 0: Wrong initialization data"
    VecListErr = "Error 0: Non-vector instance in the list of vectors"

    # Code 1: Wrong matrix size
    AddErr = "Error 1: Wrong matrix size for addition"
    SubErr = "Error 1: Wrong matrix size for subtraction"
    MulErr = "Error 1: Wrong matrix size for multiplication"
    DivErr = "Error 1: Wrong matrix size for division"
    DetErr = "Error 1: Wrong matrix size for determinant to be found"
    InvErr = "Error 1: Wrong matrix size for the inversion"

    # Code 2: Wrong vector size
    ScalErr = "Error 2: Wrong vector size for scalar product"
    VecErr = "Error 2: Wrong vector size for vector product"
    DifErr = "Error 2: Different size of vectors in a list of vectors"

    # Code 3: Wrong values
    ZeroErr = "Error 3: Division by zero impossible"
    DetInvErr = "Error 3: Wrong determinant value for the inversion"
    VecLenErr = "Error 3: Wrong size of list of vectors"
    AxErr = "Error 3: Wrong axis"

    # Code 4: Wrong operators
    PointSubErr = "Error 4: Point can not be subtracted"
    PointMulErr = "Error 4: Point can not be a multiplier"
    PointDivErr = "Error 4: Point can not be a part of division"


class Matrix:
    def __init__(self, llf):
        self.floatlist = llf
        self.m = len(llf)
        n = len(llf[0])
        for i in range(1, self.m):
            if len(llf[i]) != n:
                raise EngineException(EngineException.ZeroErr)

            n = len(llf[i])
        self.n = n

    def __add__(self, mat):
        if (self.m != mat.m) or (self.n != mat.n):
            raise EngineException(EngineException.AddErr)

        for i in range(0, self.m):
            for j in range(0, self.n):
                self.floatlist[i][j] += mat.floatlist[i][j]
        return self

    def __sub__(self, mat):
        if isinstance(mat, Point):
            raise EngineException(EngineException.PointSubErr)

        if (self.m != mat.m) or (self.n != mat.n):
            raise EngineException(EngineException.SubErr)

        return self + (mat * -1)

    def __mul__(self, elem):
        if isinstance(elem, Point):
            raise EngineException(EngineException.PointMulErr)

        if isinstance(elem, Matrix):
            if self.n != elem.m:
                raise EngineException(EngineException.MulErr)

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
            return self

    def __truediv__(self, elem):
        if isinstance(elem, Point):
            raise EngineException(EngineException.PointDivErr)

        if isinstance(elem, Matrix):
            mele = elem.inverse()
            if self.n != mele.m:
                raise EngineException(EngineException.DivErr)

            return mele * self

        else:
            if elem == 0:
                raise EngineException(EngineException.ZeroErr)

            return self * (1/elem)

    def determinant(self):
        if self.m != self.n:
            raise EngineException(EngineException.DetErr)
        det = 0
        elem = 1

        if self.m == 2:
            for i in range(0, self.m):
                elem *= self.floatlist[i][i]
            det += elem
            elem = 1
            for i in range(0, self.m):
                elem *= self.floatlist[self.m - i - 1][i]
            det -= elem
            return det

        else:
            count1 = 0
            count2 = 0
            while count1 < self.m:
                mat2 = list()
                for i in range(0, self.m):
                    if i == count1:
                        continue
                    line2 = list()
                    for j in range(0, self.m):
                        if j == count2:
                            continue
                        line2.append(self.floatlist[i][j])
                    mat2.append(line2)
                elem = Matrix(mat2).determinant()
                if (count1 + count2 + 2) % 2 == 0:
                    det += self.floatlist[count1][count2] * elem
                else:
                    det -= self.floatlist[count1][count2] * elem
                count2 += 1
                if count2 >= self.m:
                    count2 = 0
                    count1 += 1
            return det

    def inverse(self):
        if self.m != self.n:
            raise EngineException(EngineException.InvErr)

        det = self.determinant()

        if det == 0:
            raise EngineException(EngineException.DetInvErr)

        matf = list()
        if self.m == 2:
            matf = [[self.floatlist[1][1], self.floatlist[1][0]], [self.floatlist[0][1], self.floatlist[0][0]]]

        else:
            line1 = list()
            count1 = 0
            count2 = 0
            while count1 < self.m:
                mat2 = list()
                for i in range(0, self.m):
                    if i == count1:
                        continue
                    line2 = list()
                    for j in range(0, self.m):
                        if j == count2:
                            continue
                        line2.append(self.floatlist[i][j])
                    mat2.append(line2)
                elem = Matrix(mat2).determinant()
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
            if not isinstance(veclist[i], Vector):
                raise EngineException(EngineException.VecListErr)

            mv = veclist[i].m
            nv = veclist[i].n
            if prevm is None:
                prevm = mv
                prevn = nv
                continue
            elif (prevm != mv) or (prevn != nv):
                raise EngineException(EngineException.DifErr)

        mat = list()
        count = 0
        for i in range(0, len(veclist)):
            res = list()
            for j in range(0, len(veclist)):
                res.append(veclist[i][count] % veclist[i][j])
            count += 1
            mat.append(res)
        return Matrix(mat)

    @staticmethod
    def rotator(angle1, axis1, angle2=None, axis2=None, angle3=None, axis3=None):
        m1 = None
        if axis1.lower() == "x":
            m1 = Matrix([[1, 0, 0],
                         [0, round(math.cos(math.radians(angle1))), round(-math.sin(math.radians(angle1)))],  # Round нужон?
                         [0, round(math.sin(math.radians(angle1))), round(math.cos(math.radians(angle1)))]])
        elif axis1.lower() == "y":
            m1 = Matrix([[round(math.cos(math.radians(angle1))), 0, round(math.sin(math.radians(angle1)))],
                         [0, 1, 0],
                         [round(-math.sin(math.radians(angle1))), round(math.cos(math.radians(angle1)))]])
        elif axis1.lower() == "z":
            m1 = Matrix([[round(math.cos(math.radians(angle1))), round(-math.sin(math.radians(angle1))), 0],
                         [round(math.sin(math.radians(angle1))), round(math.cos(math.radians(angle1))), 0],
                         [0, 0, 1]])
        else:
            raise EngineException(EngineException.AxErr)
        if axis2 is not None and angle2 is not None:
            m2 = Matrix.rotation(angle2, axis2)
        else:
            m2 = Matrix.identity(3)
        if axis3 is not None and angle3 is not None:
            m3 = Matrix.rotation(angle3, axis3)
        else:
            m3 = Matrix.identity(3)
        res = m1 * m2 * m3
        return res


class Vector(Matrix):
    def __init__(self, llf):
        self.m = len(llf)
        self.n = 1
        self.floatlist = llf
        for i in range(0, self.m):
            if len(llf[i]) != 1:
                raise EngineException(EngineException.InitErr)

    def scalmul(self, vec):
        if (self.m != vec.m) or (self.n != vec.n):
            raise EngineException(EngineException.ScalErr)

        res = 0
        for i in range(0, self.m):
            for j in range(0, self.n):
                res += self.floatlist[i][j] * vec.floatlist[i][j]
        return res

    def vecmul(self, vec):
        if not((self.m == 3 and self.n == 1) and (vec.m == 3 and vec.n == 1)):
            raise EngineException(EngineException.VecErr)

        mat = [[0], [0], [0]]
        mat[0][0] = self.floatlist[1][0] * vec.floatlist[2][0] - self.floatlist[2][0] * vec.floatlist[1][0]
        mat[1][0] = self.floatlist[2][0] * vec.floatlist[0][0] - self.floatlist[0][0] * vec.floatlist[2][0]
        mat[2][0] = self.floatlist[0][0] * vec.floatlist[1][0] - self.floatlist[1][0] * vec.floatlist[0][0]
        return Vector(mat)

    def __pow__(self, vec):
        return self.vecmul(vec)

    def length(self):
        return math.sqrt(self.scalmul(self))

    def __mod__(self, vec):
        return BilinearForm(Matrix.identity(self.m).floatlist, self.floatlist, vec.floatlist)


def BilinearForm(mat, vec1, vec2):
    res = 0
    for i in range(0, len(vec1)):
        for j in range(0, len(vec2)):
            res += mat[i][j] * vec1[i][0] * vec2[j][0]
    return res


class VectorSpace:
    def __init__(self, veclist):
        prevn = None
        prevm = None
        for i in range(0, len(veclist)):
            if not isinstance(veclist[i], Vector):
                raise EngineException(EngineException.VecListErr)

            mv = veclist[i].m
            nv = veclist[i].n
            if prevm is None:
                prevm = mv
                prevn = nv
                continue
            elif (prevm != mv) or (prevn != nv):
                raise EngineException(EngineException.DifErr)

        self.veclist = veclist

    def scalmul(self, vec1, vec2):
        return vec1.transpose() * Matrix.gram(self.veclist) * vec2

    def vecform(self, pt):
        res = None
        if pt.m != len(self.veclist):
            raise EngineException(EngineException.VecLenErr)

        for i in range(0, pt.m):
            vec = self.veclist[i]
            vec *= pt.floatlist[i][0]
            if res is None:
                res = vec
            else:
                res += vec
        return res


class Point(Vector):
    def __add__(self, vec):
        return Point(super().__add__(vec).floatlist)

    def __sub__(self, vec):
        return self + (vec * -1)


class CoordinateSystem:
    def __init__(self, pt, vs):
        self.point = pt
        self.vecspace = vs