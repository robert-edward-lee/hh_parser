
#include <stdio.h>
#define MAX 100

void squeeze(char* str);

int main (void) {
  char str0[MAX];
  int i, c;

  for (i = 0; (c = getchar()) != '\n'; i++)
    str0[i] = c;
  str0[i] = '\0';

  squeeze (str0);

  printf("%s\n", str0);
}

void squeeze(char* str) {
  int i, j;

  for(i = 0, j = 0; str[i] != '\0'; i++) {
    if(!((str[i] == 'a') || (str[i] == 'e') || (str[i] == 'i') || (str[i] == 'o') || (str[i] == 'u') ||
         (str[i] == 'A') || (str[i] == 'E') || (str[i] == 'I') || (str[i] == 'O') || (str[i] == 'U'))) {
      str[j++] = str[i];
    }
  }
  str[j] = '\0';
}
