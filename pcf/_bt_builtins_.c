#include "_bt_builtins_.h"

str _bt_input(FILE *in)
{
    size_t alloc_length = 64;
    size_t cumulength = 0;
    str data = malloc(alloc_length);
    while (1) {
        str cursor = data + cumulength; // here we continue.
        str ret = fgets(cursor, alloc_length - cumulength, in);
        // printf("r %p %p %zd %zd %zd\n", data, cursor, cumulength, alloc_length, alloc_length - cumulength);
        if (!ret) {
            // Suppose we had EOF, no error.
            // we just return what we read till now...
            // there is still a \0 at cursor, so we are fine.
            break;
        }
        size_t newlength = strlen(cursor); // how much is new?
        cumulength += newlength; // add it to what we have.
        if (cumulength < alloc_length - 1 || data[cumulength-1] == '\n') {
            // not used the whole buffer... so we are probably done.
            break;
        }
        // we need more!
        // At least, probably.
        size_t newlen = alloc_length * 2;
        str r = realloc(data, newlen);
        // printf("%zd\n", newlen);
        if (r) {
            data = r;
            alloc_length = newlen;
        } else {
            // realloc error. Return at least what we have...
            // TODO: or better free and return NULL?
            return data;
        }
    }
    str r = realloc(data, cumulength + 1);
    // printf("%zd\n", cumulength + 1);
    return r ? r : data; // shrinking should always have succeeded, but who knows?
}

bool_list_t *new_bool_list(size_t reserve)
{
    bool_list_t *arr = calloc(1, sizeof(bool_list_t));
    arr->len = 0;
    arr->reserve = reserve;
    arr->ptr = calloc(arr->reserve, sizeof(bool));
    arr->ptr_copy = arr->ptr;

    return arr;
}

void check_reserve_bool_list(bool_list_t *arr)
{
    if (arr->len == arr->reserve)
    {
        arr->reserve += arr->len;
        printf("Reallocating memory!\n");
        arr->ptr = realloc(arr->ptr, (arr->reserve)*sizeof(bool));
        if (arr->ptr == NULL)
        {
            printf("Memory allocation failed!\n");
            exit(1);
        }
    }
}

double_list_t *new_double_list(size_t reserve)
{
    double_list_t *arr = calloc(1, sizeof(double_list_t));
    arr->len = 0;
    arr->reserve = reserve;
    arr->ptr = calloc(arr->reserve, sizeof(double));
    arr->ptr_copy = arr->ptr;

    return arr;
}

void check_reserve_double_list(double_list_t *arr)
{
    if (arr->len == arr->reserve)
    {
        arr->reserve += arr->len;
        printf("Reallocating memory!\n");
        arr->ptr = realloc(arr->ptr, (arr->reserve)*sizeof(double));
        if (arr->ptr == NULL)
        {
            printf("Memory allocation failed!\n");
            exit(1);
        }
    }
}

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
        arr->reserve += arr->len;
        printf("Reallocating memory!\n");
        arr->ptr = realloc(arr->ptr, (arr->reserve)*sizeof(long));
        if (arr->ptr == NULL)
        {
            printf("Memory allocation failed!\n");
            exit(1);
        }
    }
}

str_list_t *new_str_list(size_t reserve)
{
    str_list_t *arr = calloc(1, sizeof(str_list_t));
    arr->len = 0;
    arr->reserve = reserve;
    arr->ptr = calloc(arr->reserve, sizeof(str));
    arr->ptr_copy = arr->ptr;

    return arr;
}

void check_reserve_str_list(str_list_t *arr)
{
    if (arr->len == arr->reserve)
    {
        arr->reserve += arr->len;
        printf("Reallocating memory!\n");
        arr->ptr = realloc(arr->ptr, (arr->reserve)*sizeof(str));
        if (arr->ptr == NULL)
        {
            printf("Memory allocation failed!\n");
            exit(1);
        }
    }
}

