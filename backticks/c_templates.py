from ._tokens import *
import os

def make_header(header_file_name, funcs_list, global_vars_list):

    funcs = ""
    global_vars = ""

    for var in global_vars_list:
        global_vars += var + SEMI + NEWLINE

    for f in funcs_list:
        funcs += f + "\n"
    
    header_file_name = header_file_name.replace("/", "_")
    
    header_f_n = ("_" + header_file_name[:header_file_name.find(".h")] + "_h_").upper()

    _struct_name = header_file_name[:header_file_name.find(".h")]
    

    header = \
f"""
#ifndef {header_f_n}
#define {header_f_n}

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h>

typedef struct
{{

{global_vars}
}} {header_f_n}VARS;

{header_f_n}VARS {_struct_name};

{funcs}
#endif
"""

    with open(f"./C/{header_file_name}", "w") as bt_h:
        bt_h.write(header)

def make_source(src_file_name, func_defs, funcs_list, main_body, _return):

    funcs = ""
    f_defs = ""

    for f in funcs_list:
        funcs += f + "\n"
    
    for f in func_defs:
        f_defs += f + "\n"

    src_file_name = src_file_name.replace("/", "_")

    header_f_n = src_file_name[:src_file_name.find(".c")] + ".h"

    source_c = \
f"""
#include "{header_f_n}"

{f_defs}
{funcs}
int main(int argc, char *argv[])
{{
{main_body}

return {_return};
}}
"""

    with open(f"./C/{src_file_name}", "w") as bt_src:
        bt_src.write(source_c)
