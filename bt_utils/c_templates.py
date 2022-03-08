def make_header(header_file_name, funcs_list):

    funcs = ""

    for f in funcs_list:
        funcs += f + "\n"
    
    header_f_n = ("_" + header_file_name.strip(".h") + "_h_").upper()

    
    header = f"""#ifndef {header_f_n}
#define {header_f_n}

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

{funcs}
#endif
"""

    with open(f"{header_file_name}", "w") as bt_h:
        bt_h.write(header)

def make_source(src_file_name, func_defs, funcs_list, main_body, _return):

    funcs = ""
    f_defs = ""

    for f in funcs_list:
        funcs += f + "\n"
    
    for f in func_defs:
        f_defs += f + "\n"

    header_f_n = src_file_name.strip(".c") + ".h"

    source_c = f"""#include "{header_f_n}"

{f_defs}
{funcs}
int main(int argc, char *argv[])
{{
{main_body}

return {_return};
}}
"""

    with open(f"{src_file_name}", "w") as bt_src:
        bt_src.write(source_c)
