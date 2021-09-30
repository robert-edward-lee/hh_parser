#include <stdio.h>

int main (void) {
  int i, count = 0;
  char string[4096];

  scanf("%s", string);
  for(i = 0; string[i] != 0; i++) {
    switch(string[i]) {
        case '0' ... '9': {
          case '*':
          case '#':
          count++;
          break;
        }
        case 'a': {
          case 'd':
          case 'g':
          case 'j':
          case 'm':
          case 'p':
          case 't':
          case 'w':
          count += 2;
          break;
        }
        case 'b': {
          case 'e':
          case 'h':
          case 'k':
          case 'n':
          case 'q':
          case 'u':
          case 'x':
          count += 3;
          break;
        }
        case 'c': {
          case 'f':
          case 'i':
          case 'l':
          case 'o':
          case 'r':
          case 'v':
          case 'y':
          count += 4;
          break;
        }
        case 's': {
          case 'z':
          count += 5;
          break;
        }
        default: {
          break;
        }
    }
  }
  printf("\n%d\n", count);

  return 0;
}