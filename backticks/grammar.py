from ast import Add, Eq, operator
from ._tokens import *
from .tokenizer import Tokenizer
from .c_templates import *


def _new_str(var, _str):

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


def _concat_str(var, _str):

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


def _compare_str(var, _str):

    _s = ""
    for i in _str:
        if i == NEWLINE:
            _s += "\\n"
        else:
            _s += i

    _str = _s

    str_to_ret = f'strcmp({var}, {_str})'
    return str_to_ret


def _free_str(var):
    str_to_ret = f'free({var});' + NEWLINE
    str_to_ret += f'{var} = NULL;' + NEWLINE
    return str_to_ret


class BT_Grammar(Tokenizer):
    def __init__(self, bt_file_name):
        super().__init__(bt_file_name)
        self._vars_dict = dict()
        self._global_vars_list = []
        self._private_func_list = []
        self._public_func_list = []
        self._funcs_impl = []

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
                   (ret_val, ret_type), 
                {
                    "var1": [val, type],
                    "var2": [val, type],
                }],

                "func2": [
                        (ret_val, ret_type),    --> index 0 of 'func2'
                {
                        "var1": [val, type], 
                        "var2": [val, type],
                }
            ]
            }
        '''
        self._vars_dict["GLOBALS"] = {"global_vars": {}}
        self._vars_dict["FUNCS"] = {}

    def __bt_to_c_str(self, _str):
        _str = '"' + _str[1:-1] + '"'

        return _str

    def __eval_assign_values(self, vars_dict, tok_list, _global_call, _del):
        float_found = False
        str_found = False
        int_found = False
        val = ""
        _type = ""
        _val_idx = 0

        # To parse a string
        # Invoked from self.__string_parser()
        if len(tok_list) == 2:
            if tok_list[1] == tuple():
                tok_list = self._tokenizer(tok_list[0]+SEMI)
                # print(tok_list)


        while tok_list[_val_idx] != _del:

            v = tok_list[_val_idx]

            if self.is_operator(v) or self.is_string(v) or self.is_string(v, vars_dict) or\
                    self.is_string(v, self._vars_dict["GLOBALS"]["global_vars"]) or\
                    self.is_string(v, self._vars_dict["FUNCS"], func=True):
                
                str1 = ""
                str2 = ""

                if (tok_list[_val_idx+1] == EQUALS and tok_list[_val_idx+2] == EQUALS) or\
                    (tok_list[_val_idx+1] == LEFTBRACK and tok_list[_val_idx+2] == RIGHTBRACK and
                     tok_list[_val_idx+3] == EQUALS and tok_list[_val_idx+4] == EQUALS):
                    str1 = v
                    if tok_list[_val_idx+1] == LEFTBRACK and tok_list[_val_idx+2] == RIGHTBRACK:
                        str2 = tok_list[_val_idx+5]
                    else:
                        str2 = tok_list[_val_idx+3]

                    if self.is_string(str1):
                        str1 = self.__bt_to_c_str(str1)

                    elif self.is_string(str1, vars_dict):
                        if _global_call:
                            str1 = self.bin_name + DOT + str1

                    elif self.is_string(str1, self._vars_dict["GLOBALS"]["global_vars"]):
                        str1 = self.bin_name + DOT + str1

                    elif self.is_string(str1, self._vars_dict["FUNCS"], func=True):
                        str1 += LEFTBRACK + RIGHTBRACK
                        _val_idx += 2

                    if self.is_string(str2):
                        str2 = self.__bt_to_c_str(str2)

                    elif self.is_string(str2, vars_dict):
                        if _global_call:
                            str2 = self.bin_name + DOT + str2

                    elif self.is_string(str2, self._vars_dict["GLOBALS"]["global_vars"]):
                        str2 = self.bin_name + DOT + str2

                    elif self.is_string(str2, self._vars_dict["FUNCS"], func=True):
                        str2 += LEFTBRACK + RIGHTBRACK
                        _val_idx += 2

                    val += _compare_str(str1, str2) + EQUALS + EQUALS + ZERO

                    _val_idx += 4
                    continue

                elif self.is_string(v):
                    val += self.__bt_to_c_str(v)
                    str_found = True

                elif self.is_string(v, vars_dict):
                    if _global_call:
                        val += self.bin_name + DOT + v
                    else:
                        val += v

                    str_found = True

                elif self.is_string(v, self._vars_dict["GLOBALS"]["global_vars"]):
                    val += self.bin_name + DOT + v
                    str_found = True

                elif self.is_string(v, self._vars_dict["FUNCS"], func=True):
                    val += v
                    str_found = True


                else:
                    val += v
            

            elif v in [LEFTBRACK, RIGHTBRACK, LEFTCURL, RIGHTCURL]:
                val += v

            elif v in [AND, OR]:
                if v == AND:
                    val += " && "

                elif v == OR:
                    val += " || "

            elif v in vars_dict.keys() or v in self._vars_dict["FUNCS"].keys():

                # Check for function variable name
                # If it is in global scope or function scope
                if v in vars_dict.keys():

                    if vars_dict[v][1] == DOUBLE:
                        float_found = True

                    elif vars_dict[v][1] == LONG:
                        int_found = True

                    elif vars_dict[v][1] == STR:
                        str_found = True

                    if _global_call:
                        if not str_found:
                            val += self.bin_name + DOT + v

                    else:
                        if not str_found:
                            val += v

                # Check for function name
                elif v in self._vars_dict["FUNCS"].keys():

                    if self._vars_dict["FUNCS"][v][0][1] == DOUBLE:
                        float_found = True

                    elif self._vars_dict["FUNCS"][v][0][1] == LONG:
                        int_found = True

                    elif self._vars_dict["FUNCS"][v][0][1] == STR:
                        str_found = True

                    # if not str_found:
                    val += v

            elif v in self._vars_dict["GLOBALS"]["global_vars"].keys():

                if self._vars_dict["GLOBALS"]["global_vars"][v][1] == DOUBLE:
                    float_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == LONG:
                    int_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == STR:
                    str_found = True

                if not str_found:
                    val += self.bin_name + DOT + v

            elif self.is_float(v):
                val += v
                float_found = True
            elif self.is_int(v):
                val += v
                int_found = True

            _val_idx += 1

        if str_found:
            _type = STR

        elif float_found:
            _type = DOUBLE

        elif int_found:
            _type = LONG

        return (val, _type)

    def __reassign_vals(self, vars_dict, toks, _global_call):

        t = toks[0]
        str_to_ret = ''

        # Check for '+=', '-=', '*=', '\=' condition
        if toks[1] in [ADD, SUB, MUL, DIV] and toks[2] == EQUALS:
            val, _type = self.__eval_assign_values(
                vars_dict, toks[3:toks.index(SEMI)+1], _global_call, SEMI)

        # '=' condition
        else:
            val, _type = self.__eval_assign_values(
                vars_dict, toks[2:toks.index(SEMI)+1], _global_call, SEMI)

        if not _global_call and t in vars_dict.keys():
            
            # String or Number
            if toks[1] == ADD and toks[2] == EQUALS:
                if _type == STR:
                    str_to_ret += _concat_str(t, val)
                else:
                    str_to_ret += t + ADD + EQUALS + val + SEMI + NEWLINE
            
            # Number
            elif toks[1] in [SUB, MUL, DIV] and toks[2] == EQUALS:
                str_to_ret += t + toks[1] + EQUALS + val + SEMI + NEWLINE

            # Case '='
            else:
                if _type == STR:
                    str_to_ret += _free_str(t)
                    str_to_ret += _new_str(t, val)
                else:
                    str_to_ret += t + EQUALS + val + SEMI + NEWLINE

        elif _global_call or t in self._vars_dict["GLOBALS"]["global_vars"].keys():

            # String or Number
            if toks[1] == ADD and toks[2] == EQUALS:
                if _type == STR:
                    str_to_ret += _concat_str(self.bin_name+DOT+t, val)
                else:
                    str_to_ret += self.bin_name + DOT + t + ADD + EQUALS + val + SEMI + NEWLINE
            
            # Number
            elif toks[1] in [SUB, MUL, DIV] and toks[2] == EQUALS:
                str_to_ret += self.bin_name + DOT + t + toks[1] + EQUALS + val + SEMI + NEWLINE

            # Case '='
            else:
                if _type == STR:
                    str_to_ret += _free_str(self.bin_name+DOT+t)
                    str_to_ret += _new_str(self.bin_name+DOT+t, val)
                else:
                    str_to_ret += self.bin_name + DOT + t + EQUALS + val + SEMI + NEWLINE

        return str_to_ret

    '''
    Make a function for each keyword and call each other in recursion
    '''

    def __let(self, vars_dict, tok_list, _global_call):
        var = tok_list[0]
        val = ""
        _type = ""

        # Check if the variable is already defined
        if var not in vars_dict.keys():

            # Make list of [val, _type] for the associated var_key in vars_dict
            vars_dict[var] = []
            assign = tok_list[1]

            if assign == EQUALS:

                val, _type = self.__eval_assign_values(
                    vars_dict, tok_list[2:], _global_call, SEMI)

                vars_dict[var].append(val)
                vars_dict[var].append(_type)

            elif assign == COLON:
                _type = tok_list[2]

                if _type == INT:
                    _type = LONG
                    val = "0"

                elif _type == FLOAT:
                    _type = DOUBLE
                    val = "0.0f"

                elif _type == STR:
                    _type = STR
                    val = '""'

                vars_dict[var].append(val)
                vars_dict[var].append(_type)

            if _type == STR:
                _type = CHARSTAR

            if _global_call:
                self._global_vars_list.append(f"{_type} {var}")
                if _type == CHARSTAR:
                    return _new_str(self.bin_name+DOT+var, val)
                return f"{self.bin_name}.{var} = {val};\n"

            else:
                if _type == CHARSTAR:
                    return CHARSTAR + _new_str(var, val)
                return f"{_type} {var} = {val};\n"

    def __print(self, vars_dict, tok_list, _global_call):

        print_str = tok_list[0]

        if (self.is_string(print_str)):
            print_str = print_str[1:-1]

            return self.__string_parser(print_str, vars_dict, _global_call, new_line=False)

    def __printl(self, vars_dict, tok_list, _global_call):

        print_str = tok_list[0]

        if (self.is_string(print_str)):
            print_str = print_str[1:-1]

            return self.__string_parser(print_str, vars_dict, _global_call, new_line=True)

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

        start = tok_list.index(LEFTCURL)+1
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

        str_to_ret = ""

        if tok_list[0] in [IF, ELIF, ELSE]:
            if tok_list[0] == ELIF:
                tok_list[0] = ELSE_IF

        if tok_list[0] != ELSE:

            if tok_list[1] != LEFTBRACK:
                str_to_ret += tok_list[0] + SPACE + LEFTBRACK
                _val, _type = self.__eval_assign_values(
                    vars_dict, tok_list[1:], _global_call, LEFTCURL)
                str_to_ret += _val + RIGHTBRACK + NEWLINE + LEFTCURL + NEWLINE

            else:
                str_to_ret += tok_list[0] + SPACE
                _val, _type = self.__eval_assign_values(
                    vars_dict, tok_list[1:], _global_call, LEFTCURL)
                str_to_ret += _val + NEWLINE + LEFTCURL + NEWLINE

        else:
            str_to_ret += tok_list[0] + SPACE + LEFTCURL + NEWLINE

        start = tok_list.index(LEFTCURL)+1
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

    def __func(self, current_func, toks):
        c_func_params = ""

        if not current_func in self._vars_dict["FUNCS"]:
            self._vars_dict["FUNCS"].update({current_func: [(), {}]})
            prms_and_ret = toks[toks.index(LEFTBRACK): toks.index(LEFTCURL)]
            params = prms_and_ret[prms_and_ret.index(
                LEFTBRACK)+1: prms_and_ret.index(RIGHTBRACK)]

            func_body_toks = toks[toks.index(LEFTCURL)+1:-1]

            # Extract return type and value
            return_type = prms_and_ret[-1]
            ret_val = ""

            if return_type == COLON or return_type == RIGHTBRACK:
                return_type = VOID

            elif return_type == INT:
                return_type = LONG
                ret_val = "0"

            elif return_type == FLOAT:
                return_type = DOUBLE
                ret_val = "0.0f"

            elif return_type == STR:
                ret_val = ""

            self._vars_dict["FUNCS"][current_func][0] = (ret_val, return_type)

            if params and params[0] != ":":
                # Extract param vars and types and skip if no params
                _idx = 0
                while (_idx < len(params)):
                    var = params[_idx]
                    _type = params[_idx+2]
                    val = ""
                    if _type == INT:
                        _type = LONG
                        val = "0"

                    elif _type == FLOAT:
                        _type = DOUBLE
                        val = "0.0f"

                    elif _type == STR:
                        val = ""

                    self._vars_dict["FUNCS"][current_func][1][var] = (
                        val, _type)
                    c_func_params += f"{_type} {var}"

                    # To exclude comma after last param
                    if _idx < len(params) - 3:
                        c_func_params += ", "
                    _idx += 4

            start = 0
            sub_toks = []
            str_to_ret = ""

            while start < len(func_body_toks):

                if func_body_toks[start] in [IF, ELIF, ELSE]:
                    str_to_ret += self.__if_elif_else(
                        self._vars_dict["FUNCS"][current_func][1], func_body_toks[start:], _global_call=False)
                    break

                elif func_body_toks[start] == LOOP:
                    str_to_ret += self.__loop_until_for(
                        self._vars_dict["FUNCS"][current_func][1], func_body_toks[start:], _global_call=False)
                    break

                elif func_body_toks[start] != SEMI:

                    sub_toks.append(func_body_toks[start])
                    start += 1

                elif func_body_toks[start] == SEMI:

                    sub_toks.append(func_body_toks[start])
                    str_to_ret += self._convert_to_c_str(
                        [sub_toks], self._vars_dict["FUNCS"][current_func][1], _global_call=False)

                    sub_toks.clear()

                    start += 1

            if return_type == STR:
                return_type = CHARSTAR

            func = f"{return_type} {current_func}({c_func_params})" + \
                NEWLINE + LEFTCURL + NEWLINE

            func += str_to_ret + RIGHTCURL + NEWLINE

            self._funcs_impl.append(func)

            if toks[0] == FUNCTION:
                self._private_func_list.append(
                    f"{return_type} {current_func}({c_func_params});")
            elif toks[0] == PUB_FUNC:
                self._public_func_list.append(
                    f"{return_type} {current_func}({c_func_params});")

    def __return(self, vars_dict, tok_list):

        ret_val, _type = self.__eval_assign_values(
            vars_dict, tok_list, False, SEMI)

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
                if c == LEFTSQUARE:
                    left = right + 1
                    box_started = True

                elif c == NEWLINE:
                    frmt += "\\n"

                # Get the values between box to determine var, func
                # TODO support arithmetic operations inside box. EXAMPLES: [1+3], [`> ` * 3]
                else:
                    frmt += c

            else:
                if (c == RIGHTSQUARE):
                    var = self.sub_string(string, left, right)
                    var_list = [var, ()]
                    val, _type = self.__eval_assign_values(
                        vars_dict, var_list, _global_call, SEMI)

                    # print(val, _type)

                    # Type
                    if _type == LONG:
                        if val.find(SUB) != -1:
                            frmt += "%d"
                        else:
                            frmt += "%ld"
                        
                        
                    elif _type == DOUBLE:
                        frmt += "%f"
                    elif _type == STR:
                        frmt += "%s"

                    values += COMA + val

                    # if var.find(ADD) != -1:
                    #     nums = var.split(ADD)
                    #     float_found = False
                    #     _v = ""
                    #     for idx, n in enumerate(nums):
                    #         if self.is_float(n):
                    #             float_found = True

                    #         if idx < len(nums) - 1:
                    #             _v += n + ADD

                    #         else:
                    #             _v += n

                    #     if float_found:
                    #         frmt += "%f"
                    #     else:
                    #         frmt += "%d"

                    #     values += COMA + _v

                    # # To store
                    # elif var in vars_dict.keys():
                    #     # Type
                    #     if vars_dict[var][1] == LONG:
                    #         frmt += "%ld"
                    #     elif vars_dict[var][1] == DOUBLE:
                    #         frmt += "%f"

                    #     elif vars_dict[var][1] == STR:
                    #         frmt += "%s"

                    #     # If global variable
                    #     if _global_call:
                    #         values += f", {self.bin_name}.{var}"

                    #     else:
                    #         values += f", {var}"

                    # # If var not found check in global vars
                    # elif var in self._vars_dict["GLOBALS"]["global_vars"].keys():
                    #     # Type
                    #     if self._vars_dict["GLOBALS"]["global_vars"][var][1] == LONG:
                    #         frmt += "%ld"

                    #     elif self._vars_dict["GLOBALS"]["global_vars"][var][1] == DOUBLE:
                    #         frmt += "%f"

                    #     elif self._vars_dict["GLOBALS"]["global_vars"][var][1] == STR:
                    #         frmt += "%s"

                    #     values += f", {self.bin_name}.{var}"

                    # # If it is a function
                    # elif var[-2] == LEFTBRACK and var[-1] == RIGHTBRACK:
                    #     var = var[:-2]
                    #     if var in self._vars_dict["FUNCS"].keys():
                    #         # Type
                    #         if self._vars_dict["FUNCS"][var][0][1] == LONG:
                    #             frmt += "%ld"

                    #         elif self._vars_dict["FUNCS"][var][0][1] == DOUBLE:
                    #             frmt += "%f"

                    #         elif self._vars_dict["FUNCS"][var][0][1] == STR:
                    #             frmt += "%s"

                    #         values += f", {var}()"

                    box_started = False

            right += 1

        result += frmt
        if new_line:
            result += '\\n"'
        else:
            result += '"'

        result += values + print_tail

        return result

    def _convert_to_c_str(self, tokens, vars_dict, _global_call=True):

        c_str = ""

        # print(tokens)
        tokens = iter(tokens)
        for toks in tokens:
            for idx, t in enumerate(toks):

                if t == FUNCTION or t == PUB_FUNC:
                    current_func = toks[idx+1]
                    self.__func(current_func, toks)

                    break

                elif self.is_keyword(t):

                    # LET
                    if t == LET:
                        c_str += self.__let(vars_dict,
                                            toks[idx+1:], _global_call)

                    # IF ELIF ELSE
                    elif t in [IF, ELIF, ELSE]:
                        c_str += self.__if_elif_else(vars_dict,
                                                     toks, _global_call)

                        break

                    elif t == LOOP:
                        c_str += self.__loop_until_for(vars_dict,
                                                       toks, _global_call)

                    elif t == BREAK:
                        c_str += BREAK + SEMI + NEWLINE

                    elif t == RETURN:
                        c_str += self.__return(vars_dict,
                                               toks[idx+1:toks.index(SEMI)+1])

                    break

                # Check if the name already exist as func_name and var both
                elif t in self._vars_dict["GLOBALS"]["global_vars"].keys() and t in self._vars_dict["FUNCS"].keys() and toks[idx+1] == LEFTBRACK:
                    print("A `function name` cannot be similar to a `global variable`")
                    return ""

                # While reassigning varibles, check for varibale scope or if it is a function
                elif (t in vars_dict.keys() and toks[idx+1] == EQUALS) or\
                    (t in vars_dict.keys() and toks[idx+1] in [ADD,SUB,MUL,DIV] and toks[idx+2] == EQUALS) or\
                    (t in self._vars_dict["GLOBALS"]["global_vars"].keys() and toks[idx+1] == EQUALS) or\
                    (t in self._vars_dict["GLOBALS"]["global_vars"].keys() and toks[idx+1] in [ADD,SUB,MUL,DIV] and toks[idx+2] == EQUALS):

                    c_str += self.__reassign_vals(vars_dict,
                                                  toks, _global_call)
                    break

                elif t in self._vars_dict["FUNCS"].keys() and toks[idx+1] == LEFTBRACK:
                    # get function name
                    c_str += t
                    # Get function variables dict on index[1] with "var": (val, type) pairs
                    _vars_dict = self._vars_dict["FUNCS"][t][1]
                    _val, _type = self.__eval_assign_values(
                        _vars_dict, toks[idx+1:toks.index(SEMI)+1], _global_call, SEMI)
                    c_str += _val + SEMI + NEWLINE
                    break

                elif t == SLEEP:
                    c_str += self.__sleep(vars_dict,
                                          toks[idx+1:toks.index(SEMI)+1], _global_call)
                    break

                elif t == USLEEP:
                    c_str += self.__usleep(vars_dict,
                                           toks[idx+1:toks.index(SEMI)+1], _global_call)
                    break

                elif t == PRINT:
                    c_str += self.__print(vars_dict,
                                          toks[idx+2:], _global_call)
                    break

                elif t == PRINTL:
                    c_str += self.__printl(vars_dict,
                                           toks[idx+2:], _global_call)
                    break

        return c_str
