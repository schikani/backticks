#include "_bt_builtins_.h"


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
                    printf(__ARR__(i, j, k) ? "True]": "False]");  
                }
                else
                {
                    printf(__ARR__(i, j, k) ? "True, ": "False, ");  
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
                printf(k == arr->dims[i][1]-1 ? "%ld]": "%ld, ", __ARR__(i, j, k));
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
                printf(k == arr->dims[i][1]-1 ? "%f]": "%f, ", __ARR__(i, j, k));
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
                printf(k == arr->dims[i][1]-1 ? "%s]": "%s, ", __ARR__(i, j, k));
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
    __ARR__(atoi(argv[1]), atoi(argv[2]), atoi(argv[3])) = atoi(argv[4]);
    print_double_list(arr);

    free(arr->ptr_copy);
    free(arr);
    return 0;
}