int median_of_three(int a, int b, int c) {
  return (b >= a && a >= c) || (c >= a && a >= b) ? a :
         (a >= b && b >= c) || (c >= b && b >= a) ? b : c;
}