#include <stdio.h>

int size;

unsigned reverse_bits(unsigned n);

int main(void) {
  unsigned n;

  printf("main: begin");
  do {
    printf("\nPut integer number to bit inverse or some shit to quit: ");
    if((scanf("%d", &n) != 1)) {
      break;
    }
    printf("\n%*u --> %*u\n", size + 1, n, size + 1, reverse_bits(n));
  } while(1);
  printf("main: end\n");

  return 0;
}

unsigned reverse_bits(unsigned n) {
  unsigned ret = 0;
  size = (int)sizeof(unsigned) * 8 - 1;
  int count = 0;
  int flag_oddity = 0;

  printf("reverse_bits: begin");
  for(int i = size; i > -1; i--) {
    if(n & (1 << i)) {
      size = i;
      printf("\nnew size: %d", i);
      break;
    }
  }
  printf("\n");
  for(int i = size; i > -1; i--) {
    if(n & (1 << i)) {
      printf("1");
      ret += (1 << (size - i));
      count++;
      if(i % 2) {
        flag_oddity = 1;
      }
    } else {
      printf("0");
    }
  }
  printf(" --> ");
  for(int i = size; i > -1; i--) {
    if(ret & (1 << i)) {
      printf("1");
    } else {
      printf("0");
    }
  }
  printf("\nThere is an %s number", flag_oddity? "odd": "not odd");
  printf("\nnumber of binary digits: %d", count);
  printf("\nreverse_bits: end");

  return ret;
}