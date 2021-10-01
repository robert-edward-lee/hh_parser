

#include <stdio.h>

int next_higher(int n);
void printBin(unsigned n);

int main(void) {
  unsigned n;
  int size = (int)sizeof(unsigned) * 8 - 1;

  printf("main: begin");
  do {
    printf("\nPut integer number or some shit to quit: ");
    if((scanf("%d", &n) != 1)) {
      break;
    }
    printf("\nInit:\n\t");
    printBin(n);
    n = next_higher(n);
    printf("\nResult:\n\t");
    printBin(n);
    printf("\n");
  } while(1);
  printf("main: end\n");

  return 0;
}

int next_higher(int n) {
  int peek = (int)sizeof(n) * 8 - 1;
  int count = 0;

  printf("\nnext_higher: begin");
  for(int i = peek; i > -1; i--) {
    if(n & (1 << i)) {
      peek = i;
      printf("\nOldest bit on %dth position!", i);
      break;
    }
  }
  do {
    count++;
    n++;
    printf("\n%dth step: n = %d\n\t", count, n);
    printBin(n);
  } while(!(n & (1 << peek)));
  printf("\nnext_higher: end\n");

  return n;
}

void printBin(unsigned n) {
  int size_in_bits = (int)sizeof(unsigned) * 8 - 1;

  for(int i = size_in_bits; i > -1; i--) {
      if(n & (1 << i)) {
        printf("1");
      } else {
        printf("0");
      }
    }
}