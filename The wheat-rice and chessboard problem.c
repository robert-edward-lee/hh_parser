#include <limits.h>
#include <stdio.h>

typedef unsigned long long ull;

void printBin(ull n);
ull squares_needed(ull n);

int main(void) {
  ull n;
  int size = (int)sizeof(ull) * 8 - 1;

  printf("main: begin");
  do {
    printf("\nPut integer number or some shit to quit: ");
    if((scanf("%llu", &n) != 1)) {
      break;
    }
    printBin(n);
    squares_needed(n);
  } while(1);
  printf("main: end\n");

  return 0;
}

ull squares_needed(ull n) {
  int peek = (int)sizeof(n) * 8 - 1;

  printf("squares_needed: begin");
  n &= ULLONG_MAX;
  printBin(n);
  for(int i = peek; i > -1; i--) {
    if(n & (1 << i)) {
      return peek - i + 1;
    }
  }
  printf("squares_needed: end");

  return 0;
}

void printBin(ull n) {
  int size_in_bits = (int)sizeof(ull) * 8 - 1;

  printf("\n");
  for(int i = size_in_bits; i > -1; i--) {
      if(n & (1 << i)) {
        printf("1");
      } else {
        printf("0");
      }
    }
}