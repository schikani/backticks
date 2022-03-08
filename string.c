#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STRINGS     500

typedef struct
{
    char *strings[MAX_STRINGS];
    long strs_ptr_len;
} _str_ptr_t;


void _str_ptr_init(_str_ptr_t *_str_ptr)
{   
    _str_ptr->strings[_str_ptr->strs_ptr_len] = (char *)calloc(1, sizeof(char *));
}

char *str_new(_str_ptr_t *_str_ptr, char *str)
{
    _str_ptr_init(_str_ptr);
    _str_ptr->strings[_str_ptr->strs_ptr_len] = (char *)calloc(strlen(str)+1, sizeof(char)); 
    strcpy(_str_ptr->strings[_str_ptr->strs_ptr_len], str);
    _str_ptr->strs_ptr_len++;

    // Return strs_ptr_len - 1 because of the incremented value
    return _str_ptr->strings[_str_ptr->strs_ptr_len - 1];
}


char *str_cat(char *dest, char *from)
{
    dest = (char *)realloc(dest, sizeof(char)*(strlen(from) + strlen(dest)));
    strcat(dest, from);

    return dest;
}

void str_del(_str_ptr_t *_str_ptr, char *str)
{
    free(str);
    str = NULL;
    _str_ptr->strs_ptr_len--;
}

int main(int argc, char *argv[])
{
    _str_ptr_t str;
    str.strs_ptr_len = 0;
    char *s = str_new(&str, "STRING START");
    // char *str1 = str_new(&str, "ONE");
    // char *str2 = str_new(&str, "TWO");
    // char *str3 = str_new(&str, "THREE");
    // char *str4 = str_new(&str, "FOUR");
    // char *str5 = str_new(&str, "FIVE");   
    // char *str6 = str_new(&str, "SIX");
    // char *str7 = str_new(&str, "SEVEN");
    for (int i = 0; i < 200; ++i)
    {
        str_cat(s, "-");
    }
    str_cat(s, "STRING END");

    printf("TOTAL STRINGS: %lu\n\n", str.strs_ptr_len);
    printf("%s\n", s);
    
    str_del(&str, s);

    return 0;
}



