#include <stdio.h>
#include <stdlib.h>

const int dim1=3, dim2=5, dim3=2;  /* Global variables, dimension*/

// #define ARR(i,j,k) (arr[dim2*dim3*i + dim3*j + k])
// #define ARR(i,j,k) (arr[i+(j*k)])


void print_arr(double *arr)
{
    for (size_t i = 0; i < dim1; ++i)
    {
        for (size_t j = 0; j < dim2; ++j)
        {
            printf("|");
            for (size_t k = 0; k < dim3; ++k)
            {
                printf(" %f |", arr[i+j+k]);
            }
            printf("\n");
        }
        printf("\n");

    }
}

int main()
{
    double *arr = (double *)calloc(dim1*dim2*dim3, sizeof(double));

    *(arr[0]+1+0) = 45;
    print_arr(arr);

    return 0;
}