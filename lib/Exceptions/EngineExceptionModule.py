# Created by X-Corporation


class EngineException(Exception):
    PROPERTY_NOT_EXIST_ERROR = "Engine Error 1: Property does not exist"
    PROP_OF_PROPS_ERROR = "Engine Error 2: Can't delete list of all properties"
    ENTITY_NOT_EXIST_ERROR = "Engine Error 3: Entity does not exist in the list"
    VEC_PT_DIM_ERROR = "Engine Error 4: Sizes of position and direction do not match"
    NO_DIR_ERROR = "Engine Error 5: No direction of view"
