#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define STR "This is an example!"

void reverseWord(char* word) {
  int len = strlen(word);
  char buf;
  printf("%s\n", word);
  for (int i = 0; i < len / 2 + 1; i++) {
    buf = word[i];
    word[i] = word[len - i];
    word[len - i] = buf;
  }
  printf("%s\n", word);
  return;
}

char* main() {
  char* strOut = (char*)malloc(strlen(STR) + 1);
  char* word;
  strOut[0] = 0;
  word = strtok(STR, " ");
  while(word != NULL) {
    reverseWord(word);
    strcat(strOut, word);
    word = strtok(NULL, " ");
  }
  return strOut;
}
