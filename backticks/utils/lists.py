from backticks._tokens import *
from .strings import *

def new_list(_type, var, _list, _len=False, _func=False):
    # print(_list)
    str_to_ret = ""
    _list_len = len(_list)
    # print(f"LEN: {_list_len}")
    _li = str(_list)
    _li = _li.replace(LEFTSQUARE, LEFTCURL)
    _li = _li.replace(RIGHTSQUARE, RIGHTCURL)

    # if _type == CHARSTAR:
    #     _type = "str"

    if not _len:
        _len = _list_len

    str_to_ret += f"""{_type + '_list_t *' if _func else ""}{var} = ({_type}_list_t *)calloc(1, sizeof({_type}_list_t));
{var}->len = {_len};
{var}->ptr = calloc({_len}, sizeof({_type}));
{var}->ptr_copy = {var}->ptr;
"""

    if _type != STR:
        if _list_len > 1:
            for i in range(_list_len):
                str_to_ret += f"{var}->ptr[{i}] = {_list[i]};\n"
        elif _list_len == 1:
            str_to_ret += f"for (size_t i = 0; i < {_len}; ++i){var}->ptr[i] = {_list[0]};\n"

    else:
        if _list_len > 1:
            for i in range(_list_len):
                str_to_ret += new_str(f"{var}->ptr[{i}]", f"{_list[i]}")
        elif _list_len == 1:
            str_to_ret += f'for (size_t i = 0; i < {_len}; ++i) {{{new_str(f"{var}->ptr[i]", f"{_list[0]}")}}}\n'
                
    return str_to_ret

        
def append_list(_type, var, vals_list):
    str_to_ret = ""
    _list_len = len(vals_list)

    str_to_ret += f"{var}->ptr = realloc({var}->ptr, ({var}->len+{_list_len}) * sizeof({_type}));\n"

    str_to_ret += f'if({var}->ptr==NULL){{printf("Memory allocation failed\\n");exit(1);}}\n'
    

    if _type != STR:
        for i in range(_list_len):
            str_to_ret += f"{var}->ptr[{var}->len+{i}] = {vals_list[i]};\n"
    else:
        for i in range(_list_len):
            str_to_ret += new_str(f"{var}->ptr[{var}->len+{i}]", f"{vals_list[i]}")

    str_to_ret += f"{var}->len += {_list_len};\n"

    return str_to_ret

def access_elem_by_ref(_type, _k, _v, _list_name, for_body, _start=None, _end=None):

    if not _start:
        _start = 0

    if not _end:
        _end = f"{_list_name}->len"

    str_to_ret = f"""for (size_t {_k} = {_start}; {_k} < {_end}; ++{_k}) {{{_type} {_v} = {_list_name}->ptr[{_k}];
{for_body}}}\n"""

    return str_to_ret