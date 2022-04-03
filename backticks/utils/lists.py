from backticks._tokens import *

def new_list(_type, var, _list, _len=False):
    str_to_ret = ""
    _list_len = len(_list)
    _li = str(_list)
    _li = _li.replace(LEFTSQUARE, LEFTCURL)
    _li = _li.replace(RIGHTSQUARE, RIGHTCURL)

    if _len:
        str_to_ret += f"{_type} {var}[{_len}] = {_li};\n"

        return (f"{_type} {var}[{_list_len}];\n", str_to_ret)

    else:
        str_to_ret += f"{var}_len = {_list_len};\n"
        str_to_ret += f"{_type} *{var} = ({_type} *)calloc({_list_len}, sizeof({_type}));\n"
        str_to_ret += f"{var}_copy = {var};\n"
        for i in _list_len:
            str_to_ret += f"{var}[{i}] = {_list[i]};\n"

        return (f"{_type} *{var};\n{_type} *{var}_copy;\nsize_t {var}_len;\n", str_to_ret)

# def append_to_list(var, _val):
