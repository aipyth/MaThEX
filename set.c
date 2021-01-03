#include "set.h"

str_simple_set* init_ss_set() {
  str_simple_set* set = malloc(sizeof(str_simple_set));
  set->number_nodes = 0;
  set->used_nodes = 0;
  return set;
}

int add_to_set(str_simple_set* set, char* s) {
  
}
