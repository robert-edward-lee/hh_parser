#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define str "  Abcd   Aahhhhhhhhhhhhhhhhz  "

char* cryptWord(char* word);
char* reverseLetters(char* word);

int main(void) {
  size_t i = 0, k = 0;
  char *buf, *ret;
  printf("\nmain: begin");
  printf("\n\t%s", str);
  if(str == NULL) {
    return 0;
  }
  buf = malloc(sizeof(str));
  ret = malloc(2 * sizeof(str));
  buf[0] = 0;
  ret[0] = 0;
  printf("\n\t%s\rINIT:", ret);
  while(str[i] == ' ' && str[i] != 0) {
    i++;
  }
  do {
    if(str[i] != ' ') {
      strncat(buf, &str[i], 1);
    } else {
      strcat(ret, cryptWord(buf));
      strcat(ret, " ");
      k++;
      printf("\n\t%s\r%luth:", ret, k);
      buf[0] = 0;
      while(str[i] == ' ' && str[i] != 0) {
        i++;
      }
    }
    i++;
  } while(str[i] != 0);
  strcat(ret, cryptWord(buf));
  printf("\n\t%s\rLAST:", ret);
  printf("\nmain: end\n");
  return 0;
}

char* cryptWord(char* word) {
  printf("\ncryptWord() {");
  printf("\n\t%s\rIN:", word[0]? word: "\"is empty\"");
  char* ret = malloc(sizeof(word) + 2);
  ret[0] = 0;
  if(word[0] != 0) {
    char buf[4] = {0};
    sprintf(buf, "%d", (int)word[0]);
    strcat(ret, buf);
    strcat(ret, reverseLetters(word + 1));
  }
  printf("\n\t%s\rOUT:", ret[0]? ret: "\"is empty\"");
  printf("\n}");
  return ret;
}

char* reverseLetters(char* word) {
  size_t i;
  size_t size_word = strlen(word);
  char* ret = malloc(size_word + 1);
  for(i = 0; i < size_word; i++) {
    ret[i] = word[size_word - i - 1];
  }
  return ret;
}
