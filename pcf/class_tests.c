
#include "class_tests.h"
_CLASS_TESTS_H_VARS class_tests;

void __Person_class_tests_set_name(struct Person_class_tests *self, str name);
void __Person_class_tests_set_num(struct Person_class_tests *self, long num);

void __Person_class_tests_set_name(struct Person_class_tests *self, str name)
{
self->name=name;

}

str Person_class_tests_get_name(struct Person_class_tests *self)
{
return self->name;
}

void __Person_class_tests_set_num(struct Person_class_tests *self, long num)
{
self->num=num;

}

long Person_class_tests_get_num(struct Person_class_tests *self)
{
return self->num;
}

Person_class_tests *Person_class_tests__init__(str name, long num)
{
Person_class_tests *self = calloc(1, sizeof(Person_class_tests));
self->name = calloc(strlen(name)+1, sizeof(char));
strcpy(self->name, name);
self->num = num;
self->set_name = __Person_class_tests_set_name;
self->get_name = Person_class_tests_get_name;
self->set_num = __Person_class_tests_set_num;
self->get_num = Person_class_tests_get_num;
return self;
}


int main(int argc, char *argv[])
{
class_tests.array = new_str_list(20);
check_reserve_str_list(class_tests.array);
class_tests.array->ptr[0] = calloc(strlen("Shivang")+1, sizeof(char));
strcpy(class_tests.array->ptr[0], "Shivang");
class_tests.array->len += 1;
check_reserve_str_list(class_tests.array);
class_tests.array->ptr[1] = calloc(strlen( "Rucha")+1, sizeof(char));
strcpy(class_tests.array->ptr[1],  "Rucha");
class_tests.array->len += 1;
check_reserve_str_list(class_tests.array);
class_tests.array->ptr[2] = calloc(strlen( "Bhagya")+1, sizeof(char));
strcpy(class_tests.array->ptr[2],  "Bhagya");
class_tests.array->len += 1;
class_tests.person1 = Person_class_tests__init__("xyz",879887);
printf("%d\n",class_tests.person1->get_num(class_tests.person1));
class_tests.person1->set_num(class_tests.person1,878052);
printf("%d\n",class_tests.person1->get_num(class_tests.person1));
printf("%s\n",class_tests.person1->get_name(class_tests.person1));
class_tests.person1->set_name(class_tests.person1,"Shivang");
printf("%s\n",class_tests.person1->get_name(class_tests.person1));


return 0;
}
