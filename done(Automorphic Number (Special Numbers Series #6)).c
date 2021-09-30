#include <stdio.h>

int main(void) {
  int number;
  long powTens;
  do {
    powTens = 1;
    printf("Put number or '0': ");
    scanf("%d", &number);
    long modTens = number * number - number;
    do {
      powTens *= 10;
    } while(powTens < number);
    // while(modTens > powTens) {
    //   powTens *= 10;
    // }
    printf("\nmodTens = %ld %% powTens = %ld == %ld", modTens, powTens, modTens % powTens);
    if(modTens % powTens == 0) {
      printf("\nAutomorphic\n");
    } else {
      printf("\nNot!!\n");
    }
  } while (number != 0);
  return 0;
}

