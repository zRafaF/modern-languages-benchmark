#ifndef BOXBLUR_H
#define BOXBLUR_H

#include <stddef.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

// Function declarations
void generate_box_blur_kernel(double *kernel, size_t size);
unsigned char apply_convolution(const unsigned char *arr, size_t array_size, size_t element_idx, const double *kernel, size_t kernel_size);
unsigned char *sequential(const unsigned char *arr, size_t arr_size);
unsigned char *parallel(const unsigned char *arr, size_t arr_size);

#endif // BOXBLUR_H
