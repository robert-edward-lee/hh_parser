#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
#if BYTE_ORDER == BIG_ENDIAN
  uint8_t first_byte;
  uint8_t second_byte;
  uint8_t third_byte;
  uint8_t fourth_byte;
#endif
#if BYTE_ORDER == LITTLE_ENDIAN
  uint8_t fourth_byte;
  uint8_t third_byte;
  uint8_t second_byte;
  uint8_t first_byte;
#endif
} IPv4_struct_t;

typedef union {
  uint32_t ipv4_dec;
  IPv4_struct_t ipv4_struct_p;
} IPv4_union_t;

void uint32_to_ip(uint32_t ip, char *str);

int main(void) {
  uint64_t ip;
  char str[16] = {0};

  printf("\nmain: begin");
  do {
    printf("\nPut integer number to convert into IPv4 or some shit to quit: ");
    if(scanf("%ld", &ip) != 1) {
      break;
    }
    if(ip > UINT32_MAX) {
      printf("\nToo large number! Try again");
      continue;
    }
    uint32_to_ip((uint64_t)ip, str);
    printf("\n%s", str);
  } while(1);
  printf("\nmain: end\n");

  return 0;
}

void uint32_to_ip(uint32_t ip, char *output) {
  printf("\nuint32_to_ip: begin");
  IPv4_union_t ipU;
  ipU.ipv4_dec = ip;
  sprintf(output, "%u.%u.%u.%u", ipU.ipv4_struct_p.first_byte, ipU.ipv4_struct_p.second_byte,
                                 ipU.ipv4_struct_p.third_byte, ipU.ipv4_struct_p.fourth_byte);
  printf("\nuint32_to_ip: end");
}