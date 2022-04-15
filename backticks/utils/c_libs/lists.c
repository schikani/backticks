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

        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                __ARR__(i, j, k) = false;
            }
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

        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                __ARR__(i, j, k) = 0;
            }
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

        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                __ARR__(i, j, k) = 0.0f;
            }
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
        arr->ptr[i] = calloc(arr->dims[i][0]*arr->dims[i][1], sizeof(str));

        for (size_t j = 0; j < arr->dims[i][0]; ++j)
        {
            for (size_t k = 0; k < arr->dims[i][1]; ++k)
            {
                __ARR__(i, j, k) = NULL;
            }
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



int main(int argc, char *argv[])
{

    const size_t DIMS = argc-2;
    const str type = argv[1];
    char *dims = argv[2];

    // printf("%d\n", DIMS);

    size_t **shapes = calloc(DIMS, sizeof(size_t *));
    
    // Allocate memory for dimensions ex: (2, 2)
    for (int i = 0, j = 1; i < DIMS; ++i, ++j)
    {
        shapes[i] = (size_t *)calloc(2, sizeof(size_t));
        shapes[i][0] = atoi(strtok(argv[j+1], ","));
        shapes[i][1] = atoi(strtok(NULL, ","));
    }
    if (strcmp(type, "bool") == 0)
    {
        bool_list_t *arr = new_bool_list(DIMS, shapes);
        print_bool_list(arr);
    }
    else if (strcmp(type, "long") == 0)
    {
        long_list_t *arr = new_long_list(DIMS, shapes);
        print_long_list(arr);
    }
    else if (strcmp(type, "double") == 0)
    {
        double_list_t *arr = new_double_list(DIMS, shapes);
        print_double_list(arr);
    }
    else if (strcmp(type, "str") == 0)
    {
        str_list_t *arr = new_str_list(DIMS, shapes);
        print_str_list(arr);
    }


    // free(arr->ptr_copy);
    // free(arr);

    return 0;
}