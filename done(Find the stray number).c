#include <stddef.h>
#include <stdio.h>

#define SIZE 7


int main(void) {
  int arr[SIZE] = {17, 1, 17, 17, 17, 17, 17};
  int i;
  printf("Init: %d\n", arr[0]);
  if((arr[0] != arr[1]) && (arr[1] == arr[2])) {
    return arr[0];
  }
  for(i = 0; i < SIZE; i++) {
    if(arr[0] != arr[i]) {
      printf("%d\n", arr[i]);
      return arr[i];
    }
  }
}
