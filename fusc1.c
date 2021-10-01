#include <stdio.h>

typedef struct quotient_t {
  int numerator;
  int denominator;
};

int fusc(int n);

int main(void) {
  long inx, i, j;
  unsigned long long* arr;

  printf("\nPut order of fusc: ");
  scanf("%ld", &inx);
  printf("Here we are!\n");
  for(i = 0; i < inx; i++) {
    printf("%d ", fusc(2 * i));
  }
  printf("\n");
  for(i = 0; i < inx; i++) {
    printf("- ");
  }
  printf("\n");
  for(i = 0; i < inx; i++) {
    printf("%d ", fusc(2 * i + 1));
  }
  printf("\n");
  return 0;
}

int fusc(int n) {
  if(n < 2) {
    return n;
  }
  return (n % 2)? fusc(n / 2) + fusc(n / 2 + 1): fusc(n / 2);
}