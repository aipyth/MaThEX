#pragma once
#include <inttypes.h>

typedef uint64_t (*hash_function) (unsigned char*);

typedef struct  {
    char* _key;
    uint64_t _hash;
} SimpleSetNode, str_set_node;


typedef struct  {
    str_set_node *nodes;
    uint64_t number_nodes;
    uint64_t used_nodes;
    hash_function hash_function;
} SimpleSet, str_simple_set;


str_simple_set* init_ss_set();
