#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef char* str;


// ---------------------------------------------------------------------------------------
typedef struct class_Hobby
{
    str hobby_name;
    str hobby_description;
    void (*set_hobby_name)(struct class_Hobby *self, str hobby_name);
    str (*get_hobby_name)(struct class_Hobby *self);
    void (*set_hobby_description)(struct class_Hobby *self, str hobby_description);
    str (*get_hobby_description)(struct class_Hobby *self);
    
} class_Hobby;
class_Hobby *class_Hobby__init__();
void class_Hobby_set_hobby_name(class_Hobby *self, str hobby_name);
str class_Hobby_get_hobby_name(class_Hobby *self);
void class_Hobby_set_hobby_description(class_Hobby *self, str hobby_description);
str class_Hobby_get_hobby_description(class_Hobby *self);




void class_Hobby_set_hobby_name(class_Hobby *self, str hobby_name)
{   
    strcpy(self->hobby_name, hobby_name);
}

str class_Hobby_get_hobby_name(class_Hobby *self)
{
    return self->hobby_name;
}

void class_Hobby_set_hobby_description(class_Hobby *self, str hobby_description)
{   
    strcpy(self->hobby_description, hobby_description);
}

str class_Hobby_get_hobby_description(class_Hobby *self)
{
    return self->hobby_description;
}

class_Hobby *class_Hobby__init__()
{
    class_Hobby *self = calloc(1, sizeof(class_Hobby));
    self->hobby_name = calloc(20, sizeof(char));
    strcpy(self->hobby_name, "Football");
    self->hobby_description = calloc(200, sizeof(char));
    strcpy(self->hobby_description, "I like to play Football. It is one of the most played and watched game in the world!");
    self->set_hobby_name = class_Hobby_set_hobby_name;
    self->set_hobby_description = class_Hobby_set_hobby_description;
    self->get_hobby_name = class_Hobby_get_hobby_name;
    self->get_hobby_description = class_Hobby_get_hobby_description;
    return self;
}
// ---------------------------------------------------------------------------------------


// ---------------------------------------------------------------------------------------
typedef struct class_Person
{
    class_Hobby *class_Hobby;
    str name;
    long age;
    str (*get_name)(struct class_Person *self);
    void (*set_name)(struct class_Person *self, str name);
} class_Person;
class_Person *class_Person__init__();
str class_Person_get_name(class_Person *self);
void class_Person_set_name(class_Person *self, str name);


str class_Person_get_name(class_Person *self)
{   
    return self->name;
}

void class_Person_set_name(class_Person *self, str name)
{
    strcpy(self->name, name);
}

class_Person *class_Person__init__()
{
    class_Person *self = calloc(1, sizeof(class_Person));
    self->age = 25;
    self->name = calloc(20, sizeof(char));
    strcpy(self->name, "Shivang");
    self->set_name = class_Person_set_name;
    self->get_name = class_Person_get_name;
    // initialize derived class
    self->class_Hobby = class_Hobby__init__();
    return self;
}
// ---------------------------------------------------------------------------------------


int main()
{
    class_Person *person1 = class_Person__init__();
    class_Person *person2 = class_Person__init__();



    printf("person1: %s\n", person1->get_name(person1));
    printf("person2: %s\n", person2->get_name(person2));

    person2->set_name(person2, "Bhagya");

    printf("person1: %s\n", person1->get_name(person1));
    printf("person2: %s\n", person2->get_name(person2));

    person1->set_name(person1, "Darshi");

    printf("person1: %s\n", person1->get_name(person1));
    printf("person2: %s\n", person2->get_name(person2));

    printf("person1: %s\n", person1->class_Hobby->hobby_name);
    printf("person2: %s\n", person2->class_Hobby->hobby_name);

    printf("person1: %s\n", person1->class_Hobby->hobby_description);
    printf("person2: %s\n", person2->class_Hobby->hobby_description);

    // printf("person1: %s\n", person1->class_Hobby->get_hobby_name);
    // printf("person2: %s\n", person2->class_Hobby->hobby_description);

    person1->class_Hobby->set_hobby_description(person1->class_Hobby, "I usually don't play football nowadays.");
    printf("person1: %s\n", person1->class_Hobby->hobby_description);



    return 0;
}