#include <stddef.h>
#include <stdio.h>


/* dzfhnadfhn
dfhsdfh
dfhdfhsd */


int main(void) {
  char ret[4096] = {0};
  size_t n = 4;
  const char *const names[] = {"Alex", "Jacob", "Mark", "Max"};
  switch(n) {
      case 0: {
        sprintf(ret, "no one likes this");
        break;
      }
      case 1: {
        sprintf(ret, "%s likes this", names[0]);
        break;
      }
      case 2: {
        sprintf(ret, "%s and %s like this", names[0], names[1]);
        break;
      }
      case 3: {
        sprintf(ret, "%s, %s and %s like this", names[0], names[1], names[2]);
        break;
      }
      default: {
        sprintf(ret, "%s, %s and %ld others like this", names[0], names[1], n - 2);
        break;
      }
  }
  printf("\n%s\n", ret);
  return 0;
}