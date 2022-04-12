#ifndef __BT_INBUILTS_HEADER__
#define __BT_INBUILTS_HEADER__

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h>

#define __ARR__(dim, row, col) arr->ptr[dim][dim * (arr->dims[dim][0] * arr->dims[dim][1]) + row * arr->dims[dim][1] + col]
//arr3d[r][c][d]
// becomes:
// arr3d.data[r * (arr3d.b * arr3d.c) + c * arr3d.c + d];

#pragma GCC diagnostic ignored "-Wformat" 
// #pragma GCC diagnostic ignored "-Wunknown-escape-sequence"
typedef char* str;


typedef struct 
{
  bool **ptr;
  bool **ptr_copy;
  size_t **dims;
  size_t no_of_dims;
} bool_list_t;

typedef struct 
{
  long **ptr;
  long **ptr_copy;
  size_t **dims;
  size_t no_of_dims;
} long_list_t;

typedef struct 
{
  double **ptr;
  double **ptr_copy;
  size_t **dims;
  size_t no_of_dims;
} double_list_t;

typedef struct 
{
  str **ptr;
  str **ptr_copy;
  size_t **dims;
  size_t no_of_dims;
} str_list_t;

bool_list_t *new_bool_list(size_t dims, size_t **shapes);
long_list_t *new_long_list(size_t dims, size_t **shapes);
double_list_t *new_double_list(size_t dims, size_t **shapes);
str_list_t *new_str_list(size_t dims, size_t **shapes);
void print_bool_list(bool_list_t *arr);
void print_long_list(long_list_t *arr);
void print_double_list(double_list_t *arr);
void print_str_list(str_list_t *arr);
str _bt_input(FILE *in);

#endif