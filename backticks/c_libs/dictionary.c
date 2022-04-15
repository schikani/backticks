#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct nlist 
{ /* table entry: */
    struct nlist *next; /* next entry in chain */
    char *key; /* defined name */
    char *val; /* replacement text */
} nlist;

#define HASHSIZE 101
static nlist *hashtab[HASHSIZE]; /* pointer table */

/* hash: form hash value for string s */
unsigned hash(char *s)
{
    unsigned hashval;
    for (hashval = 0; *s != '\0'; s++)
      hashval = *s + 31 * hashval;
    return hashval % HASHSIZE;
}

/* find: look for s in hashtab */
nlist *find(char *key)
{
    nlist *np;
    for (np = hashtab[hash(key)]; np != NULL; np = np->next)
        if (strcmp(key, np->key) == 0)
          return np; /* found */
    return NULL; /* not found */
}

/* install: put (name, defn) in hashtab */
nlist *update(char *key, char *val)
{
    nlist *np;
    unsigned hashval;
    if ((np = find(key)) == NULL) { /* not found */
        np = ( nlist *) malloc(sizeof(*np));
        if (np == NULL || (np->key = strdup(key)) == NULL)
          return NULL;
        hashval = hash(key);
        np->next = hashtab[hashval];
        hashtab[hashval] = np;
    } else /* already there */
        free((void *) np->val); /*free previous val */
    if ((np->val = strdup(val)) == NULL)
       return NULL;
    return np;
}

int main()
{
    update("key1", "val1");
    update("key2", "val2");

    nlist *list = find("key1");
    printf("%s\n", list->val);

    return 0;
}