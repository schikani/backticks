from backticks._tokens import *
from .strings import *

def new_list(_type, var, _list, _len=False):
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
        str_to_ret += f"{var}_len = {_list_len};\n"
        str_to_ret += f"{var} = ({_type} *)calloc({_list_len}, sizeof({_type}));\n"
        str_to_ret += f"{var}_copy = {var};\n"

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
# def append_to_list(var, _val):
