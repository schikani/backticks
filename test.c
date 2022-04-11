#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct 
{
  long **ptr;
  long **ptr_copy;
  size_t **dims;
  size_t no_of_dims;
} long_list_t;
 

// #define ARR(dim, row, col) (dim + row + col)

// #define ARR(dim, j, k) (arr->ptr[dim][j+k])

// #define ARR(i,j,k) (arr->ptr[i][arr->dims[i][0]*arr->dims[i][1]*i + arr->dims[i][1]*j + k])

#define ARR(i,j,k) *(arr->ptr[i]+j+k)

long_list_t *new_long_list(size_t dims, size_t row, size_t col)
// long_list_t *new_long_list()
{
    // Allocate memory for long_list_t
    long_list_t *arr = calloc(1, sizeof(long_list_t));
    arr->no_of_dims = dims;
    // Allocate memory for dimensions ex: (2, 2)
    arr->dims = (size_t **)calloc(arr->no_of_dims, sizeof(size_t *));
    // Allocate memory for ptr with no of dimension
    arr->ptr = (long **)calloc(arr->no_of_dims, sizeof(long *));

    for (int i = 0; i < arr->no_of_dims; ++i)
    {
        arr->dims[i] = (size_t *)calloc(2, sizeof(size_t));
        printf("Allocating memory for arr->dim[%d]\n", i);
        arr->dims[i][0] = row;
        arr->dims[i][1] = col;
    }
    printf("NO OF DIMS: %ld\n", arr->no_of_dims);

    // DIMENSIONS
    for (size_t i = 0; i < arr->no_of_dims; ++i)
    {   
        // ROWS[0] and COLS[1]
        arr->ptr[i] = calloc(arr->dims[i][0]*arr->dims[i][1], sizeof(long));
        for (size_t j = 0; j < arr->dims[i][0]*arr->dims[i][1]; ++j)
        {
            arr->ptr[i][j] = 0;
            // printf("%ld | %ld\n", i, j);
        }
    }

    arr->ptr_copy = arr->ptr;
    return arr;
}

void print_list(long_list_t *arr)
{
    for (size_t i = 0; i < arr->no_of_dims; i++)
    {
        // printf("DIMENSION: %ld\n", i);
        // ROW
        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            // arr->ptr[i][j] = 0;
            printf("|");
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                // printf(" %ld |", *arr->ptr[i]+j+k);
                printf(" %ld |", ARR(i, j, k));
            }

            printf("\n");
        }
        printf("\n");

    }
}

// void get_list(long_list_t *arr, size_t dim, size_t row, size_t col, long val)
// {
//     ARR(dim, row, col) = val;
//     // printf("%ld\n", ARR(dim, row, col));
// }

int main()
{
    long_list_t *arr = new_long_list(5, 5, 5);
    ARR(0, 0, 1) = 45;
    // arr->ptr[0][0] = 54;
    print_list(arr);

    return 0;
}