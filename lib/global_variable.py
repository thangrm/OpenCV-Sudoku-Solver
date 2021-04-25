def init_global_variable():
    global GLOBALS_DICT
    GLOBALS_DICT = {}

def set_variable(name, value):
    try:
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False

def get_variable(name):
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"