#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_NUM 4
#define STR "128.114.17.104"

uint32_t main(void) {
  char ip[] = STR;
  char buf[MAX_NUM] = {0};
  int i = 0, j = 0, bias = 0;
  uint32_t value = 0;
  while(bias < 4) {
    j = i;
    while((ip[j] != '.') && (ip[j] != 0)) {
      strncat(buf, &ip[j], 1);
      ++j;
    }
    value += (atoi(buf) << (24 - bias * 8));
    buf[0] = 0;
    i = j + 1;
    ++bias;
  }
  printf("%x", value);
  return value;
}
