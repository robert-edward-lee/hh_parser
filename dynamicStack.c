#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef int32_t data_stack_t;

typedef struct {
  data_stack_t data;
  dynamic_stack_t* next;
} dynamic_stack_t;

void push(dynamic_stack_t** head_stack, data_stack_t value);
data_stack_t pop(dynamic_stack_t** head_stack);
data_stack_t peek(dynamic_stack_t* staticStackPtr);
void printStack(static_stack_t* staticStack);
void printHelp(void);

int main() {
  char keyChar;
  static_stack_t MyStack = {
    .top = -1,
    .data = {0}
  };
  printf("Welcome to my stack! :)");
  printHelp();
  do {
    printf("\nSelect working regime or try 'q' for quit: ");
    while ((keyChar = getchar()) == '\n') {
      continue;
    }
    switch (keyChar)
    {
      case 'h':
        push(&MyStack);
        break;
      case 'p':
        pop(&MyStack);
        break;
      case 'k':
        peek(&MyStack);
        break;
      case 't':
        printStack(&MyStack);
        break;
      case 'l':
        printHelp();
        break;
      case 'q':
        break;
      default:
        printf("\nAre you polish?");
        break;
    }
  } while (keyChar != 'q');
  printf("\nGoodnight, sweet prince.\n");
  return 0;
}

void push(dynamic_stack_t** head_stack, data_stack_t value) {
  dynamic_stack_t* tmp = (dynamic_stack_t*)malloc(sizeof(dynamic_stack_t));
  tmp->data = value;
  tmp->next = *head_stack;
  *head_stack = tmp;
  return;
}

data_stack_t pop(dynamic_stack_t** head_stack) {
  if(head_stack == NULL) {
    /* code */
  }

  dynamic_stack_t* prev = NULL;
  data_stack_t ret;
  prev = *head_stack;
  ret = prev->data;
  *head_stack = (*head_stack)->next;
  free(prev);
  return ret;
}

data_stack_t peek(dynamic_stack_t* staticStackPtr) {
  if(staticStackPtr->top < 0) {
    printf("\nStack is empty");
  } else {
    printf("\nPeeking data: %d", staticStackPtr->data[staticStackPtr->top]);
    printStack(staticStackPtr);
  }
  return;
}

void printStack(static_stack_t* staticStackPtr) {
  int8_t i;
  if(staticStackPtr->top < 0) {
    printf("\nStack is empty");
  } else {
    printf("\nActual size: %d", staticStackPtr->top + 1);
    printf("\nCurrent data: ");
    for (i = 0; i < staticStackPtr->top + 1; i++) {
      printf("%d ", staticStackPtr->data[staticStackPtr->top - i]);
    }
  }
  return;
}

void printHelp(void) {
  printf("\nWhat can i do:\n\t- 'h' for push\n\t- 'p' for pop"
         "\n\t- 'k' for peek \n\t- 't' for just print\n\t- 'l' for help");
  return;
}