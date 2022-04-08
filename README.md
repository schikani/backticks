<img src="https://github.com/schikani/backticks/blob/main/LOGO.png" width="200" height="200">

### A Transpiler written in Python to convert source code from .bt to .h/.c

#### Example file `test.bt` in `src` dir can be transpiled with `./bt ./src/test.bt` command

### Backticks source
```typescript
let num1 = 45;
let num2 = 67.53;

printl(`num1+num2 = {num1+num2}`);

let line = `*`;
let char_count = 0;

printl(`Before:\t{line}`);
loop until char_count < 30 
{
    line += `*`;
    char_count += 1;
}
printl(`After:\t{line}`);
Output
```
num1+num2 = 112.530000
Before:	*
After:	*******************************
```

### ~ Generated C header and source files ~
### Header file
```H
#ifndef _TEST_H_
#define _TEST_H_

#include "_bt_inbuilts_.h"

typedef struct
{
long num1;
double num2;
char * line;
long char_count;

} _TEST_H_VARS;

extern _TEST_H_VARS test;

#endif
```
### Source file
```C
#include "test.h"
_TEST_H_VARS test;

int main(int argc, char *argv[])
{
    test.num1 = 45;
    test.num2 = 67.53;
    printf("num1+num2 = %f\n", test.num1 + test.num2);
    test.line = calloc(strlen("*") + 1, sizeof(char));
    strcpy(test.line, "*");
    test.char_count = 0;
    printf("Before:\t%s\n", test.line);
    while (test.char_count < 30)
    {
        test.line = realloc(test.line, (strlen(test.line) + strlen("*")) * sizeof(char));
        strcat(test.line, "*");
        test.char_count += 1;
    }
    printf("After:\t%s\n", test.line);

    return 0;
}

```
