def is_presented(value):
    return value is not None

def is_bigger(value, n=0, is_required=False):
    if value is None:
        return not is_required
    return value>n

def is_string(value,):
    return isinstance(value, str)

def is_boolean(value, is_required=False):
    if value is None:
        return not is_required
    return isinstance(value, bool)

def is_list(value):
    return isinstance(value, list)

def is_probability(value):
    return value > 0 and value <1

def is_list_of_dict(value, is_required=False, elements_are_required=False):
    if value is None:
        return not is_required
    if isinstance(value, list):
        for element in value:
            if elements_are_required and element is None:
                return False
            if not isinstance(element, dict):
                return False
        return True
    return False