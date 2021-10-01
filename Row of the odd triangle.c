#include <stdlib.h>
#include <stdio.h>

void printSpaces(long spaces);
void printString(unsigned long long* arr, long size_arr, long total_strings);

int main(void) {
  long inx, i, j;
  unsigned long long* arr;

  printf("\nPut order of triangle: ");
  scanf("%lu", &inx);
  printf("Here we are!");
  for(i = 1; i <= inx; i++) {
    arr = malloc(sizeof(unsigned long long) * i);
    arr[0] = (unsigned long long)i + (unsigned long long)(i - 1) * (i - 1);
    for(j = 1; j < i; j++) {
      arr[j] = arr[j - 1] + 2;
    }
    printString(arr, i, inx);
    free(arr);
  }
  printf("\n");
  return 0;
}


void printString(unsigned long long* arr, long size_arr, long total_strings) {
  long i;
  printf("\n");
  printSpaces(total_strings - size_arr);
  for(i = 0; i < size_arr; i++) {
    printf("%llu ", arr[i]);
  }
  printSpaces(total_strings - size_arr - 1);
}

void printSpaces(long spaces) {
  long i;
  for(i = 0; i < spaces; i++) {
    printf(" ");
  }
}