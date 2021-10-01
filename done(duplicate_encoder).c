#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(void) {
  char* STR = "PeDoFfKaSePEr";
  int i = 0, j = 0;
  char* strOut = malloc(strlen(STR) + 1);
  strOut[0] = 0;
  int flag;

  while(STR[i] != 0) {
    j = i + 1;
    flag = 0;
    while(j != i) {
      if(STR[j] == 0) {
        j = 0;
        if(j == i) {
          break;
        }
      }
      if(tolower(STR[i]) == tolower(STR[j])) {
        strcat(strOut, ")");
        flag = 1;
        break;
      }
      j++;
    }
    if(flag == 0) {
      strcat(strOut, "(");
    }
    i++;
  }
  return 0;
}
