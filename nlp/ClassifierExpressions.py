COUNT_TYPE  = r'^(how many|count of|number of)$'
OPERATOR_EQUALITY_TYPE  = r'^(equals)$'
OPERATOR_INVERT_TYPE  = r'^(not)$'
OPERATOR_MANY_TYPE = r'(^(in|are|have|will|)(\s)(taking|taken|took|take))$'
OPERATOR_MAX_TYPE = r'^(most|greatest|best|largest|max)$'
OPERATOR_MIN_TYPE = r'^(least|smallest|worst|min)$'
OPERATOR_GREATER_TYPE = r'(^(greater|bigger|more)\s(than|then))$'
OPERATOR_LESS_TYPE = r'(^(less|fewer)(\s)(than|then))$'
LIST_TYPE   = r'(^(list|give me)(\s)(several|all|a few|few|one|two|three|four|five|six|seven|eight|nine|ten))$'
TIME_TYPE  = r'(^(1[012]|[1-9]):[0-5][0-9](\s)?(?i)(\s)*(am|pm))$'
DATE_TYPE  = r'(^(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/((19|20)\d\d))$'
STOP_TYPE = r'^(return|[.?])$'

ALL_TYPES = {
    'COUNT': COUNT_TYPE,
    'LIST': LIST_TYPE,
    'TIME': TIME_TYPE,
    'DATE': DATE_TYPE,
    'STOP': STOP_TYPE,
    'EQUALS': OPERATOR_EQUALITY_TYPE,
    'NOT': OPERATOR_INVERT_TYPE,
    'IN': OPERATOR_MANY_TYPE,
    'MAX': OPERATOR_MAX_TYPE,
    'MIN': OPERATOR_MIN_TYPE,
    'LESS': OPERATOR_GREATER_TYPE,
    'MORE': OPERATOR_LESS_TYPE
}