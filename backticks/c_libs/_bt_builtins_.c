#include "_bt_builtins_.h"

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