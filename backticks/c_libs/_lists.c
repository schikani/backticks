#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef char* str;

typedef struct 
{
    long *ptr;
    long *ptr_copy;
    size_t len;
    size_t reserve;

} long_list_t;


long_list_t *new_long_list(size_t reserve)
{

    long_list_t *arr = calloc(1, sizeof(long_list_t));
    arr->len = 0;
    arr->reserve = reserve;
    arr->ptr = calloc(arr->reserve, sizeof(long));
    arr->ptr_copy = arr->ptr;

    return arr;
}

void check_reserve_long_list(long_list_t *arr)
{
    if (arr->len == arr->reserve)
    {
        printf("Reallocating memory!\n");
        arr->ptr = realloc(arr->ptr, (arr->len+arr->reserve)*sizeof(long));
        if (arr->ptr == NULL)
        {
            printf("Memory allocation failed!\n");
            exit(1);
        }
    }
}

int main(int argc, char *argv[])
{
    long_list_t *l_list = new_long_list(5);
    return 0;
}