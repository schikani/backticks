
#ifndef _CLASS_TESTS_H_
#define _CLASS_TESTS_H_

#include "_bt_builtins_.h"


typedef struct Person_class_tests
{
str name;
long num;
void (*set_name)(struct Person_class_tests *self, str name);
str (*get_name)(struct Person_class_tests *self);
void (*set_num)(struct Person_class_tests *self, long num);
long (*get_num)(struct Person_class_tests *self);

}Person_class_tests;


typedef struct
{
str_list_t *array;
Person_class_tests *person1;

} _CLASS_TESTS_H_VARS;
extern _CLASS_TESTS_H_VARS class_tests;


Person_class_tests *Person_class_tests__init__(str name, long num);
str Person_class_tests_get_name(struct Person_class_tests *self);
long Person_class_tests_get_num(struct Person_class_tests *self);



#endif
