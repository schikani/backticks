from backticks._tokens import *
from .strings import *

DEFAULT_RESERVE_SIZE = 20

def new_list(_type, var, _list, _reserve=None, _func=False):
    # print(_list)
    str_to_ret = ""
    _list_len = len(_list)

    if not _reserve:
        _reserve = DEFAULT_RESERVE_SIZE

    str_to_ret += f"{_type + '_list_t *' if _func else ''}{var} = new_{_type}_list({_reserve});\n"

    if _type != STR:
        if _list_len > 1:
            for i in range(_list_len):
                str_to_ret += f"check_reserve_{_type}_list({var});\n"
                str_to_ret += f"{var}->ptr[{i}] = {_list[i]};\n"
                str_to_ret += f"{var}->len += 1;\n"

        elif _list_len == 1:
            str_to_ret += f"for (size_t i = 0; i < {_reserve}; ++i){var}->ptr[i] = {_list[0]};\n"
            str_to_ret += f"{var}->len += 1;\n"

    else:
        if _list_len > 1:
            for i in range(_list_len):
                str_to_ret += f"check_reserve_{_type}_list({var});\n"
                str_to_ret += new_str(f"{var}->ptr[{i}]", f"{_list[i]}")
                str_to_ret += f"{var}->len += 1;\n"


        elif _list_len == 1:
            str_to_ret += f'for (size_t i = 0; i < {_reserve}; ++i) {{{new_str(f"{var}->ptr[i]", f"{_list[0]}")}}}\n'
                
    return str_to_ret

        
def append_list(_type, var, vals_list):
    str_to_ret = ""
    _list_len = len(vals_list)

    if _type != STR:
        for i in range(_list_len):
            str_to_ret += f"check_reserve_{_type}_list({var});\n"
            str_to_ret += f"{var}->ptr[{var}->len] = {vals_list[i]};\n"
            str_to_ret += f"{var}->len += 1;\n"

    else:
        for i in range(_list_len):
            str_to_ret += f"check_reserve_{_type}_list({var});\n"
            str_to_ret += new_str(f"{var}->ptr[{var}->len]", f"{vals_list[i]}")
            str_to_ret += f"{var}->len += 1;\n"

    # str_to_ret += f'printf("%ld\\n", {var}->reserve);\n'
    return str_to_ret

def access_elem_by_ref(_type, _k, _v, _list_name, for_body, _start=None, _end=None):

    if not _start:
        _start = 0

    if not _end:

        _end = f"{_list_name}->len"
        _list_name += "->ptr"
    
    # print(_type)

    str_to_ret = f"""for (size_t {_k} = {_start}; {_k} < {_end}; ++{_k}) {{{_type} {_v} = {_list_name}[{_k}];
{for_body}}}\n"""

    return str_to_ret