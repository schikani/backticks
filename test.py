def get_bt_list_src():
    source = ""
    
    types = ["bool", "double", "long", "str"]
    for t in types:
        source += f"""{t}_list_t *new_{t}_list(size_t reserve)
{{

    {t}_list_t *arr = calloc(1, sizeof({t}_list_t));
    arr->len = 0;
    arr->reserve = reserve;
    arr->ptr = calloc(arr->reserve, sizeof({t}));
    arr->ptr_copy = arr->ptr;

    return arr;
}}

void check_reserve_{t}_list({t}_list_t *arr)
{{
    if (arr->len == arr->reserve)
    {{
        printf("Reallocating memory!\\n");
        arr->ptr = realloc(arr->ptr, (arr->len+arr->reserve)*sizeof({t}));
        if (arr->ptr == NULL)
        {{
            printf("Memory allocation failed!\\n");
            exit(1);
        }}
    }}
}}

"""
    return source
