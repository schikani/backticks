def make_header(header_file_name, funcs_list):

    funcs = ""

    for f in funcs_list:
        funcs += f + "\n"


    header = f"""#ifndef _BACKTICKS_H_
#define _BACKTICKS_H_
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

def make_source(src_file_name, funcs_list, main_body, _return):

    funcs = ""

    for f in funcs_list:
        funcs += f + "\n"

    source_c = f"""#include "backticks.h"
{funcs}
int main(int argc, char *argv[])
{{
{main_body}

return {_return};
}}
"""

    with open(f"{src_file_name}", "w") as bt_src:
        bt_src.write(source_c)
