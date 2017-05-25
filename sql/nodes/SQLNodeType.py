class SQLNodeType(object):
    """
    Enum of Node types we'll be working with. This will help bring up errors.
    """
    SELECT_NODE       = 1
    TABLE_NODE        = 2
    VALUE_NODE        = 3
    ATTRIBUTE_NODE    = 4
    FUNCTION_NODE     = 5
    LIMIT_NODE        = 6
    INTERMEDIATE_NODE = 7
