#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct 
{
  size_t row;
  size_t col;
  long *ptr;
  long *ptr_copy;
} long_list_t;
 

// Int3d arr3d = { 2, 3, 4 };
// arr3d.data = malloc(arr3d.a * arr3d.b * arr3d.c * sizeof *arr3d.data);

// //arr3d[r][c][d]
// // becomes:
// arr3d.data[r * (arr3d.b * arr3d.c) + c * arr3d.c + d];

long_list_t *new_long_list(size_t row, size_t col)
{
    long_list_t *arr = calloc(1, sizeof(long_list_t));
    arr->row = row;
    arr->col = col;
    arr->ptr = calloc(arr->row*arr->col, sizeof(long));
    arr->ptr_copy = arr->ptr;
    return arr;
}

void print_list(long_list_t *arr)
{
    for (size_t i = 0; i < arr->row; i++)
    {
        printf("|");
        for (size_t j = 0; j < arr->col; j++)
        {
            printf(" %ld |", *(arr->ptr+i+j));
        }
        printf("\n");
    }
}

int main()
{

    long_list_t *arr = new_long_list(5, 5);
    print_list(arr);


    // arr.data = malloc(arr3d.a * arr3d.b * arr3d.c * sizeof *arr3d.data);

    return 0;
}