from backticks._tokens import *
from .strings import *

def new_list(_type, var, _list, _len=False, _func=False):
    # print(_list)
    str_to_ret = ""
    _list_len = len(_list)
    # print(f"LEN: {_list_len}")
    # _header = f"{_type} {var}[{_list_len}];\n"
    _li = str(_list)
    _li = _li.replace(LEFTSQUARE, LEFTCURL)
    _li = _li.replace(RIGHTSQUARE, RIGHTCURL)

    if _len:
        str_to_ret += f"{_type} {var}[{_len}] = {_li};\n"

        # return (_header, str_to_ret)
        return str_to_ret


    else:
        if not _func:
            str_to_ret += f"{var}_len = {_list_len};\n"
            str_to_ret += f"{var} = ({_type} *)calloc({_list_len}, sizeof({_type}));\n"
            str_to_ret += f"{var}_copy = {var};\n"
        else:
            str_to_ret += f"size_t {var}_len = {_list_len};\n"
            str_to_ret += f"{_type} *{var} = ({_type} *)calloc({_list_len}, sizeof({_type}));\n"
            str_to_ret += f"{_type} *{var}_copy = {var};\n"

        if _type != CHARSTAR:    
            for i in range(_list_len):
                str_to_ret += f"{var}[{i}] = {_list[i].strip()};\n"
        else:
            for i in range(_list_len):
                str_to_ret += new_str(f"{var}[{i}]", f"{_list[i].strip()}")
                # str_to_ret += f"{var}[{i}] = {_list[i].strip()};\n"

        return str_to_ret

def assign_by_idx(var, idx, val):
    str_to_ret = f"{var[[idx]]} = {val};"
    return str_to_ret

def access_elem_by_ref(_type, _k, _v, _list_name, for_body, _start=None, _end=None):

    if not _start:
        _start = 0

    if not _end:
        _end = f"{_list_name}_len"

    str_to_ret = f'''for (size_t {_k} = {_start}; {_k} < {_end}; ++{_k})
{{
    {_type} {_v} = {_list_name}[{_k}];
    {for_body}
    
}}'''

    return str_to_ret