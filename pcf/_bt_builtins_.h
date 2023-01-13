#ifndef __BT_BUILTINS_HEADER__
#define __BT_BUILTINS_HEADER__

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h>

#pragma GCC diagnostic ignored "-Wformat" 
// #pragma GCC diagnostic ignored "-Wunknown-escape-sequence"

typedef char* str;

typedef struct
{
    bool *ptr;
    bool *ptr_copy;
    size_t len;
    size_t reserve;
} bool_list_t;

typedef struct
{
    double *ptr;
    double *ptr_copy;
    size_t len;
    size_t reserve;
} double_list_t;

typedef struct
{
    long *ptr;
    long *ptr_copy;
    size_t len;
    size_t reserve;
} long_list_t;

typedef struct
{
    str *ptr;
    str *ptr_copy;
    size_t len;
    size_t reserve;
} str_list_t;


str _bt_input(FILE *in);
bool_list_t *new_bool_list(size_t reserve);
void check_reserve_bool_list(bool_list_t *arr);
double_list_t *new_double_list(size_t reserve);
void check_reserve_double_list(double_list_t *arr);
long_list_t *new_long_list(size_t reserve);
void check_reserve_long_list(long_list_t *arr);
str_list_t *new_str_list(size_t reserve);
void check_reserve_str_list(str_list_t *arr);
#endif
