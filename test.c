#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

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

 

#define ARR(dim, row, col) arr->ptr[dim][dim * (arr->dims[dim][0] * arr->dims[dim][1]) + row * arr->dims[dim][1] + col]
//arr3d[r][c][d]
// becomes:
// arr3d.data[r * (arr3d.b * arr3d.c) + c * arr3d.c + d];


bool_list_t *new_bool_list(size_t dims, size_t **shapes)
// bool_list_t *new_bool_list()
{
    // Allocate memory for bool_list_t
    bool_list_t *arr = (bool_list_t *)calloc(1, sizeof(bool_list_t));
    arr->no_of_dims = dims;
    arr->dims = shapes;

    // Allocate memory for ptr with no of dimension
    arr->ptr = (bool **)calloc(arr->no_of_dims, sizeof(bool *));
    // Copy the pointer 
    arr->ptr_copy = arr->ptr;

    printf("NO OF DIMS: %ld\n\n", arr->no_of_dims);

    // DIMENSIONS
    for (size_t i = 0; i < arr->no_of_dims; ++i)
    {   
        // ROWS[0] and COLS[1]
        arr->ptr[i] = calloc(arr->dims[i][0]*arr->dims[i][1], sizeof(bool));

        for (size_t j = 0; j < arr->dims[i][0]*arr->dims[i][1]; ++j)
        {
            arr->ptr[i][j] = 0;
        }
    }
    return arr;
}

long_list_t *new_long_list(size_t dims, size_t **shapes)
// long_list_t *new_long_list()
{
    // Allocate memory for long_list_t
    long_list_t *arr = (long_list_t *)calloc(1, sizeof(long_list_t));
    arr->no_of_dims = dims;
    arr->dims = shapes;

    // Allocate memory for ptr with no of dimension
    arr->ptr = (long **)calloc(arr->no_of_dims, sizeof(long *));
    // Copy the pointer 
    arr->ptr_copy = arr->ptr;

    printf("NO OF DIMS: %ld\n\n", arr->no_of_dims);

    // DIMENSIONS
    for (size_t i = 0; i < arr->no_of_dims; ++i)
    {   
        // ROWS[0] and COLS[1]
        arr->ptr[i] = calloc(arr->dims[i][0]*arr->dims[i][1], sizeof(long));

        for (size_t j = 0; j < arr->dims[i][0]*arr->dims[i][1]; ++j)
        {
            arr->ptr[i][j] = 0;
        }
    }
    return arr;
}

double_list_t *new_double_list(size_t dims, size_t **shapes)
// double_list_t *new_double_list()
{
    // Allocate memory for double_list_t
    double_list_t *arr = (double_list_t *)calloc(1, sizeof(double_list_t));
    arr->no_of_dims = dims;
    arr->dims = shapes;

    // Allocate memory for ptr with no of dimension
    arr->ptr = (double **)calloc(arr->no_of_dims, sizeof(double *));
    // Copy the pointer 
    arr->ptr_copy = arr->ptr;

    printf("NO OF DIMS: %ld\n\n", arr->no_of_dims);

    // DIMENSIONS
    for (size_t i = 0; i < arr->no_of_dims; ++i)
    {   
        // ROWS[0] and COLS[1]
        arr->ptr[i] = calloc(arr->dims[i][0]*arr->dims[i][1], sizeof(double));

        for (size_t j = 0; j < arr->dims[i][0]*arr->dims[i][1]; ++j)
        {
            arr->ptr[i][j] = 0;
        }
    }
    return arr;
}

str_list_t *new_str_list(size_t dims, size_t **shapes)
// str_list_t *new_str_list()
{
    // Allocate memory for str_list_t
    str_list_t *arr = (str_list_t *)calloc(1, sizeof(str_list_t));
    arr->no_of_dims = dims;
    arr->dims = shapes;

    // Allocate memory for ptr with no of dimension
    arr->ptr = (str **)calloc(arr->no_of_dims, sizeof(str *));
    // Copy the pointer 
    arr->ptr_copy = arr->ptr;

    printf("NO OF DIMS: %ld\n\n", arr->no_of_dims);

    // DIMENSIONS
    for (size_t i = 0; i < arr->no_of_dims; ++i)
    {   
        // ROWS[0] and COLS[1]
        arr->ptr[i] = calloc((arr->dims[i][0]*arr->dims[i][1])+1, sizeof(str));

        for (size_t j = 0; j < arr->dims[i][0]*arr->dims[i][1]; ++j)
        {
            arr->ptr[i][j] = "0";
        }
    }
    return arr;
}

void print_bool_list(bool_list_t *arr)
{
    printf("[");
    for (size_t i = 0; i < arr->no_of_dims; i++)
    {
        // printf("DIMENSION: %ld\n", i);
        printf("[");
        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            printf("[");
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                if (k == arr->dims[i][1]-1)
                {
                    printf(ARR(i, j, k) ? "True]": "False]");  
                }
                else
                {
                    printf(ARR(i, j, k) ? "True, ": "False, ");  
                } 
            }
            printf(j == arr->dims[i][0]-1 ? "]": ", ");
        }
        if (i < arr->no_of_dims-1)
        {
            printf(",\n\n");
        }
    }
    printf("]\n");
}

void print_long_list(long_list_t *arr)
{
    printf("[");
    for (size_t i = 0; i < arr->no_of_dims; i++)
    {
        // printf("DIMENSION: %ld\n", i);
        printf("[");
        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            printf("[");
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                printf(k == arr->dims[i][1]-1 ? "%ld]": "%ld, ", ARR(i, j, k));
            }
            printf(j == arr->dims[i][0]-1 ? "]": ", ");
        }
        if (i < arr->no_of_dims-1)
        {
            printf(",\n\n");
        }
    }
    printf("]\n");
}

void print_double_list(double_list_t *arr)
{
    printf("[");
    for (size_t i = 0; i < arr->no_of_dims; i++)
    {
        // printf("DIMENSION: %ld\n", i);
        printf("[");
        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            printf("[");
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                printf(k == arr->dims[i][1]-1 ? "%f]": "%f, ", ARR(i, j, k));
            }
            printf(j == arr->dims[i][0]-1 ? "]": ", ");
        }
        if (i < arr->no_of_dims-1)
        {
            printf(",\n\n");
        }
    }
    printf("]\n");
}

void print_str_list(str_list_t *arr)
{
    printf("[");
    for (size_t i = 0; i < arr->no_of_dims; i++)
    {
        // printf("DIMENSION: %ld\n", i);
        printf("[");
        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            printf("[");
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                printf(k == arr->dims[i][1]-1 ? "%s]": "%s, ", ARR(i, j, k));
            }
            printf(j == arr->dims[i][0]-1 ? "]": ", ");
        }
        if (i < arr->no_of_dims-1)
        {
            printf(",\n\n");
        }
    }
    printf("]\n");
}


int main(int argc, char *argv[])
{
    const int DIMS = 2;

    size_t **shapes = calloc(DIMS, sizeof(size_t *));
    
    // Allocate memory for dimensions ex: (2, 2)
    for (int i = 0; i < DIMS; ++i)
    {
        shapes[i] = (size_t *)calloc(2, sizeof(size_t));
    }

    // printf("Allocating memory for arr->dim[%d]\n", i);
    shapes[0][0] = 5;
    shapes[0][1] = 5;

    shapes[1][0] = 5;
    shapes[1][1] = 5;

    // shapes[2][0] = 2;
    // shapes[2][1] = 2;

    // shapes[3][0] = 2;
    // shapes[3][1] = 2;

    // shapes[4][0] = 2;
    // shapes[4][1] = 2;

    // shapes[5][0] = 2;
    // shapes[5][1] = 2;
    
    double_list_t *arr = new_double_list(DIMS, shapes);

    arr->ptr_copy = arr->ptr;
    ARR(atoi(argv[1]), atoi(argv[2]), atoi(argv[3])) = atoi(argv[4]);
    print_double_list(arr);

    free(arr->ptr_copy);
    free(arr);
    return 0;
}