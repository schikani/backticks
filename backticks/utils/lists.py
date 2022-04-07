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

    if _len and not _func:
        str_to_ret += f"{var}_len = {_len};\n"

        if _type != CHARSTAR:
            if _list_len > 1:
                for i in range(_list_len):
                    str_to_ret += f"{var}[{i}] = {_list[i]};\n"
            elif _list_len == 1:
                str_to_ret += f"for (size_t i = 0; i < {_len}; ++i){var}[i] = {_list[0]};\n"

                # str_to_ret += f"{var}[{_len}] = {{{_list[0]}}};\n"
        else:
            for i in range(_list_len):
                str_to_ret += new_str(f"{var}[{i}]", f"{_list[i]}")
        return str_to_ret

    elif _len and _func:
        str_to_ret += f"size_t {var}_len = {_len};\n"
        str_to_ret += f"{_type} {var}[{_len}] = {_li};\n"
        return str_to_ret

    else:
        if not _func:
            str_to_ret += f"{var} = ({_type} *)calloc({_list_len}, sizeof({_type}));\n"
            str_to_ret += f"{var}_copy = {var};\n"
            str_to_ret += f"{var}_len = {_list_len};\n"
        else:
            str_to_ret += f"{_type} *{var} = ({_type} *)calloc({_list_len}, sizeof({_type}));\n"
            str_to_ret += f"{_type} *{var}_copy = {var};\n"
            str_to_ret += f"size_t {var}_len = {_list_len};\n"

        if _type != CHARSTAR:    
            for i in range(_list_len):
                str_to_ret += f"{var}[{i}] = {_list[i]};\n"
        else:
            for i in range(_list_len):
                str_to_ret += new_str(f"{var}[{i}]", f"{_list[i]}")
                # str_to_ret += f"{var}[{i}] = {_list[i]};\n"

        return str_to_ret

def append_list(_type, var, vals_list):
    str_to_ret = ""
    _list_len = len(vals_list)

    str_to_ret += f"{var} = ({_type} *)realloc({var}, ({var}_len+{_list_len}) * sizeof({_type}));\n"

    str_to_ret += f'if({var}==NULL){{printf("Memory allocation failed\\n");exit(1);}}\n'
    

    if _type != CHARSTAR:
        for i in range(_list_len):
            str_to_ret += f"{var}[{var}_len+{i}] = {vals_list[i]};\n"
    else:
        for i in range(_list_len):
            str_to_ret += new_str(f"{var}[{var}_len+{i}]", f"{vals_list[i]}")

    str_to_ret += f"{var}_len += {_list_len};\n"

    return str_to_ret

def access_elem_by_ref(_type, _k, _v, _list_name, for_body, _start=None, _end=None):

    if not _start:
        _start = 0

    if not _end:
        _end = f"{_list_name}_len"

    str_to_ret = f"""for (size_t {_k} = {_start}; {_k} < {_end}; ++{_k})
{{
{_type} {_v} = {_list_name}[{_k}];
{for_body}
    
}}"""

    return str_to_ret