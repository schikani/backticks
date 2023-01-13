
#include "list_test.h"
_LIST_TEST_H_VARS list_test;

void list_test_list_test(str_list_t *array);

void list_test_list_test(str_list_t *array)
{
for (size_t _i_ = 0; _i_ < array->len; ++_i_) {str l = array->ptr[_i_];
printf("%s\n",l);
}

}


int main(int argc, char *argv[])
{
list_test.array = new_str_list(20);
check_reserve_str_list(list_test.array);
list_test.array->ptr[0] = calloc(strlen("Shivang")+1, sizeof(char));
strcpy(list_test.array->ptr[0], "Shivang");
list_test.array->len += 1;
check_reserve_str_list(list_test.array);
list_test.array->ptr[1] = calloc(strlen( "Rucha")+1, sizeof(char));
strcpy(list_test.array->ptr[1],  "Rucha");
list_test.array->len += 1;
check_reserve_str_list(list_test.array);
list_test.array->ptr[2] = calloc(strlen( "Bhagya")+1, sizeof(char));
strcpy(list_test.array->ptr[2],  "Bhagya");
list_test.array->len += 1;
list_test_list_test(list_test.array);
printf("\n");
check_reserve_str_list(list_test.array);
list_test.array->ptr[list_test.array->len] = calloc(strlen("Yatha")+1, sizeof(char));
strcpy(list_test.array->ptr[list_test.array->len], "Yatha");
list_test.array->len += 1;
check_reserve_str_list(list_test.array);
list_test.array->ptr[list_test.array->len] = calloc(strlen("Dev")+1, sizeof(char));
strcpy(list_test.array->ptr[list_test.array->len], "Dev");
list_test.array->len += 1;
list_test_list_test(list_test.array);


return 0;
}
