#include <stdbool.h>
#include <stdio.h>

bool shared_bits(unsigned a, unsigned b);
void printBin(unsigned n);

int main(void) {
  unsigned a, b;
  int size = (int)sizeof(unsigned) * 8 - 1;

  printf("main: begin");
  do {
    printf("\nPut two integer numbers compare or some shit to quit: ");
    if((scanf("%d%d", &a, &b) != 2)) {
      break;
    }
    printBin(a);
    printBin(b);
    printf("\nThese two numbers are %s", shared_bits(a, b)? "true": "false");
  } while(1);
  printf("main: end\n");

  return 0;
}

bool shared_bits(unsigned a, unsigned b) {
  int count = 0;
  int size = (int)sizeof(unsigned) * 8 - 1;
  unsigned c = a & b;

  printf("\nshared_bits: begin");
  for(int i = size; i > -1; i--) {
    if(c & (1 << i)) {
      printf("\n%dth bits are equal", i + 1);
      count++;
    }
  }
  printf("\nshared_bits: end");

  return (count > 1)? true: false;
}

void printBin(unsigned n) {
  int size_in_bits = (int)sizeof(unsigned) * 8 - 1;

  printf("\n");
  for(int i = size_in_bits; i > -1; i--) {
      if(n & (1 << i)) {
        printf("1");
      } else {
        printf("0");
      }
    }
}