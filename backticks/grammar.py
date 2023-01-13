from ._tokens import *
from .tokenizer import Tokenizer
from .c_templates import *
from .utils.strings import *
from .utils.lists import *
import pprint


class BT_Grammar(Tokenizer):
    def __init__(self, bt_file_path):
        super().__init__(bt_file_path)
        self._vars_dict = dict()
        self._class_vars_dict = dict()
        self._imports_dict = dict()
        self._global_vars_list = []
        self._private_func_list = []
        self._public_func_list = []
        self._funcs_impl = []
        self._includes = []
        self._includes.append('#include "_bt_builtins_.h"')

        '''
                      GLOBAL VARIABLES
            {
               "global_vars": {
                        "var1": [val, type],
                        "var2": [val, type],
                }
            }
        
                      FUNCTION VARIABLES
            {
               "func1": [
                   (ret_val, ret_type, func_type), 
                {
                    "var1": [val, type],
                    "var2": [val, type],
                }],

                "func2": [
                        (ret_val, ret_type, func_type),    --> index 0 of 'func2'
                {
                        "var1": [val, type], 
                        "var2": [val, type],
                }
            ]
            }
        '''
        self._vars_dict["GLOBALS"] = {"global_vars": {}}
        self._vars_dict["FUNCS"] = {}

        # self._class_vars_dict["GLOBALS"] = {"global_vars": {}}
        # self._class_vars_dict["FUNCS"] = {}
        self._class_structs = []

        # self._vars_dict["INBUILT_FUNCS"] = {}
        # self._vars_dict["INBUILT_FUNCS"][f"input_{self.bin_name}"] = [("", STR), {"var1": ["", STR]}]

    def __bt_to_c_str(self, _str):
        _str = '"' + _str[1:-1] + '"'

        return _str

    def __eval_assign_values(self, vars_dict, tok_list, _global_call, _del):
        bool_found = False
        float_found = False
        str_found = False
        int_found = False
        val = ""
        _type = ""
        _type_suffix = ""
        _sub_type = ""
        _val_idx = 0

        # print(tok_list)

        # To parse a string
        # Invoked from self.__string_parser()
        if len(tok_list) == 2:
            if tok_list[1] == tuple():
                tok_list = self._tokenizer(tok_list[0] + SEMI)
                # print(tok_list)
                # for idx, t in enumerate(tok_list):
                #     if t.find(DOT) != -1:
                #         tl = t.split(DOT)
                #         if tl[0] in self._imports_dict:
                #             tok_list[idx] = self._imports_dict[tl[0]] + DOT + tl[1]

        # print(tok_list)
        while tok_list[_val_idx] != _del:

            v = tok_list[_val_idx]

            if self._in_func_names(v):
                v = self._in_func_names(v)

            if self.is_list(v) or self.is_string(v) or self.is_string(v, vars_dict) or \
                    self.is_string(v, self._vars_dict["GLOBALS"]["global_vars"]) or \
                    self.is_string(v, self._vars_dict["FUNCS"], func=True) or \
                    self.is_string(tok_list[_val_idx + 1]):

                if self.is_list(v) and v[0] == LEFTSQUARE:

                    if self.is_float(v):
                        float_found = True

                    elif self.is_int(v):
                        int_found = True

                    elif self.is_bool(v):
                        bool_found = True

                str1 = ""
                str1_params = ""
                str2 = ""
                str2_params = ""

                # Compare
                if tok_list.count(EQUALS) == 2:
                    if v != EQUALS:
                        str1 = v
                    else:
                        str1 = tok_list[0]

                    # a[0] case
                    if self.is_list(str1):
                        str1, str1_params = str1.split(LEFTSQUARE)
                        str1_params = "[" + str1_params

                    if tok_list.count(LEFTBRACK):
                        if tok_list[_val_idx + 1] == LEFTBRACK:
                            _val_idx += 2
                            while tok_list[_val_idx] != RIGHTBRACK:
                                str1_params += tok_list[_val_idx]
                                _val_idx += 1

                            _val_idx += 3

                            str2 = tok_list[_val_idx]

                            # print(str2)

                            if self.is_list(str2):
                                str2, str2_params = str2.split(LEFTSQUARE)
                                str2_params = "[" + str2_params

                                # print(str2)

                            if tok_list[_val_idx + 1] == LEFTBRACK:
                                _val_idx += 2
                                while tok_list[_val_idx] != RIGHTBRACK:
                                    str2_params += tok_list[_val_idx]
                                    _val_idx += 1

                                _val_idx += 1

                            if self._in_func_names(str2):
                                str2 = self._in_func_names(str2)

                        else:
                            _val_idx += 3
                            str2 = tok_list[_val_idx]

                            if str2 == LEFTCURL:
                                str2 = tok_list[_val_idx - 1]

                            if tok_list[_val_idx + 1] == LEFTBRACK:
                                _val_idx += 2
                                while tok_list[_val_idx] != RIGHTBRACK:
                                    str2_params += tok_list[_val_idx]
                                    _val_idx += 1

                                _val_idx += 1

                            if self.is_list(str2):
                                str2, str2_params = str2.split(LEFTSQUARE)
                                str2_params = "[" + str2_params

                            if self._in_func_names(str2):
                                str2 = self._in_func_names(str2)

                    else:
                        _val_idx += 3
                        str2 = tok_list[_val_idx]

                        if self.is_list(str2):
                            str2, str2_params = str2.split(LEFTSQUARE)
                            str2_params = "[" + str2_params

                    if str1_params and str1_params.find(COMA):
                        s1_t = str1_params.split(COMA)
                        new_s1_t = []
                        for idx, v in enumerate(s1_t):
                            new_s1_t.append(v)
                            if idx < len(s1_t) - 1:
                                new_s1_t.append(COMA)
                        # print(new_s1_t)
                        new_s1_t.append(SEMI)
                        _val, _type = self.__eval_assign_values(
                            vars_dict, new_s1_t, _global_call, SEMI)
                        str1_params = _val

                    if str2_params and str2_params.find(COMA):
                        s2_t = str2_params.split(COMA)
                        new_s2_t = []
                        for idx, v in enumerate(s2_t):
                            new_s2_t.append(v)
                            if idx < len(s2_t) - 1:
                                new_s2_t.append(COMA)
                        # print(new_s2_t)
                        new_s2_t.append(SEMI)
                        _val, _type = self.__eval_assign_values(
                            vars_dict, new_s2_t, _global_call, SEMI)
                        str2_params = _val

                    # print(str1, str1_params)
                    # print(str2, str2_params)

                    if self.is_string(str1):
                        str1 = self.__bt_to_c_str(str1)

                    elif self.is_string(str1, vars_dict):
                        # print("~"+str1+"~")
                        if _global_call:
                            if str1.find(DOT) == -1 and vars_dict[str1][2] != "__FOR__":
                                str1 = self.bin_name + DOT + str1 + str1_params

                            elif str1.find(DOT) == -1 and vars_dict[str1][2] == "__FOR__":
                                str1 = str1 + str1_params
                            else:
                                sl = str1.split(DOT)
                                # print(sl)
                                if sl[0] in self._imports_dict:
                                    str1 = self._imports_dict[sl[0]
                                                              ] + DOT + sl[1]

                    elif self.is_string(str1, self._vars_dict["GLOBALS"]["global_vars"]):
                        # print("~"+str1+"~")

                        str1 = self.bin_name + DOT + str1 + str1_params
                        # print(str1)

                    elif self.is_string(str1, self._vars_dict["FUNCS"], func=True):
                        # print("~"+str1+"~")
                        if str1.find(DOT) != -1:
                            sl = str1.split(DOT)
                            if sl[0] in self._imports_dict:
                                str1 = sl[1] + "_" + self._imports_dict[sl[0]]

                        str1 += LEFTBRACK + str1_params + RIGHTBRACK
                        # _val_idx += 2

                    if self.is_string(str2):
                        # print("~"+str2+"~")

                        str2 = self.__bt_to_c_str(str2)

                    elif self.is_string(str2, vars_dict):
                        # print("~"+str2+"~")

                        if _global_call:
                            if str2.find(DOT) == -1 and vars_dict[str2][2] != "__FOR__":
                                str2 = self.bin_name + DOT + str2 + str2_params

                            elif str2.find(DOT) == -1 and vars_dict[str2][2] == "__FOR__":
                                str2 = str2 + str2_params

                            else:
                                sl = str2.split(DOT)
                                if sl[0] in self._imports_dict:
                                    str2 = self._imports_dict[sl[0]
                                                              ] + DOT + sl[1]

                    elif self.is_string(str2, self._vars_dict["GLOBALS"]["global_vars"]):
                        if str2.find(DOT) == -1:
                            str2 = self.bin_name + DOT + str2 + str2_params
                        else:
                            sl = str2.split(DOT)
                            if sl[0] in self._imports_dict:
                                str2 = self._imports_dict[sl[0]] + DOT + sl[1]

                    elif self.is_string(str2, self._vars_dict["FUNCS"], func=True):
                        # print("~"+str2+"~")
                        if str2.find(DOT) != -1:
                            sl = str2.split(DOT)
                            if sl[0] in self._imports_dict:
                                str2 = sl[1] + "_" + self._imports_dict[sl[0]]

                        str2 += LEFTBRACK + str2_params + RIGHTBRACK
                        # _val_idx += 2

                    val = compare_str(str1, str2) + EQUALS + EQUALS + ZERO

                    # _val_idx += 4
                    # continue
                    break

                # elif v == INPUT and tok_list[_val_idx+1] == LEFTBRACK and self.is_string(tok_list[_val_idx+2]):
                #     print("~"+v+"~")
                # user_input()
                # val += f"_bt_input({self.__bt_to_c_str(tok_list[_val_idx+2])});"

                elif self.is_string(v):
                    # print("~"+v+"~")

                    val += self.__bt_to_c_str(v)
                    str_found = True

                elif self.is_string(v, vars_dict):
                    if _global_call:
                        if v.find(DOT) == -1 and vars_dict[v][2] != "__FOR__":
                            val += self.bin_name + DOT + v

                        elif v.find(DOT) == -1 and vars_dict[v][2] == "__FOR__":
                            val += v

                        else:
                            vl = v.split(DOT)
                            if vl[0] in self._imports_dict:
                                val += self._imports_dict[vl[0]] + DOT + vl[1]

                    else:
                        # print("~"+v+"~")
                        val += v

                    str_found = True
                    # if vars_dict[v][2] == "__LIST__":
                    #     _type_suffix = "_list_t"

                    # print(_type)

                elif self.is_string(v, self._vars_dict["GLOBALS"]["global_vars"]):
                    # print("~"+v+"~")

                    if v.find(DOT) == -1 and self._vars_dict["GLOBALS"]["global_vars"][v][2] != "__FOR__":
                        val += self.bin_name + DOT + v

                    elif v.find(DOT) == -1 and self._vars_dict["GLOBALS"]["global_vars"][v][2] == "__FOR__":
                        val += v

                    else:
                        # print("~"+v+"~")
                        vl = v.split(DOT)
                        if vl[0] in self._imports_dict:
                            val += self._imports_dict[vl[0]] + DOT + vl[1]

                    if self._vars_dict["GLOBALS"]["global_vars"][v][2] == "__LIST__":
                        _type_suffix = "_list_t"

                    str_found = True

                elif self.is_string(v, self._vars_dict["FUNCS"], func=True):
                    if v.find(DOT) == -1:
                        val += v
                    else:
                        # print("~"+v+"~")
                        vl = v.split(DOT)
                        if vl[0] in self._imports_dict:
                            val += vl[1] + "_" + self._imports_dict[vl[0]]

                    if self._vars_dict["FUNCS"][v][0][2] == "__LIST__":
                        _type_suffix = "_list_t"

                    str_found = True

                else:
                    # print(v)
                    val += v

            elif v in [LEFTBRACK, RIGHTBRACK, LEFTCURL, RIGHTCURL]:

                # if v == LEFTBRACK and tok_list[-1] == RIGHTBRACK:
                # _list =
                # val += LEFTCURL

                # else:
                val += v

            elif v in ["True", "False"]:
                # print("*" * 67)
                val += v.lower()
                _type = BOOL

            elif v in [AND, OR]:
                if v == AND:
                    val += " && "

                elif v == OR:
                    val += " || "

            # 1. Check for function variable name or
            # 2. Check for global scope
            elif v in vars_dict.keys() or v in self._vars_dict["FUNCS"].keys():
                # print(v)
                if v in vars_dict.keys():

                    _ret_type = vars_dict[v][1]
                    # print(_ret_type)

                    # try:
                    if _ret_type.endswith("_list_t"):
                        _ret_type = _ret_type[:_ret_type.find("_list_t")]
                        _type_suffix = "_list_t"

                    # except AttributeError:
                    #     if _ret_type[v].endswith("_list_t"):
                    #         _ret_type = _ret_type[:_ret_type.find("_list_t")]
                    #         _type_suffix = "_list_t"

                    if _ret_type == BOOL:
                        bool_found = True

                    elif _ret_type == DOUBLE:
                        float_found = True

                    elif _ret_type == LONG:
                        int_found = True

                    elif _ret_type == STR:
                        str_found = True

                    if _global_call:
                        # if not str_found:
                        if v.find(DOT) == -1 and vars_dict[v][2] != "__FOR__":
                            val += self.bin_name + DOT + v

                        elif v.find(DOT) == -1 and vars_dict[v][2] == "__FOR__":
                            val += v

                        else:
                            vl = v.split(DOT)
                            if vl[0] in self._imports_dict:
                                val += self._imports_dict[vl[0]] + DOT + vl[1]

                    else:
                        if not str_found:
                            val += v

                # Check for function name
                elif v in self._vars_dict["FUNCS"].keys():

                    _func_ret_type = self._vars_dict["FUNCS"][v][0][1]

                    if _func_ret_type.endswith("_list_t"):
                        _func_ret_type = _func_ret_type[:_func_ret_type.find(
                            "_list_t")]
                        _type_suffix = "_list_t"

                    if _func_ret_type == BOOL:
                        bool_found = True

                    elif _func_ret_type == DOUBLE:
                        float_found = True

                    elif _func_ret_type == LONG:
                        int_found = True

                    elif _func_ret_type == STR:
                        str_found = True

                    if v.find(DOT) == -1:
                        # print(v)
                        val += v
                    else:
                        # print(v)
                        vl = v.split(DOT)
                        if vl[0] in self._imports_dict:
                            val += vl[1] + "_" + self._imports_dict[vl[0]]

            elif v in self._vars_dict["GLOBALS"]["global_vars"].keys():
                # print(v)

                if self._vars_dict["GLOBALS"]["global_vars"][v][1] == BOOL:
                    bool_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == DOUBLE:
                    float_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == LONG:
                    int_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == STR:
                    str_found = True

                if not str_found:
                    if v.find(DOT) == -1:
                        val += self.bin_name + DOT + v
                    else:
                        vl = v.split(DOT)
                        if vl[0] in self._imports_dict:
                            val += self._imports_dict[vl[0]] + DOT + vl[1]

                    # val += self.bin_name + DOT + v

            elif self.is_bool(v):
                val += v
                bool_found = True

            elif self.is_float(v):
                val += v
                float_found = True
            elif self.is_int(v):
                val += v
                int_found = True

            _val_idx += 1

        if val.find(DOT) != -1:
            # print(val)
            class_var = val.split(DOT)
            _class_var, _func = class_var[0], class_var[1]
            _func_name, _func_param = _func[:_func.find(
                LEFTBRACK)], _func[_func.find(LEFTBRACK):]
            if _class_var in self._vars_dict["GLOBALS"]["global_vars"]:
                body = self.bin_name+DOT+_class_var
                left = _func_param.find(LEFTBRACK)
                right = _func_param.find(RIGHTBRACK)+1
                if right - left != 2:
                    body += COMA + _func_param[left+1:right]
                val = self.bin_name + DOT + _class_var + "->" + \
                    _func_name + LEFTBRACK + body + RIGHTBRACK
                _type = self._class_vars_dict[self._vars_dict["GLOBALS"]
                                              ["global_vars"][_class_var][1]]["FUNCS"]["self->"+_func_name][0][1]
                # print(_type, val)
                if _type == STR:
                    str_found = True

                
                # print(val, _type)

                return (val, _type + _type_suffix)

        if str_found:
            _type = STR

        elif bool_found:
            _type = BOOL

        elif float_found:
            _type = DOUBLE

        elif int_found:
            _type = LONG

        # print(_type_suffix)
        # print(val, _type)

        return (val, _type + _type_suffix)

    def __reassign_vals(self, vars_dict, toks, _global_call):

        # t = toks[0]
        # print(toks)
        _list_count = ""
        str_to_ret = ""

        if self.is_list(toks[0]):
            _t = toks[0][:toks[0].find(LEFTSQUARE)]
            _list_count = toks[0][toks[0].find(LEFTSQUARE):]
            toks[0] = _t

        t = toks[0]

        # List append condition 'a <- 45, 55'
        if toks[1] == S_THAN and toks[2] == SUB:
            _v, _t = self.__eval_assign_values(
                vars_dict, toks, _global_call, SEMI)

            _list_var, _vals = _v.split(SUB)
            _list_var = _list_var[:-1]
            _vals_list = _vals.split(COMA)

            # Check if string
            if _vals.startswith('"'):
                for idx, v in enumerate(_vals_list):
                    # Case ',' in string
                    if not _vals_list[idx].startswith('"') and _vals_list[idx].endswith('"'):
                        if idx != 0:
                            _vals_list[idx-1] += ',' + _vals_list[idx]
                            _vals_list.pop(idx)
                    

            str_to_ret += append_list(_t, _list_var, _vals_list)

        # Check for '+=', '-=', '*=', '\=' condition
        elif toks[1] in [ADD, SUB, MUL, DIV] and toks[2] == EQUALS:

            if self._in_func_names(toks[3]):
                toks[3] = self._in_func_names(toks[3])

            # else:
            #     print(toks[3])

            val, _type = self.__eval_assign_values(
                vars_dict, toks[3:toks.index(SEMI) + 1], _global_call, SEMI)

        # '=' condition
        else:
            if self._in_func_names(toks[2]):
                toks[2] = self._in_func_names(toks[2])

            else:
                if toks[2].find(DOT) != -1:
                    l = toks[2].split(DOT)
                    # print(l)
                    if l[0] in self._imports_dict:
                        toks[2] = l[1] + "_" + self._imports_dict[l[0]]
                # print(toks[2])

            val, _type = self.__eval_assign_values(
                vars_dict, toks[2:toks.index(SEMI) + 1], _global_call, SEMI)

            # v1 = v2
            if self.is_list(val):
                new_val = val.split(LEFTSQUARE)
                _v2, _t2 = self.__eval_assign_values(
                    vars_dict, [new_val[0], SEMI], _global_call, SEMI)
                # print(_v2, _t2)
                _v2 += "->ptr" + "[" + new_val[1]
                # print(_v2)
                val = _v2

        # print(t, _list_count)

        if not _global_call and t in vars_dict.keys():
            t += _list_count
            # String or Number
            if toks[1] == ADD and toks[2] == EQUALS:
                if _type == STR:
                    str_to_ret += concat_str(t, val)

                else:
                    str_to_ret += t + ADD + EQUALS + val + SEMI + NEWLINE

            # Number
            elif toks[1] in [SUB, MUL, DIV] and toks[2] == EQUALS:
                str_to_ret += t + toks[1] + EQUALS + val + SEMI + NEWLINE

            # Case '='
            elif toks[1] == EQUALS:
                if _type == STR:
                    str_to_ret += free_str(t)
                    str_to_ret += new_str(t, val)

                else:
                    str_to_ret += t + EQUALS + val + SEMI + NEWLINE

        elif _global_call or t in self._vars_dict["GLOBALS"]["global_vars"] or t in self._vars_dict["FUNCS"]:

            if t in self._vars_dict["GLOBALS"]["global_vars"]:
                if self._vars_dict["GLOBALS"]["global_vars"][t][2] == "__LIST__":
                    t += "->ptr" + _list_count

                # print(t)

            if t.find(DOT) == -1:
                t = self.bin_name + DOT + t

            else:
                # print(t)
                tl = t.split(DOT)
                # print(tl)

                # Write correct file name from alias `t3.count = test3.count`
                if t in self._vars_dict["GLOBALS"]["global_vars"]:
                    t = self._imports_dict[tl[0]] + DOT + tl[1]

            # print(t)

            # if _list_count:
            #     t += "->ptr"+_list_count

            # String or Number
            if toks[1] == ADD and toks[2] == EQUALS:
                if _type == STR:
                    str_to_ret += concat_str(t, val)

                else:
                    str_to_ret += t + ADD + EQUALS + val + SEMI + NEWLINE

            # Number
            elif toks[1] in [SUB, MUL, DIV] and toks[2] == EQUALS:
                str_to_ret += t + toks[1] + EQUALS + val + SEMI + NEWLINE

            # Case '='
            elif toks[1] == EQUALS:
                if _type == STR:
                    # print(toks)
                    str_to_ret += free_str(t)
                    str_to_ret += new_str(t, val)
                else:
                    # print(t, _type)
                    # str_to_ret += self.bin_name + DOT + t + EQUALS + val + SEMI + NEWLINE
                    # else:
                    str_to_ret += t + EQUALS + val + SEMI + NEWLINE
        # else:
        #     print(t)

        return str_to_ret

    '''
    Make a function for each keyword and call each other in recursion
    '''

    def __let(self, vars_dict, tok_list, _global_call):
        var = tok_list[0]
        val = ""
        _type = ""
        _li_assign_idx = ""
        _dynamic_list = False
        _func_ret_list = False
        _class_found = False
        _list_len = ""
        _sub_type = ""

        if self.is_list(var):
            _list_len = var[var.find(LEFTSQUARE) + 1:var.find(RIGHTSQUARE)]
            var = var[:var.find(LEFTSQUARE)]
            # if not _list_len:
            _dynamic_list = True

        # Check if this function return a list
        if self._in_func_names(tok_list[2]):
            _f = self._in_func_names(tok_list[2])
            if self._vars_dict["FUNCS"][_f][0][2] == "__LIST__":
                # list_type
                _func_ret_list = self._vars_dict["FUNCS"][_f][0][1]

        # Check if the variable is already defined
        if var not in vars_dict.keys():

            # Make list of [val, _type] for the associated var_key in vars_dict
            vars_dict[var] = []
            assign = tok_list[1]

            if assign == EQUALS:

                # Case let 'a = nums[0]'
                if not _dynamic_list and self.is_list(tok_list[2]):
                    _li_assign_idx = tok_list[2][tok_list[2].find(
                        LEFTSQUARE) + 1:tok_list[2].find(RIGHTSQUARE)]
                    tok_list[2] = tok_list[2][:tok_list[2].find(LEFTSQUARE)]

                    # print(tok_list[2], _li_assign_idx)

                    # print(val)

                # User input
                elif tok_list[2] == INPUT and tok_list[3] == LEFTBRACK:
                    _func = False

                    if _global_call:
                        self._global_vars_list.append(f"str {var}")
                        var = self.bin_name + DOT + var
                    else:
                        _func = True

                    if self.is_string(tok_list[4]):
                        val = user_input(var, self.__bt_to_c_str(
                            tok_list[4]), func=_func)
                    else:
                        val = user_input(var, func=_func)

                    vars_dict[tok_list[0]].append(val)
                    vars_dict[tok_list[0]].append(STR)
                    vars_dict[tok_list[0]].append(False)

                    return val

                elif len(tok_list) > 1 and tok_list[2][0] == LEFTSQUARE and tok_list[2][-1] == RIGHTSQUARE:

                    val, _type = self.__eval_assign_values(
                        vars_dict, [tok_list[2], SEMI], _global_call, SEMI)
                    # print(val, _type)
                    if self.is_list(tok_list[2]):
                        _t = val[1:-1]
                        _new_list = ""

                        if _t.find(TICK) != -1:
                            _t = _t.replace(TICK, D_QUOTE)
                            _type = STR

                        for i in _t:
                            if _type == STR:
                                _new_list += i
                            else:
                                _new_list += i.replace(SPACE, "")

                        tok_list[2] = LEFTSQUARE + _new_list + RIGHTSQUARE

                        val = tok_list[2]

                elif self._in_func_names(tok_list[2]):
                    tok_list[2] = self._in_func_names(tok_list[2])
                    # print(tok_list[2])

                elif self._in_class_names(tok_list[2]):
                    _class_found = True
                    tok_list[2] = self._in_class_names(tok_list[2])
                    val = tok_list[2] + "__init__"
                    for v in tok_list[3:-1]:
                        if self.is_string(v):
                            v = self.__bt_to_c_str(v)
                        val += v
                    _type = tok_list[2]
                    # for i in self._class_vars_dict[tok_list[2]]["FUNCS"]:
                    #     # print(i)
                    #     # print(tok_list[0]+DOT+i)
                    # self._vars_dict["FUNCS"][tok_list[0]+DOT+i] = self._class_vars_dict[tok_list[2]]["FUNCS"]

                elif _type != STR:
                    # print(tok_list[2:])
                    val, _type = self.__eval_assign_values(
                        vars_dict, tok_list[2:], _global_call, SEMI)

                    # print(val, _type)

                if _type.endswith("_list_t") and not _dynamic_list:
                    _type = _type[:-len("_list_t")]

                if _li_assign_idx:
                    val += "->ptr[" + _li_assign_idx + "]"

                vars_dict[var].append(val)
                vars_dict[var].append(_type)
                if _dynamic_list or _list_len or _func_ret_list:
                    vars_dict[var].append("__LIST__")
                    # _type += ""
                else:
                    # print(var)
                    vars_dict[var].append(False)

            elif assign == COLON:
                _type = tok_list[2]

                if _type == BOOL:
                    val = "false"

                elif _type == INT:
                    _type = LONG
                    val = "0"

                elif _type == FLOAT:
                    _type = DOUBLE
                    val = "0.0f"

                elif _type == STR:
                    _type = STR
                    val = '""'

                # print(var)
                # print(val, _type)

                vars_dict[var].append(val)
                vars_dict[var].append(_type)

                if _dynamic_list or _list_len or _func_ret_list:
                    vars_dict[var].append("__LIST__")
                else:
                    vars_dict[var].append(False)

            if _global_call:

                if not _dynamic_list and not _list_len and not _func_ret_list and not _class_found:
                    self._global_vars_list.append(f"{_type} {var}")

                elif _dynamic_list:
                    self._global_vars_list.append(f"{_type}_list_t *{var}")

                elif _func_ret_list:
                    self._global_vars_list.append(f"{_func_ret_list} *{var}")

                elif _class_found:
                    self._global_vars_list.append(f"{_type} *{var}")

            # elif _global_call:
            #     self._global_vars_list.append(f"{_type} {var}")

            if _global_call:
                var = self.bin_name + DOT + var + _sub_type

            if _type == STR and not _dynamic_list and not _list_len:
                return new_str(var, val)

            elif _dynamic_list:
                if _global_call:
                    # print(_type, var, val)
                    return new_list(_type, var, val.replace(LEFTSQUARE, "").replace(RIGHTSQUARE, "").split(COMA),
                                    _reserve=_list_len)
                else:
                    # print(_type, var, val)
                    return new_list(_type, var, val.replace(LEFTSQUARE, "").replace(RIGHTSQUARE, "").split(COMA),
                                    _reserve=_list_len, _func=True)

            else:
                if _global_call:
                    return f"{var} = {val};\n"
                else:
                    return f"{_type} {var} = {val};\n"

    def __print(self, vars_dict, tok_list, _global_call, newline):

        print_str = tok_list[0]

        str_to_ret = ""

        if (self.is_string(print_str)):
            print_str = print_str[1:-1]

        elif self.is_string(print_str, vars_dict):
            # print(54654, print_str)
            print_str = vars_dict[print_str][0]
            if print_str[0] == D_QUOTE and print_str[-1] == D_QUOTE:
                print_str = print_str[1:-1]
            else:
                # Maybe a function
                print_str = LEFTCURL + print_str + RIGHTCURL

            # When empty string is found, evaluate the variable inside []
            if not print_str:
                print_str = LEFTCURL + tok_list[0] + RIGHTCURL

        elif self.is_string(print_str, self._vars_dict["GLOBALS"]["global_vars"]):
            print_str = self._vars_dict["GLOBALS"]["global_vars"][print_str][0][1:-1]
            # print(print_str)

        elif self._in_func_names(print_str):
            print_str = self._in_func_names(print_str)
            for st in tok_list[1:]:
                print_str += st

            print_str = print_str[:-2]
            print_str = LEFTCURL + print_str + RIGHTCURL

        # elif print_str.find(DOT) != -1:

        #     class_var = print_str.split(DOT)
        #     _class_var, _func = class_var[0], class_var[1]
        #     _func_name, _func_param = _func[:_func.find(LEFTBRACK)], _func[_func.find(LEFTBRACK):]
        #     if _class_var in self._vars_dict["GLOBALS"]["global_vars"]:
        #         _type = self._class_vars_dict[self._vars_dict["GLOBALS"]["global_vars"][_class_var][1]]["FUNCS"][_func_name][0][1]
        #         body = self.bin_name+DOT+_class_var
        #         left = _func_param.find(LEFTBRACK)
        #         right = _func_param.find(RIGHTBRACK)+1
        #         if right - left != 2:
        #             body += COMA + _func_param[left+1:right]
        #         # print(self._vars_dict["GLOBALS"]["global_vars"][_class_var][1])

        #         print_str = self.bin_name + DOT + _class_var + "->" + _func_name + LEFTBRACK + body + RIGHTBRACK

        else:
            print_str = LEFTCURL + print_str + RIGHTCURL

        if newline:
            str_to_ret += self.__string_parser(print_str,
                                               vars_dict, _global_call, new_line=True)
        else:
            str_to_ret += self.__string_parser(print_str,
                                               vars_dict, _global_call, new_line=False)

        return str_to_ret

    # Loops
    def __loop_until_for(self, vars_dict, tok_list, _global_call):

        loop_head = ""
        str_to_ret = ""

        if tok_list[0] == LOOP and tok_list[1] == LEFTCURL:
            loop_head = WHILE + SPACE + "(1)" + NEWLINE + LEFTCURL

        elif tok_list[0] == LOOP and tok_list[1] == UNTIL:
            loop_head = WHILE + SPACE
            _val, _type = self.__eval_assign_values(
                vars_dict, tok_list[2:], _global_call, LEFTCURL)

            if tok_list[2] != LEFTBRACK:
                loop_head += LEFTBRACK
                str_to_ret += _val + RIGHTBRACK + NEWLINE + LEFTCURL + NEWLINE

            else:
                str_to_ret += _val + NEWLINE + LEFTCURL + NEWLINE

        start = tok_list.index(LEFTCURL) + 1
        sub_toks = []

        while start < len(tok_list):

            if tok_list[start] == LOOP:
                str_to_ret += self.__loop_until_for(
                    vars_dict, tok_list[start:], _global_call)
                break

            elif tok_list[start] in [IF, ELIF, ELSE]:
                str_to_ret += self.__if_elif_else(vars_dict,
                                                  tok_list[start:], _global_call)
                break

            elif tok_list[start] == RIGHTCURL:
                str_to_ret += tok_list[start]
                start += 1

            elif tok_list[start] != SEMI:

                sub_toks.append(tok_list[start])
                start += 1

            elif tok_list[start] == SEMI:

                sub_toks.append(tok_list[start])
                str_to_ret += self._convert_to_c_str(
                    [sub_toks], vars_dict, _global_call)
                sub_toks.clear()

                start += 1

        return loop_head + str_to_ret

    # Determine the control type (if/elif/else)

    def __if_elif_else(self, vars_dict, tok_list, _global_call):

        single_line = False
        left_brack = ""
        right_brack = ""
        str_to_ret = ""

        if tok_list[0] in [IF, ELIF, ELSE]:
            if tok_list[0] == ELIF:
                tok_list[0] = ELSE_IF

        if tok_list[0] != ELSE:

            if tok_list[1] != LEFTBRACK:
                left_brack = LEFTBRACK
                right_brack = RIGHTBRACK

            str_to_ret += tok_list[0] + SPACE + left_brack

            # Multi-line body
            if LEFTCURL in tok_list[1:]:
                # print(tok_list[1:])
                _val, _type = self.__eval_assign_values(
                    vars_dict, tok_list[1:], _global_call, LEFTCURL)

                str_to_ret += _val + right_brack + NEWLINE + LEFTCURL + NEWLINE

            # @ TODO
            # # Single-line body
            # else:
            #     single_line = True
            #     _idx = tok_list[1:].index(SEMI)
            #     _val, _type = self.__eval_assign_values(
            #         vars_dict, tok_list[1:_idx+1], _global_call, tok_list[_idx])
            #     str_to_ret += _val + right_brack + \
            #         SPACE + tok_list[_idx] + SEMI + NEWLINE

        # Else Condition
        else:
            # Multi-line body
            if LEFTCURL in tok_list[1:]:
                str_to_ret += tok_list[0] + SPACE + LEFTCURL + NEWLINE

            # @ TODO
            # # Single-line body
            # else:
            #     single_line = True
            #     _val, _type = self.__eval_assign_values(vars_dict, tok_list[1:], _global_call, SEMI)
            #     str_to_ret += tok_list[0] + SPACE + _val + SEMI + NEWLINE

        if not single_line:
            start = tok_list.index(LEFTCURL) + 1
            sub_toks = []

        else:
            start = tok_list.index(SEMI) + 1
            sub_toks = []

        while start < len(tok_list):

            if tok_list[start] in [IF, ELIF, ELSE]:
                str_to_ret += self.__if_elif_else(vars_dict,
                                                  tok_list[start:], _global_call)
                break

            elif tok_list[start] == LOOP:
                str_to_ret += self.__loop_until_for(
                    vars_dict, tok_list[start:], _global_call)
                break

            elif tok_list[start] == FOR:
                str_to_ret += self.__for(vars_dict,
                                         tok_list[start:], _global_call)
                break

            elif tok_list[start] == RIGHTCURL:
                str_to_ret += tok_list[start]
                start += 1

            elif tok_list[start] != SEMI:

                sub_toks.append(tok_list[start])
                start += 1

            elif tok_list[start] == SEMI:

                sub_toks.append(tok_list[start])
                str_to_ret += self._convert_to_c_str(
                    [sub_toks], vars_dict, _global_call)
                sub_toks.clear()

                start += 1

        return str_to_ret

    def __sleep(self, vars_dict, tok_list, _global_call):
        _val, _type = self.__eval_assign_values(
            vars_dict, tok_list, _global_call, SEMI)
        if _val[0] == LEFTBRACK and _val[-1] == RIGHTBRACK:
            return f"sleep{_val};"
        else:
            return f"sleep({_val});\n"

    def __usleep(self, vars_dict, tok_list, _global_call):
        _val, _type = self.__eval_assign_values(
            vars_dict, tok_list, _global_call, SEMI)
        if _val[0] == LEFTBRACK and _val[-1] == RIGHTBRACK:
            return f"usleep{_val};"
        else:
            return f"usleep({_val});\n"

    def _in_func_names(self, name):
        if name + "_" + self.bin_name in self._vars_dict["FUNCS"]:
            return name + "_" + self.bin_name
        return False

    def _in_class_names(self, name):
        if name + "_" + self.bin_name in self._class_vars_dict:
            return name + "_" + self.bin_name
        return False

    def __class(self, toks):

        class_type = toks[0]

        class_name = toks[2] + "_" + self.bin_name
        class_struct_str = ""
        class_init_str = ""

        # self._class_vars_dict["GLOBALS"] = {"global_vars":{}}
        self._class_vars_dict[class_name] = {
            "FUNCS": {},
            "GLOBALS": {
                "global_vars": {}
            },
            "INHERITED_CLASSES": []
        }

        __init = ""

        # if class_type == PUB_FUNC:
        #     print("PUBLIC")
        # elif class_type == FUNCTION:
        #     print("PRIVATE")

        end_param_idx = toks.index(RIGHTBRACK)
        param_toks = toks[4:end_param_idx]
        # print(param_toks)

        # param_toks = param_toks[end_param_idx:]

        count = 0
        param_list = False

        # Get the class global variables
        while count < len(param_toks):
            if param_toks[count] == PUB_FUNC or param_toks[count] == FUNCTION:
                var_type = param_toks[count]
                var = param_toks[count + 1]
                val = ""
                _type = param_toks[count + 3]
                if var_type == FUNCTION:
                    var = "__" + var

                _sub_t = False

                if var.endswith("[]"):
                    var = var[:var.find(LEFTSQUARE)]
                    _sub_t = "__LIST__"
                    param_list = True

                if _type == INT:
                    _type = LONG
                    val = "0"

                elif _type == FLOAT:
                    _type = DOUBLE
                    val = "0.0f"

                elif _type == STR:
                    val = ""

                if param_list:
                    param_list = False
                    _type += "_list_t"

                class_struct_str += f"{_type} {var};\n"
                self._class_vars_dict[class_name]["GLOBALS"]["global_vars"]["self->" + var] = [
                    val, _type, _sub_t]
                # self._class_vars_dict[class_name]["FUNCS"][var] = [(), {}]
                # print(var_type, var, val, _type, _sub_t)

            count += 1

        inh_classes = end_param_idx
        multiple_classes = False

        # print(toks[inh_classes:])

        if toks[inh_classes + 1] != LEFTCURL:
            inh_classes += 1
            while inh_classes < len(toks):
                if toks[inh_classes] == "<" and toks[inh_classes + 1] == "-":
                    inh_classes += 2
                    self._class_vars_dict[class_name]["INHERITED_CLASSES"].append(
                        toks[inh_classes] + "_" + self.bin_name)
                elif toks[inh_classes] == COMA:
                    inh_classes += 1
                    multiple_classes = True

                if multiple_classes:
                    multiple_classes = False
                    self._class_vars_dict[class_name]["INHERITED_CLASSES"].append(
                        toks[inh_classes] + "_" + self.bin_name)

                if toks[inh_classes] == LEFTCURL and (toks[inh_classes + 1] == "__init__" or
                                                      toks[inh_classes + 1] == PUB_FUNC or toks[
                                                          inh_classes + 1] == FUNCTION):
                    break

                inh_classes += 1

            inh_classes += 1

            end_param_idx = inh_classes

            # print(toks[end_param_idx:])
            toks = toks[end_param_idx:]
            # toks.insert(0, FUNCTION)
            end_param_idx += 1

            # print(toks)
        else:
            # Exclude last `}`
            toks = toks[end_param_idx + 2:-1]
            # print(toks)

        # Get function type, name, params, return type
        # print(toks)
        count = 0
        func_toks = []
        while count < len(toks):
            _func_toks = []
            if toks[count] == PUB_FUNC or toks[count] == FUNCTION:
                while toks[count] != RIGHTCURL and (toks[count+1] != FUNCTION or toks[count+1] != PUB_FUNC):
                    _func_toks.append(toks[count])
                    count += 1
                func_toks.append(_func_toks)
                
            count += 1
        # print(func_toks)

        for func in func_toks:
            _func_type = func[0]
            # _func_name = class_name + "_" + func[1]
            _func_name = func[1]
            __func_param_end_idx = func.index(RIGHTBRACK)
            _func_params = func[3:__func_param_end_idx]
            _func_ret_type = func[func.index(RIGHTBRACK)+2:func.index(LEFTCURL)]
            func_ret_type = ""
            for i in _func_ret_type:
                func_ret_type += i
            print(_func_type, _func_name, _func_params, _func_ret_type)

            return_list = False
            _sub_type = False
            ret_val = ""

            if not func_ret_type or func_ret_type == COLON or func_ret_type == RIGHTBRACK:
                func_ret_type = VOID

            if func_ret_type.endswith("[]"):
                func_ret_type = func_ret_type[:func_ret_type.find(LEFTSQUARE)]
                _sub_type = "__LIST__"
                return_list = True

            if func_ret_type == INT:
                func_ret_type = LONG
                ret_val = "0"

            elif func_ret_type == FLOAT:
                func_ret_type = DOUBLE
                ret_val = "0.0f"

            elif func_ret_type == STR:
                ret_val = ""

            if return_list:
                func_ret_type += "_list_t"


            count = 0
            # print("self->"+_func_name, ret_val, func_ret_type, _sub_type, _func_type)
            self._class_vars_dict[class_name]["FUNCS"]["self->"+_func_name] = [(ret_val, func_ret_type, _sub_type, _func_type), {"__FUNC_PARAMS__":_func_params}]
            self._class_vars_dict[class_name]["FUNCS"]["self->"+_func_name][1].update(
                self._class_vars_dict[class_name]["GLOBALS"]["global_vars"])
            
            # print(_func_name, self._class_vars_dict[class_name]["FUNCS"][_func_name])
            print(self._class_vars_dict[class_name]["FUNCS"]["self->"+_func_name])
            print("\n")

            while count < len(func):

                count += 1

        count = 0
        closing = 0
        start = 0
        functions = []
        init_found = False

        while count < len(toks):

            # if toks[count] == "__init__":
            #     init_found = True
            #     # toks.insert(count + 1, LEFTBRACK)
            #     # toks.insert(count + 2, RIGHTBRACK)
            #     # toks.insert(count + 3, COLON)
            #     # toks.insert(count + 4, class_name + " *")

            #     _param_toks_idx = count + 1
            #     for i in param_toks:
            #         if i not in [FUNCTION, PUB_FUNC]:
            #             toks.insert(_param_toks_idx, i)
            #         _param_toks_idx += 1
            #     start = count

            #     # print(toks)

            if toks[count] == PUB_FUNC or toks[count] == FUNCTION:
                start = count

            elif toks[count].startswith(DOT):
                # print(toks[count].split(DOT))
                _temp = "self->" + toks[count].split(DOT)[1]
                # if toks[count].split(DOT)[1] in self._class_vars_dict[class_name]["FUNCS"]:
                # print(self._class_vars_dict[class_name]["FUNCS"])
                # print(self._class_vars_dict[class_name]["FUNCS"][toks[count].split(DOT)[1]][0])
                # self._class_vars_dict[class_name]["GLOBALS"]["global_vars"][_temp] = self._class_vars_dict[class_name]["FUNCS"][toks[count].split(DOT)[1]][0]
                # print(toks[count])
                # print(self._class_vars_dict[class_name]["FUNCS"])
                toks[count] = _temp
                # print(toks[count])

            elif toks[count] == LEFTCURL:
                closing += 1

            elif toks[count] == RIGHTCURL:
                closing -= 1

                if closing == 0:
                    _func = toks[start:count + 1]
                    if init_found:
                        _func.insert(0, PUB_FUNC)

                if not init_found:
                    func_name = class_name + "_" + \
                        _func[1] + "_" + self.bin_name
                    functions.append((_func[1], _func))
                    # self._class_vars_dict[class_name]["FUNCS"][_func[1]] = [(), {
                    # }]
                    # self._class_vars_dict[class_name]["FUNCS"][_func[1]][1].update(
                        # self._class_vars_dict[class_name]["GLOBALS"]["global_vars"])
                else:
                    init_found = False
                    _func = toks[start:count + 1]
                    # _func.insert(0, "__init__")
                    func_name = class_name + "__init__"
                    functions.append((func_name, _func))
                    # self._class_vars_dict[class_name]["FUNCS"][func_name] = [(), {
                    # }]
                    # self._class_vars_dict[class_name]["FUNCS"][func_name][1].update(
                        # self._class_vars_dict[class_name]["GLOBALS"]["global_vars"])

                    if _func[0] == FUNCTION:
                        func_name = "__" + func_name

                    # class_struct_str += f"{_type} {var};\n"

            count += 1


        class_vars_str = ""
        class_init_vars_str = ""

        for index, i in enumerate(self._class_vars_dict[class_name]["GLOBALS"]["global_vars"]):
            var_dict = self._class_vars_dict[class_name]["GLOBALS"]["global_vars"][i]
            if index < len(self._class_vars_dict[class_name]["GLOBALS"]["global_vars"]) - 1:
                class_vars_str += f"{var_dict[1]} {i[i.rfind('>') + 1:]}, "
            elif index == len(self._class_vars_dict[class_name]["GLOBALS"]["global_vars"]) - 1:
                class_vars_str += f"{var_dict[1]} {i[i.rfind('>') + 1:]}"

            # Type of global variable
            if var_dict[1] != STR and var_dict[2] != "__LIST__":
                class_init_vars_str += f"{i} = {i[i.rfind('>') + 1:]};\n"

            elif var_dict[1] == STR and var_dict[2] != "__LIST__":
                class_init_vars_str += new_str(i, i[i.rfind('>') + 1:])

            # elif var_dict[1] != STR and var_dict[2] == "__LIST__":
            #     class_init_vars_str += new_list()

        class_init_str += f"{class_name} *{class_name}__init__({class_vars_str})\n" + \
            LEFTCURL + NEWLINE

        if class_type == FUNCTION:
            self._private_func_list.append(
                f"{class_name} *{class_name}__init__({class_vars_str});")
        elif class_type == PUB_FUNC:
            self._public_func_list.append(
                f"{class_name} *{class_name}__init__({class_vars_str});")

        class_init_str += f"{class_name} *self = calloc(1, sizeof({class_name}));\n"
        class_init_str += class_init_vars_str

        _class_funcs = []

        for f in functions:
            _class_funcs.append("self->" + f[0])

        for f in functions:
            if f[1][0] == "__init__":
                self.__func(f[0], f[1], class_name)

            if f[1][0] == FUNCTION and f[1][1] != "__init__":
                class_struct_str += self.__func(f[0], f[1], class_name)
                class_init_str += f"self->{f[0]} = __{class_name}_{f[0]};\n"

            elif f[1][0] == PUB_FUNC and f[1][1] != "__init__":
                class_struct_str += self.__func(f[0], f[1], class_name)
                class_init_str += f"self->{f[0]} = {class_name}_{f[0]};\n"

        class_init_str += "return self;\n"
        class_init_str += RIGHTCURL + NEWLINE

        class_struct_str = f"""typedef struct {class_name}
{{
{class_struct_str}
}}{class_name};
"""

        self._funcs_impl.append(class_init_str)

        self._class_structs.append(class_struct_str)


    def __func(self, current_func, toks, class_name=None):

        c_func_params = ""
        return_list = False

        class_struct_str = ""

        if not class_name:
            current_func += "_" + self.bin_name
            func_dict = self._vars_dict["FUNCS"]

        else:
            func_dict = self._class_vars_dict[class_name]

        if not current_func in func_dict or class_name:
            func_type = toks[0]

            if not class_name:
                func_dict.update({current_func: [(), {}]})

            # print(toks)
            func_body_toks = toks[toks.index(LEFTCURL) + 1:-1]
            _sub_type = False
            if not class_name:
                prms_and_ret = toks[toks.index(LEFTBRACK): toks.index(LEFTCURL)]
                params = prms_and_ret[prms_and_ret.index(
                    LEFTBRACK) + 1: prms_and_ret.index(RIGHTBRACK)]

                # func_body_toks = toks[toks.index(LEFTCURL) + 1:-1]

                # Extract return type and value
                return_type = prms_and_ret[-1]
                ret_val = ""
                # _sub_type = False

                if return_type == COLON or return_type == RIGHTBRACK:
                    return_type = VOID

                if return_type.endswith("[]"):
                    return_type = return_type[:return_type.find(LEFTSQUARE)]
                    _sub_type = "__LIST__"
                    return_list = True

                if return_type == INT:
                    return_type = LONG
                    ret_val = "0"

                elif return_type == FLOAT:
                    return_type = DOUBLE
                    ret_val = "0.0f"

                elif return_type == STR:
                    ret_val = ""

                if return_list:
                    return_type += "_list_t"

                # func_type can be `@` or `<`
                func_dict[current_func][0] = [
                ret_val, return_type, _sub_type, func_type]

            else:
                return_type = func_dict["FUNCS"]["self->"+current_func][0][1]
                # print(i, self._class_vars_dict[class_name]["FUNCS"]["self->"+current_func])
                # for i in self._class_vars_dict[class_name]["FUNCS"]:
                print(self._class_vars_dict[class_name]["FUNCS"]["self->"+current_func][1])
                params = self._class_vars_dict[class_name]["FUNCS"]["self->"+current_func][1]["__FUNC_PARAMS__"]
                # del self._class_vars_dict[class_name]["FUNCS"]["self->"+current_func][1]["__FUNC_PARAMS__"]

            if not current_func.endswith("__init__"):
                class_struct_str += f"{return_type} (*{current_func})(struct {class_name} *self"
            else:
                class_struct_str += f"{return_type} (*{current_func})("

            
            # if not class_name:
            if params and params[0] != ":":
                # Extract param vars and types and skip if no params
                _idx = 0
                param_list = False
                while (_idx < len(params)):
                    var = params[_idx]
                    _type = params[_idx + 2]
                    val = ""
                    _sub_t = False

                    if var.endswith("[]"):
                        var = var[:var.find(LEFTSQUARE)]
                        _sub_t = "__LIST__"
                        param_list = True

                    if _type == INT:
                        _type = LONG
                        val = "0"

                    elif _type == FLOAT:
                        _type = DOUBLE
                        val = "0.0f"

                    elif _type == STR:
                        val = ""

                    if param_list:
                        param_list = False
                        _type += "_list_t"

                    class_struct_str += f", {_type} {var}"
                    if class_name:
                        func_dict["FUNCS"]["self->"+current_func][1][var] = (val, _type, _sub_t)
                    else:
                        func_dict[current_func][1][var] = (val, _type, _sub_t)


                    # if _type == STR:
                    #     _type = CHARSTAR

                    if _sub_t == "__LIST__":
                        c_func_params += f"{_type} *{var}"

                    else:
                        c_func_params += f"{_type} {var}"

                    # To exclude comma after last param
                    if _idx < len(params) - 3:
                        class_struct_str += ", "
                        c_func_params += ", "
                    _idx += 4
            # else:
                # print(self._class_vars_dict[class_name]["FUNCS"][current_func][1]["__FUNC_PARAMS__"])
                # for _type, var in self._class_vars_dict[class_name]:
                    # print(_type, var)

            class_struct_str += ");\n"

            # print(class_struct_str)

            start = 0
            sub_toks = []
            str_to_ret = ""

            while start < len(func_body_toks):

                if func_body_toks[start] in [IF, ELIF, ELSE]:
                    str_to_ret += self.__if_elif_else(
                        func_dict[current_func][1], func_body_toks[start:], _global_call=False)
                    break

                elif func_body_toks[start] == LOOP:
                    str_to_ret += self.__loop_until_for(
                        func_dict[current_func][1], func_body_toks[start:], _global_call=False)
                    break

                elif func_body_toks[start] == FOR:
                    str_to_ret += self.__for(func_dict[current_func]
                                             [1], func_body_toks[start:], _global_call=False)
                    break

                elif func_body_toks[start] != SEMI:

                    sub_toks.append(func_body_toks[start])
                    start += 1

                elif func_body_toks[start] == SEMI:

                    sub_toks.append(func_body_toks[start])
                    if not class_name:
                        str_to_ret += self._convert_to_c_str(
                            [sub_toks], func_dict[current_func][1], _global_call=False)

                        # print(sub_toks)
                    else:
                        str_to_ret += self._convert_to_c_str(
                            [sub_toks], func_dict, _global_call=False)

                    sub_toks.clear()


                    start += 1

            # print(return_type)

            if return_type == STR and _sub_type != "__LIST__":
                pass

            elif return_type == STR and _sub_type == "__LIST__":
                return_type = STR + "*"

            elif _sub_type == "__LIST__":
                return_type += "*"

            if class_name:
                if func_type == FUNCTION:
                    current_func = f"__{class_name}_{current_func}"

                elif func_type == PUB_FUNC:
                    current_func = f"{class_name}_{current_func}"

                if c_func_params:
                    if not current_func.endswith("__init__"):
                        c_func_params = f"struct {class_name} *self, {c_func_params}"
                    else:
                        c_func_params = f"{c_func_params}"

                else:
                    if not current_func.endswith("__init__"):
                        c_func_params = f"struct {class_name} *self"
                    # else:
                    # c_func_params = f"struct {class_name} *self"

            func = f"{return_type} {current_func}({c_func_params})" + \
                   NEWLINE + LEFTCURL + NEWLINE

            func += str_to_ret + NEWLINE + RIGHTCURL + NEWLINE

            self._funcs_impl.append(func)

            if func_type == FUNCTION:
                self._private_func_list.append(
                    f"{return_type} {current_func}({c_func_params});")
            elif func_type == PUB_FUNC:
                self._public_func_list.append(
                    f"{return_type} {current_func}({c_func_params});")

        if class_name:
            return class_struct_str

    def __return(self, vars_dict, tok_list):

        ret_val, _type = self.__eval_assign_values(
            vars_dict, tok_list, False, SEMI)

        # print(ret_val)
        if ret_val[0] != LEFTSQUARE and self.is_list(ret_val):
            _list = ret_val.split(LEFTSQUARE)
            new_name = _list[0] + "->ptr[" + _list[1]

            ret_val = new_name

        ret_val = RETURN + SPACE + ret_val + SEMI

        return ret_val

    def __string_parser(self, string, vars_dict, _global_call, new_line=False):

        print_head = 'printf("'
        print_tail = ');\n'

        result = print_head
        frmt = ""
        values = ""

        length = len(string)
        left = 0
        right = 0

        box_started = False

        while (right < length):

            c = string[right]

            if not box_started:
                if c == LEFTCURL and string[right - 1] != BACKSLASH:
                    left = right + 1
                    box_started = True

                # elif c == BACKSLASH and string[right+1] == LEFTCURL or\
                #     string[right+1] == RIGHTCURL:
                #     # frmt += string[right+1]
                #     pass

                elif c == NEWLINE:
                    frmt += "\\n"

                # Get the values between box to determine var, func
                # TODO support arithmetic operations inside box. EXAMPLES: [1+3], [`> ` * 3]
                else:
                    frmt += c

            else:
                if c == RIGHTCURL and string[right - 1] != BACKSLASH:
                    var = self.sub_string(string, left, right)
                    # Remove \[ and \] from substring
                    _li_conts = ""
                    if LEFTSQUARE in var or RIGHTSQUARE in var:
                        var = var.replace(BACKSLASH, "")
                        if LEFTSQUARE in var and RIGHTSQUARE in var:
                            _li_conts = var[var.find(
                                LEFTSQUARE) + 1:var.find(RIGHTSQUARE)]
                            _v, t = self.__eval_assign_values(
                                vars_dict, [_li_conts, SEMI], _global_call, SEMI)
                            _li_conts = "->ptr" + LEFTSQUARE + _v + RIGHTSQUARE
                        var = var[:var.find(LEFTSQUARE)]

                    var_list = [var, ()]
                    val, _type = self.__eval_assign_values(
                        vars_dict, var_list, _global_call, SEMI)

                    # print(val, _type)

                    # if _type.endswith("__LIST__"):
                    #     _type = _type[:_type.find("__LIST__")]

                    # elif _type.endswith("__LIST_DY__"):
                    #     _type = _type[:_type.find("__LIST_DY__")]

                    # elif _type.endswith("__LIST_ST__"):
                    #     _type = _type[:_type.find("__LIST_ST__")]

                    # Type

                    # if val.find(DOT) != -1:
                    #     class_var = val.split(DOT)
                    #     _class_var, _func = class_var[0], class_var[1]
                    #     _func_name, _func_param = _func[:_func.find(LEFTBRACK)], _func[_func.find(LEFTBRACK):]
                    #     if _class_var in self._vars_dict["GLOBALS"]["global_vars"]:
                    #         _type = self._class_vars_dict[self._vars_dict["GLOBALS"]["global_vars"][_class_var][1]]["FUNCS"][_func_name][0][1]
                    #         body = self.bin_name+DOT+_class_var
                    #         left = _func_param.find(LEFTBRACK)
                    #         right = _func_param.find(RIGHTBRACK)+1
                    #         if right - left != 2:
                    #             body += COMA + _func_param[left+1:right]
                    #         # print(self._vars_dict["GLOBALS"]["global_vars"][_class_var][1])

                    #         val = self.bin_name + DOT + _class_var + "->" + _func_name + LEFTBRACK + body + RIGHTBRACK
                    # print(self.bin_name+DOT+_class_var+"->"+_func)
                    # print(_func_param)
                    # print(val)
                    # print(frmt)

                    if _type.endswith("_list_t"):
                        _type = _type[:_type.find("_list_t")]

                    if _type == LONG:
                        if val.find(SUB) != -1:
                            frmt += "%d"
                        else:
                            frmt += "%ld"

                    elif _type == BOOL:
                        frmt += "%d"

                    elif _type == DOUBLE:
                        frmt += "%f"
                    elif _type == STR:
                        frmt += "%s"

                    if _li_conts:
                        # _li_conts += SEMI
                        # print(_li_conts)
                        # v = self._convert_to_c_str([[_li_conts]], vars_dict, _global_call)
                        # print(v)
                        values += COMA + val + _li_conts
                    else:
                        values += COMA + val

                    box_started = False

            right += 1
        result += frmt
        if new_line:
            result += '\\n"'
        else:
            result += '"'

        result += values + print_tail

        # print(frmt)

        return result

    def __for(self, vars_dict, toks, _global_call):
        str_to_ret = ""
        _k = "_i_"
        _v = ""
        _obj = ""

        for_body_toks = []

        if toks[2] == IN:
            _v = toks[1]
            _obj = toks[3]
            for_body_toks = toks[4:-1]

        elif toks[4] == IN:
            _k = toks[1]
            _v = toks[3]
            _obj = toks[5]
            for_body_toks = toks[6:-1]

            # print(for_body_toks)

        _start = None
        _end = None

        if _obj.endswith(RIGHTSQUARE):
            _sliced_str = _obj[_obj.find(
                LEFTSQUARE) + 1:_obj.find(RIGHTSQUARE)]
            _obj = _obj[:_obj.find(LEFTSQUARE)]

            _v_, _t_ = self.__eval_assign_values(
                vars_dict, [_sliced_str, ()], _global_call, SEMI)

            if _v_.find(COLON) != -1:
                _start, _end = _v_.split(COLON)

        val, _type = self.__eval_assign_values(
            vars_dict, [_obj, ()], _global_call, SEMI)

        if not _type or vars_dict[_obj][1].endswith("_list_t"):
            _type = vars_dict[_obj][1][:vars_dict[_obj][1].find("_list_t")]

        # This is to ensure val == _obj as eval assign values doesn't catch this when string found        
        if val == "":
            val = _obj

        if _end:
            if _end.startswith(SUB):
                _end = val + "->len" + _end

        if _start:
            if _start.startswith(SUB):
                _start = val + "->len" + _start

        vars_dict.update({_v: [_v, _type, "__FOR__"]})
        # print(_type)

        for_body = ""

        start = 1
        sub_toks = []
        while start < len(for_body_toks):

            if for_body_toks[start] == FOR:
                for_body += self.__for(vars_dict,
                                       for_body_toks[start:], _global_call)
                break

            elif for_body_toks[start] in [IF, ELIF, ELSE]:
                for_body += self.__if_elif_else(vars_dict,
                                                for_body_toks[start:], _global_call)
                break

            elif for_body_toks[start] == LOOP:
                for_body += self.__loop_until_for(
                    vars_dict, for_body_toks[start:], _global_call)
                break

            elif for_body_toks[start] == RIGHTCURL:
                for_body += for_body_toks[start]
                start += 1

            elif for_body_toks[start] != SEMI:

                sub_toks.append(for_body_toks[start])
                start += 1

            elif for_body_toks[start] == SEMI:

                sub_toks.append(for_body_toks[start])
                for_body += self._convert_to_c_str(
                    [sub_toks], vars_dict, _global_call)
                sub_toks.clear()

                start += 1

        str_to_ret += access_elem_by_ref(_type,
                                         _k, _v, val, for_body, _start, _end)

        return str_to_ret

    def _convert_to_c_str(self, tokens, vars_dict, _global_call=True):

        c_str = ""

        # print(tokens, vars_dict)
        # print(vars_dict)
        tokens = iter(tokens)
        for toks in tokens:
            for idx, t in enumerate(toks):

                if t.endswith("]"):
                    c_str += self.__reassign_vals(vars_dict,
                                                  toks, _global_call)
                    break

                if self._in_func_names(t):
                    t = self._in_func_names(t)

                if t == IMPORT:

                    from .bt_to_c import BT_to_C

                    import_name = toks[idx + 1]
                    try:
                        imp_file_path = self.bt_file_path[:self.bt_file_path.rindex(
                            "/") + 1] + import_name + ".bt"
                    except ValueError:
                        imp_file_path = "./" + import_name + ".bt"

                    source = BT_to_C(imp_file_path, main_file=False)

                    self._includes.append(f'#include "{import_name}.h"')
                    c_str += f"main_{import_name}(argc, argv);" + NEWLINE

                    import_alias = import_name
                    if toks[idx + 2] == AS:
                        import_alias = toks[idx + 3]

                    new_glbl_dict = dict()
                    for k, v in source._vars_dict["GLOBALS"]["global_vars"].items():
                        new_k = import_alias + DOT + k
                        new_glbl_dict[new_k] = v

                    new_funcs_dict = dict()
                    for k, v in source._vars_dict["FUNCS"].items():
                        if k.endswith("_" + import_name) and source._vars_dict["FUNCS"][k][0][3] == PUB_FUNC:
                            new_k = import_alias + DOT + \
                                k[:k.rfind("_" + import_name)]
                            new_funcs_dict[new_k] = v

                    self._imports_dict[import_alias] = import_name
                    self._vars_dict["GLOBALS"]["global_vars"].update(
                        new_glbl_dict)
                    self._vars_dict["FUNCS"].update(new_funcs_dict)

                    break

                elif t.find(DOT) != -1 and t not in self._vars_dict["GLOBALS"]["global_vars"] and \
                        t not in self._vars_dict["FUNCS"] and not self.is_float(t):

                    print(f"{t} not Found!")
                    break

                elif t == FUNCTION or t == PUB_FUNC and toks[idx + 1] != SUB and toks[idx + 1] != CLASS:
                    current_func = toks[idx + 1]
                    self.__func(current_func, toks)

                    break

                elif t == FUNCTION or t == PUB_FUNC and toks[idx + 1] != SUB and toks[idx + 1] == CLASS:

                    # print(toks)
                    self.__class(toks)

                    break

                elif self.is_keyword(t):

                    # LET
                    if t == LET:
                        # print(toks[idx+1])
                        c_str += self.__let(vars_dict,
                                            toks[idx + 1:], _global_call)

                    # IF ELIF ELSE
                    elif t in [IF, ELIF, ELSE]:
                        c_str += self.__if_elif_else(vars_dict,
                                                     toks, _global_call)
                        break

                    elif t == LOOP:
                        c_str += self.__loop_until_for(vars_dict,
                                                       toks, _global_call)

                    elif t == FOR:
                        # print(toks)
                        c_str += self.__for(vars_dict, toks, _global_call)

                    elif t == BREAK:
                        c_str += BREAK + SEMI + NEWLINE

                    elif t == RETURN:
                        c_str += self.__return(vars_dict,
                                               toks[idx + 1:toks.index(SEMI) + 1])

                    break

                # Check if the name already exist as func_name and var both
                elif t in self._vars_dict["GLOBALS"]["global_vars"].keys() and t in self._vars_dict["FUNCS"].keys() and \
                        toks[idx + 1] == LEFTBRACK:
                    print("A `function name` cannot be similar to a `global variable`")
                    return ""

                # While reassigning varibles, check for varibale scope or if it is a function
                elif (t in vars_dict.keys() and toks[idx + 1] == EQUALS) or \
                        (t in vars_dict.keys() and toks[idx + 1] in [ADD, SUB, MUL, DIV, S_THAN] and toks[idx + 2] in [
                            EQUALS, SUB]) or \
                        (t in self._vars_dict["GLOBALS"]["global_vars"].keys() and toks[idx + 1] == EQUALS) or \
                        (t in self._vars_dict["GLOBALS"]["global_vars"].keys() and toks[idx + 1] in [ADD, SUB, MUL, DIV,
                                                                                                     S_THAN] and toks[
                            idx + 2] in [EQUALS, SUB]):
                    c_str += self.__reassign_vals(vars_dict,
                                                  toks, _global_call)
                    break

                elif t in self._vars_dict["FUNCS"].keys() and toks[idx + 1] == LEFTBRACK:
                    # Get function variables dict on index[1] with "var": (val, type) pairs
                    _vars_dict = self._vars_dict["FUNCS"][t][1]
                    _val, _type = self.__eval_assign_values(
                        _vars_dict, toks[:toks.index(SEMI) + 1], _global_call, SEMI)
                    c_str += _val + SEMI + NEWLINE
                    break
                
                # Class Functions
                elif "FUNCS" in vars_dict and t in vars_dict["FUNCS"].keys() and toks[idx + 1] == LEFTBRACK:
                    # Get function variables dict on index[1] with "var": (val, type) pairs
                    # print(vars_dict)
                    if toks[idx+2] == RIGHTBRACK:
                        toks.insert(idx+2, "self")
                    elif toks[idx+2] != RIGHTBRACK:
                        toks.insert(idx+2, "self, ")

                    _vars_dict = vars_dict["FUNCS"][t][1]
                    _val, _type = self.__eval_assign_values(
                        _vars_dict, toks[:toks.index(SEMI) + 1], _global_call, SEMI)
                    c_str += _val + SEMI + NEWLINE
                    break
                
                # Class Global variables
                elif "GLOBALS" in vars_dict and t in vars_dict["GLOBALS"]["global_vars"].keys():
                    _vars_dict = vars_dict["GLOBALS"]["global_vars"]

                    _val, _type = self.__eval_assign_values(
                        _vars_dict, toks[:toks.index(SEMI) + 1], _global_call, SEMI)

                    c_str += _val + SEMI + NEWLINE
                

                # elif toks[idx + 1] == LEFTBRACK:
                #     for _class in self._class_vars_dict:
                #         if t in self._class_vars_dict[_class]["FUNCS"]:
                #             # Get function variables dict on index[1] with "var": (val, type) pairs
                #             _vars_dict = self._class_vars_dict[_class]["FUNCS"]
                #             _val, _type = self.__eval_assign_values(
                #                 _vars_dict, toks[:toks.index(SEMI) + 1], _global_call, SEMI)
                #             c_str += _val + SEMI + NEWLINE
                #             break
                    

                elif t.find(DOT) != -1:
                    # print(t)
                    toks[0] = toks[0].split(
                        DOT)[0] + "->" + toks[0].split(DOT)[1]
                    _var = t.split(DOT)[0]
                    # print(_var)
                    if _var in self._vars_dict["GLOBALS"]["global_vars"].keys() and toks[idx + 1] == LEFTBRACK:
                        if self._vars_dict["GLOBALS"]["global_vars"][_var][1] in self._class_vars_dict:
                            toks.insert(idx+2, self.bin_name+DOT+_var)
                            # print(toks)
                            if toks[idx+3] != RIGHTBRACK:
                                toks.insert(idx+3, COMA)
                            # toks.insert(idx+4, _var)
                            _vars_dict = self._class_vars_dict[self._vars_dict["GLOBALS"]
                                                               ["global_vars"][_var][1]]
                            _val, _type = self.__eval_assign_values(
                                _vars_dict, toks[:toks.index(SEMI) + 1], _global_call, SEMI)

                            c_str += self.bin_name + DOT + _val + SEMI + NEWLINE
                        break

                elif t == SLEEP:
                    c_str += self.__sleep(vars_dict,
                                          toks[idx + 1:toks.index(SEMI) + 1], _global_call)
                    break

                elif t == USLEEP:
                    c_str += self.__usleep(vars_dict,
                                           toks[idx + 1:toks.index(SEMI) + 1], _global_call)
                    break

                elif t == PRINT:
                    c_str += self.__print(vars_dict,
                                          toks[idx + 2:], _global_call, False)
                    break

                elif t == PRINTL:
                    c_str += self.__print(vars_dict,
                                          toks[idx + 2:], _global_call, True)
                    break

        return c_str
