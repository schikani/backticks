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

#pragma GCC diagnostic ignored "-Wformat" 
// #pragma GCC diagnostic ignored "-Wunknown-escape-sequence"

typedef char * str;

typedef struct
{
    bool *ptr;
    bool *ptr_copy;
    size_t len;
} bool_list_t;

typedef struct
{
    double *ptr;
    double *ptr_copy;
    size_t len;
} double_list_t;

typedef struct
{
    long *ptr;
    long *ptr_copy;
    size_t len;
} long_list_t;

typedef struct
{
    char **ptr;
    char **ptr_copy;
    size_t len;
} str_list_t;

char *_bt_input(FILE *in);

#endif
"""

    with open("./C/_bt_inbuilts_.h", "w") as h_write:
        h_write.write(header)

def make_inbuilts_source():
    source = """#include "_bt_inbuilts_.h"
char *_bt_input(FILE *in)
{
    size_t alloc_length = 64;
    size_t cumulength = 0;
    char * data = malloc(alloc_length);
    while (1) {
        char * cursor = data + cumulength; // here we continue.
        char * ret = fgets(cursor, alloc_length - cumulength, in);
        // printf("r %p %p %zd %zd %zd\\n", data, cursor, cumulength, alloc_length, alloc_length - cumulength);
        if (!ret) {
            // Suppose we had EOF, no error.
            // we just return what we read till now...
            // there is still a \\0 at cursor, so we are fine.
            break;
        }
        size_t newlength = strlen(cursor); // how much is new?
        cumulength += newlength; // add it to what we have.
        if (cumulength < alloc_length - 1 || data[cumulength-1] == '\\n') {
            // not used the whole buffer... so we are probably done.
            break;
        }
        // we need more!
        // At least, probably.
        size_t newlen = alloc_length * 2;
        char * r = realloc(data, newlen);
        // printf("%zd\\n", newlen);
        if (r) {
            data = r;
            alloc_length = newlen;
        } else {
            // realloc error. Return at least what we have...
            // TODO: or better free and return NULL?
            return data;
        }
    }
    char * r = realloc(data, cumulength + 1);
    // printf("%zd\\n", cumulength + 1);
    return r ? r : data; // shrinking should always have succeeded, but who knows?
}
"""
    with open("./C/_bt_inbuilts_.c", "w") as s_write:
        s_write.write(source)


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

extern {header_f_n}VARS {_struct_name};

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

    global_struct_def = f'{("_" + src_file_name[:src_file_name.find(".c")] + "_h_").upper()}VARS {src_file_name[:src_file_name.find(".c")]};'

    source_c = \
f"""
#include "{header_f_n}"
{global_struct_def}

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
