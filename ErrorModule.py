# Created by X-Corporation


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
    VECTOR_SIZE_SPACE_ERROR = "Error 3: Wrong vector size for vector space"

    # Code 4: Wrong operators
    POINT_SUBTRACTION_ERROR = "Error 4: Point can not be subtracted"
    POINT_MULTIPLICATION_ERROR = "Error 4: Point can not be a multiplier"
    POINT_DIVISION_ERROR = "Error 4: Point can not be a part of division"
