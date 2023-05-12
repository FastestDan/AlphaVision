# Created by X-Corporation


class MathException(Exception):
    # Code 0: Wrong input data
    INIT_ERROR = "Math Error 01: Wrong initialization data"
    VECTOR_LIST_ERROR = "Math Error 02: Non-vector instance in the list of vectors"

    # Code 1: Wrong matrix size
    ADDITION_ERROR = "Math Error 11: Wrong matrix size for addition"
    SUBTRACTION_ERROR = "Math Error 12: Wrong matrix size for subtraction"
    MULTIPLICATION_ERROR = "Math Error 13: Wrong matrix size for multiplication"
    DIVISION_ERROR = "Math Error 14: Wrong matrix size for division"
    DETERMINANT_ERROR = "Math Error 15: Wrong matrix size for determinant to be found"
    INVERSION_ERROR = "Math Error 16: Wrong matrix size for the inversion"

    # Code 2: Wrong vector size
    SCALAR_PRODUCT_ERROR = "Math Error 21: Wrong vector size for scalar product"
    VECTOR_PRODUCT_ERROR = "Math Error 22: Wrong vector size for vector product"
    DIFFERENCE_ERROR = "Math Error 23: Different size of vectors in a list of vectors"

    # Code 3: Wrong values
    ZERO_ERROR = "Math Error 31: Division by zero impossible"
    INVERSION_DETERMINANT_ERROR = "Math Error 32: Wrong determinant value for the inversion"
    VECTOR_LIST_SIZE_ERROR = "Math Error 33: Wrong size of list of vectors"
    INDEX_ERROR = "Math Error 34: Wrong indexes"
    ROTATOR_SIZE_ERROR = "Math Error 35: Wrong value for the size of the rotation matrix"
    STATE_ERROR = "Math Error 36: Vector states are not the same"
    ANGLE_ERROR = "Math Error 37: Wrong angle values"
    VECTOR_SIZE_SPACE_ERROR = "Math Error 38: Wrong vector size for vector space"

    # Code 4: Wrong operators
    POINT_SUBTRACTION_ERROR = "Math Error 41: Point can not be subtracted"
    POINT_MULTIPLICATION_ERROR = "Math Error 42: Point can not be a multiplier"
    POINT_DIVISION_ERROR = "Math Error 43: Point can not be a part of division"
