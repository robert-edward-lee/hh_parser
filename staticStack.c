#include <stdint.h>
#include <stdio.h>

#define STACK_MAX_SIZE 20

typedef struct {
  int8_t top;
  int32_t data[STACK_MAX_SIZE];
} static_stack_t;

void push(static_stack_t* staticStackPtr);
void pop(static_stack_t* staticStackPtr);
void peek(static_stack_t* staticStackPtr);
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
      case 'h': {
        push(&MyStack);
        break;
      }
      case 'p': {
        pop(&MyStack);
        break;
      }
      case 'k': {
        peek(&MyStack);
        break;
      }
      case 't': {
        printStack(&MyStack);
        break;
      }
      case 'l': {
        printHelp();
        break;
      }
      case 'q': {
        break;
      }
      default: {
        printf("\nAre you polish?");
        break;
      }
    }
  } while (keyChar != 'q');
  printf("\nGoodnight, sweet prince.\n");
  return 0;
}

void push(static_stack_t* staticStackPtr) {
  int32_t data;
  if(staticStackPtr->top + 1 == STACK_MAX_SIZE) {
    printf("\nStack is full");
  } else {
    printf("\nPut data for push: ");
    scanf("%d", &data);
    staticStackPtr->top++;
    staticStackPtr->data[staticStackPtr->top] = data;
    printStack(staticStackPtr);
  }
  return;
}

void pop(static_stack_t* staticStackPtr) {
  if(staticStackPtr->top < 0) {
    printf("\nStack is empty");
  } else {
    staticStackPtr->data[staticStackPtr->top] = 0;
    staticStackPtr->top--;
    printStack(staticStackPtr);
  }
  return;
}

void peek(static_stack_t* staticStackPtr) {
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