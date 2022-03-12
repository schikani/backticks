from operator import index
from ._tokens import *
from .tokenizer import Tokenizer
from .c_templates import *


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
                        (ret_val, ret_type),
                {
                        "var1": [val, type],
                        "var2": [val, type],
                }]
            }
        '''
        self._vars_dict["GLOBALS"] = {"global_vars": {}}
        self._vars_dict["FUNCS"] = {}


    def __eval_assign_values(self, vars_dict, tok_list, _global_call):
        float_found = False
        str_found = False
        int_found = False
        val = ""
        _type = ""
        _val_idx = 0

        while (tok_list[_val_idx] != SEMI):

            v = tok_list[_val_idx]
            if v in [ADD, SUB, MUL, DIV]:
                val += v

            elif v in [LEFTBRACK, RIGHTBRACK]:
                val += v

            
            elif v in vars_dict.keys() or v in self._vars_dict["FUNCS"].keys():

                # Check for function variable name
                if v in vars_dict.keys():
                    if _global_call:
                        val += self.bin_name + DOT + v

                    else:
                        val += v

                    if vars_dict[v][1] == DOUBLE:
                        float_found = True

                    elif vars_dict[v][1] == LONG:
                        int_found = True

                    elif vars_dict[v][1] == STR:
                        str_found = True
                
                # Check for function name
                elif v in self._vars_dict["FUNCS"].keys():
                    val += v

                    if self._vars_dict["FUNCS"][v][0][1] == DOUBLE:
                        float_found = True

                    elif self._vars_dict["FUNCS"][v][0][1] == LONG:
                        int_found = True

                    elif self._vars_dict["FUNCS"][v][0][1] == STR:
                        str_found = True

            
            elif v in self._vars_dict["GLOBALS"]["global_vars"].keys():

                val += self.bin_name + DOT + v
                if self._vars_dict["GLOBALS"]["global_vars"][v][1] == DOUBLE:
                    float_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == LONG:
                    int_found = True

                elif self._vars_dict["GLOBALS"]["global_vars"][v][1] == STR:
                    str_found = True

            elif self.is_float(v):
                val += v
                float_found = True
            elif self.is_int(v):
                val += v
                int_found = True
            elif self.is_string(v):
                val += v
                str_found = True

            _val_idx += 1

        if float_found:
            # print("DOUBLE")
            _type = DOUBLE
        elif int_found:
            # print("INT")
            _type = LONG
        elif str_found:
            _type = STR
        
        return (val, _type)

    # TODO
    '''
    Make a function for each keyword and call each other in recursion
    '''

    def __let(self, vars_dict, tok_list, _global_call):
        # print(tok_list)
        var = tok_list[0]
        val = ""
        _type = ""

        # Check if the variable is already defined
        if var not in vars_dict.keys():

            # Make list of [val, _type] for the associated var_key in vars_dict
            vars_dict[var] = []
            assign = tok_list[1]

            if assign == EQUALS:

                val, _type = self.__eval_assign_values(vars_dict, tok_list[2:], _global_call)

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
                    val = ""

                vars_dict[var].append(val)
                vars_dict[var].append(_type)

                # _val_idx += 1

            if _global_call:
                self._global_vars_list.append(f"{_type} {var}")
                return f"{self.bin_name}.{var} = {val};\n"

            else:
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

    def __if_elif_else(self, tok_list):
        pass

    def __sleep(self, vars_dict, tok_list, _global_call):
        _val, _type = self.__eval_assign_values(vars_dict, tok_list, _global_call)
        return f"sleep({_val});\n" 
    
    def __usleep(self, vars_dict, tok_list, _global_call):
        _val, _type = self.__eval_assign_values(vars_dict, tok_list, _global_call)
        return f"usleep({_val});\n"
    
#     def __loop(self, vars_dict, tok_list, _global_call):
        
#         loop_body = ""
#         for t in tok_list:
#             # loop_body += t + NEWLINE
#             pass


#         _loop = \
# f"""
# while (true)
# {{
# {loop_body}
# }}
# """     
#         return _loop



    def __func(self, current_func, toks):
        if not current_func in self._vars_dict["FUNCS"]:
            self._vars_dict["FUNCS"].update({current_func: [(), {}]})
            prms_and_ret = toks[toks.index(LEFTBRACK):toks.index(LEFTCURL)]
            params = prms_and_ret[prms_and_ret.index(
                LEFTBRACK)+1:prms_and_ret.index(RIGHTBRACK)]
            func_body_toks = toks[toks.index(LEFTCURL)+1:toks.index(RIGHTCURL)]

            # Extract return type and value
            return_type = prms_and_ret[-1]
            ret_val = ""
            if return_type == RIGHTBRACK:
                return_type = VOID
        
            elif return_type == INT:
                return_type = LONG
                ret_val = "0"

            elif return_type == FLOAT:
                return_type = DOUBLE
                ret_val = "0.0f"

            elif return_type == STR:
                ret_val = ""

            # print(return_type, ret_val)
            self._vars_dict["FUNCS"][current_func][0] = (ret_val, return_type)

            c_func_params = ""

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

                # print(var, _type, val)
                self._vars_dict["FUNCS"][current_func][1][var] = (val, _type)
                c_func_params += f"{_type} {var}"

                # To exclude comma after last param
                if _idx < len(params) - 3:
                    c_func_params += ", "
                _idx += 4

            # print(c_func_params)

            toks_to_pass_on = []

            # Seperate tokens with semi
            count = 0
            while (count < len(func_body_toks)):
                t = []
                while func_body_toks[count] != SEMI:
                    t.append(func_body_toks[count])
                    count += 1
                t.append(func_body_toks[count])
                toks_to_pass_on.append(t)
                count += 1

            # print(toks_to_pass_on)

            func = f"{return_type} {current_func}({c_func_params})" + \
                NEWLINE + LEFTCURL + NEWLINE
            func += self._convert_to_c_str(
                toks_to_pass_on, self._vars_dict["FUNCS"][current_func][1], _global_call=False) + NEWLINE + RIGHTCURL
            self._funcs_impl.append(func)

            if toks[0] == FUNCTION:
                self._private_func_list.append(
                    f"{return_type} {current_func}({c_func_params});")
            elif toks[0] == PUB_FUNC:
                self._public_func_list.append(
                    f"{return_type} {current_func}({c_func_params});")

    def __return(self, vars_dict, tok_list):

        ret_val, _type = self.__eval_assign_values(vars_dict, tok_list, False)

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
                if (c == LEFTSQUARE):
                    left = right + 1
                    box_started = True

                # Get the values between box to determine var, func
                # TODO support arithmetic operations inside box. EXAMPLES: [1+3], [`> ` * 3]
                else:
                    frmt += c

            else:
                if (c == RIGHTSQUARE):
                    var = self.sub_string(string, left, right)

                    # To store
                    if var in vars_dict.keys():
                        # Type
                        if vars_dict[var][1] == LONG:
                            frmt += "%ld"
                        elif vars_dict[var][1] == DOUBLE:
                            frmt += "%f"
                        
                        # If global variable
                        if _global_call:
                            values += f", {self.bin_name}.{var}"

                        else:
                            values += f", {var}"
                    
                    # If var not found check in global vars
                    elif var in self._vars_dict["GLOBALS"]["global_vars"].keys():
                        # Type
                        if self._vars_dict["GLOBALS"]["global_vars"][var][1] == LONG:
                            frmt += "%ld"
                        elif self._vars_dict["GLOBALS"]["global_vars"][var][1] == DOUBLE:
                            frmt += "%f"
                        
                        values += f", {self.bin_name}.{var}"
                    
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
        tokens = iter(tokens)
        for toks in tokens:
            for idx, t in enumerate(toks):

                if self.is_keyword(t):
                    if t == LET:
                        c_str += self.__let(vars_dict, toks[idx+1:], _global_call)

                    elif t == RETURN:
                        c_str += self.__return(vars_dict, toks[idx+1:toks.index(SEMI)+1])

                    break

                elif t == FUNCTION or t == PUB_FUNC:
                    current_func = toks[idx+1]
                    self.__func(current_func, toks[idx:toks.index(RIGHTCURL)+1])
                    break
                
                # Reassign variables
                elif t in vars_dict.keys() and toks[idx+1] == EQUALS:
                    val, _type = self.__eval_assign_values(vars_dict, toks[2:toks.index(SEMI)+1], _global_call)
                    if _global_call:
                        c_str += self.bin_name + DOT + t + EQUALS + val + SEMI + NEWLINE
                    else:
                        c_str += t + EQUALS + val + SEMI + NEWLINE
                    
                    break

                elif t == SLEEP:
                    c_str += self.__sleep(vars_dict, toks[idx+1:toks.index(SEMI)+1], _global_call)
                    break

                elif t == USLEEP:
                    c_str += self.__usleep(vars_dict, toks[idx+1:toks.index(SEMI)+1], _global_call)
                    break
                
                elif t == LOOP:
                    c_str += self.__loop(toks[idx+2:toks.index(G_THAN)+1])
                    break

                elif t == PRINT:
                    c_str += self.__print(vars_dict, toks[idx+2:], _global_call)
                    break

                elif t == PRINTL:
                    c_str += self.__printl(vars_dict, toks[idx+2:], _global_call)
                    break


        return c_str