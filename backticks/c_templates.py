from ._tokens import *


def make_bt_inbuilts_header():
    header = """#ifndef __BT_INBUILTS_HEADER__
#define __BT_INBUILTS_HEADER__

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h>

// # pragma GCC diagnostic ignored "-Wformat"

#endif
"""

    with open("./C/_bt_inbuilts_.h", "w") as h_write:
        h_write.write(header)


def make_header(header_file_name, funcs_list, global_vars_list, main_file=True, includes=[]):

    funcs = ""
    global_vars = ""
    file_main_func = ""
    _includes = ""

    if not main_file:
        file_main_func = "int main_"+header_file_name[:header_file_name.index(".h")] + "(int argc, char *argv[]);"

    for inc in includes:
        _includes += inc + NEWLINE

    for var in global_vars_list:
        global_vars += var + SEMI + NEWLINE

    for f in funcs_list:
        funcs += f + NEWLINE
        
        
    header_file_name = header_file_name.replace("/", "_")
    
    header_f_n = ("_" + header_file_name[:header_file_name.find(".h")] + "_h_").upper()

    _struct_name = header_file_name[:header_file_name.find(".h")]
    

    header = \
f"""
#ifndef {header_f_n}
#define {header_f_n}

{_includes}

typedef struct
{{

{global_vars}
}} {header_f_n}VARS;

{header_f_n}VARS {_struct_name};

{funcs}
{file_main_func}

#endif
"""

    with open(f"./C/{header_file_name}", "w") as bt_h:
        bt_h.write(header)

def make_source(src_file_name, func_defs, funcs_list, main_body, _return, main_file=True):

    funcs = ""
    f_defs = ""

    for f in funcs_list:
        funcs += f + NEWLINE
    
    for f in func_defs:
        f_defs += f + NEWLINE

    src_file_name = src_file_name.replace("/", "_")

    header_f_n = src_file_name[:src_file_name.find(".c")] + ".h"

    source_c = \
f"""
#include "{header_f_n}"

{f_defs}
{funcs}
int {"main_"+src_file_name[:src_file_name.find(".c")] if not main_file else "main"}(int argc, char *argv[])
{{
{main_body}

return {_return};
}}
"""

    with open(f"./C/{src_file_name}", "w") as bt_src:
        bt_src.write(source_c)
