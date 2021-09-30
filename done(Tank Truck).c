#include <math.h>
#include <stdio.h>

int main(void) {
  int height;
  int diameter;
  int total_volume;
  printf("\nPut your data: height, diameter and total volume:\n");
  scanf("%d %d %d", &height, &diameter, &total_volume);

  double V, area_triangle, area_segment;
  double alpha;
  double radius = (double)diameter / 2;
  double total_length = (double)total_volume / (M_PI * radius * radius);
  printf("\nRadius = %.4lf", radius);
  if((height - radius) < 0) {
    alpha = acos((radius - height) / radius);
    area_segment = alpha * radius * radius;
    area_triangle = radius * (radius - height) * sin(alpha);
    V = (area_segment - area_triangle) * total_length;
  } else {
    height = diameter - height;
    printf("\nheight = %d", height);
    alpha = acos((radius - height) / radius);
    area_segment = alpha * radius * radius;
    area_triangle = radius * (radius - height) * sin(alpha);
    V = total_volume - (area_segment - area_triangle) * total_length;
  }
  printf("\nalpha = %.4lf", (alpha * 180) / M_PI);
  printf("\narea_segment = %.4lf", area_segment);
  printf("\narea_triangle = %.4lf", area_triangle);
  printf("\ntotal_length = %.4lf", total_length);
  printf("\nV = %d\n", (int)V);
  return 0;
}