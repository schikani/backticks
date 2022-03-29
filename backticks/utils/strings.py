from backticks._tokens import *

def user_input(var, prompt=""):
    str_to_ret = ""

    if prompt:
        str_to_ret += f'printf({prompt});' + NEWLINE
        
    str_to_ret += f"{var} = _bt_input(stdin);" + NEWLINE

    return str_to_ret


def new_str(var, _str):

    _s = ""
    for i in _str:
        if i == NEWLINE:
            _s += "\\n"
        else:
            _s += i

    _str = _s

    str_to_ret = f'{var} = calloc(strlen({_str})+1, sizeof(char));' + NEWLINE
    str_to_ret += f'strcpy({var}, {_str});' + NEWLINE
    return str_to_ret


def concat_str(var, _str):

    _s = ""
    for i in _str:
        if i == NEWLINE:
            _s += "\\n"
        else:
            _s += i

    _str = _s

    str_to_ret = f'{var} = realloc({var}, (strlen({var}) + strlen({_str})) * sizeof(char));' + NEWLINE
    str_to_ret += f'strcat({var}, {_str});' + NEWLINE
    return str_to_ret


def compare_str(var, _str):

    _s = ""
    for i in _str:
        if i == NEWLINE:
            _s += "\\n"
        else:
            _s += i

    _str = _s

    str_to_ret = f'strcmp({var}, {_str})'
    return str_to_ret


def free_str(var):
    str_to_ret = f'free({var});' + NEWLINE
    str_to_ret += f'{var} = NULL;' + NEWLINE
    return str_to_ret
