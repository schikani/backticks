#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef char* str;

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
 

#define ARR(dim, row, col) arr->ptr[0][dim * (arr->dims[dim][0] * arr->dims[dim][1]) + row * arr->dims[dim][1] + col]
//arr3d[r][c][d]
// becomes:
// arr3d.data[r * (arr3d.b * arr3d.c) + c * arr3d.c + d];


long_list_t *new_long_list(size_t dims, size_t row, size_t col)
// long_list_t *new_long_list()
{
    // Allocate memory for long_list_t
    long_list_t *arr = (long_list_t *)calloc(1, sizeof(long_list_t));
    arr->no_of_dims = dims;
    // Allocate memory for dimensions ex: (2, 2)
    arr->dims = (size_t **)calloc(arr->no_of_dims, sizeof(size_t *));
    // Allocate memory for ptr with no of dimension
    arr->ptr = (long **)calloc(arr->no_of_dims, sizeof(long *));
    // Copy the pointer 
    arr->ptr_copy = arr->ptr;

    for (int i = 0; i < arr->no_of_dims; ++i)
    {
        arr->dims[i] = (size_t *)calloc(2, sizeof(size_t));
        printf("Allocating memory for arr->dim[%d]\n", i);
        arr->dims[i][0] = row;
        arr->dims[i][1] = col;
    }
    printf("NO OF DIMS: %ld\n\n", arr->no_of_dims);

    // DIMENSIONS
    for (size_t i = 0; i < arr->no_of_dims; ++i)
    {   
        // printf("%ld | %ld | %ld\n", arr->dims[i][0], arr->dims[i][1], arr->dims[i][2]);
        // ROWS[0] and COLS[1]
        arr->ptr[i] = calloc(arr->dims[i][0]*arr->dims[i][1], sizeof(long));

        // memset(arr->ptr, (long)arr->no_of_dims*arr->dims[i][0]*arr->dims[i][1], 1);
        for (size_t j = 0; j < arr->dims[i][0]*arr->dims[i][1]; ++j)
        {
            arr->ptr[i][j] = 0;
            // printf("%ld | %ld\n", i, j);
        }
    }
    return arr;
}

void print_list(long_list_t *arr)
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


int main(int argc, char *argv[])
{
    long_list_t *arr = new_long_list(5, 5, 5);
    arr->ptr_copy = arr->ptr;
    ARR(atoi(argv[1]), atoi(argv[2]), atoi(argv[3])) = atoi(argv[4]);
    print_list(arr);

    free(arr->ptr_copy);
    free(arr);
    return 0;
}