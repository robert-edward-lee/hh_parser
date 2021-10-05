#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUMBER_OF_THREADS 10

void *print_hello_world(void *tid);

int main(int argc, char *argv[]) {
  /* Основная программа создает 10 потоков, а затем осуществляет выход. */
  pthread_t threads[NUMBER_OF_THREADS];
  int numbers[NUMBER_OF_THREADS];
  int status, i;

  for(i=0; i < NUMBER_OF_THREADS; i++) {
    numbers[i] = i + 1;
    printf("Это основная программа. Создание потока № %d\n", numbers[i]);
    status = pthread_create(&threads[i], NULL, print_hello_world, (void*)&(numbers[i]));
    if(status != 0) {
      printf("Жаль, функция pthread_create вернула код ошибки %d\n",status);
      exit(-1);
    }
  }
}

void *print_hello_world(void *tid) {
  /* Эта функция выводит идентификатор потока, а затем осуществляет выход */
  printf("Привет, мир. Тебя приветствует поток № %d\n", *((int*)tid));
  pthread_exit(NULL);
}