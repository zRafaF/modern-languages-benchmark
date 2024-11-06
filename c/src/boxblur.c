#include "boxblur.h"

#define KERNEL_SIZE 19

size_t index(size_t x, size_t y, size_t side_size)
{
    return x * side_size + y;
}

void generate_box_blur_kernel(double *kernel, size_t size)
{
    double value = 1.0 / (size * size);
    for (size_t i = 0; i < size * size; ++i)
    {
        kernel[i] = value;
    }
}

unsigned char apply_convolution(const unsigned char *arr, size_t array_size, size_t element_idx, const double *kernel, size_t kernel_size)
{
    size_t kernel_half = kernel_size / 2;
    double sum = 0.0;

    size_t x = element_idx / array_size;
    size_t y = element_idx % array_size;

    for (size_t i = 0; i < kernel_size; i++)
    {
        for (size_t j = 0; j < kernel_size; j++)
        {
            size_t xi = x + i - kernel_half;
            size_t yj = y + j - kernel_half;
            if (xi < array_size && yj < array_size)
            {
                sum += arr[index(xi, yj, array_size)] * kernel[index(i, j, kernel_size)];
            }
        }
    }
    return (unsigned char)round(sum);
}

unsigned char *sequential(const unsigned char *arr, size_t arr_size)
{
    size_t array_size = (size_t)sqrt(arr_size);
    unsigned char *result = (unsigned char *)malloc(arr_size);
    if (!result)
    {
        return NULL;
    }

    double kernel[KERNEL_SIZE * KERNEL_SIZE];
    generate_box_blur_kernel(kernel, KERNEL_SIZE);

    for (size_t idx = 0; idx < arr_size; ++idx)
    {
        result[idx] = apply_convolution(arr, array_size, idx, kernel, KERNEL_SIZE);
    }

    return result;
}

unsigned char *parallel(const unsigned char *arr, size_t arr_size)
{
    size_t array_size = (size_t)sqrt(arr_size);
    unsigned char *result = (unsigned char *)malloc(arr_size);
    if (!result)
    {
        return NULL;
    }

    double kernel[KERNEL_SIZE * KERNEL_SIZE];
    generate_box_blur_kernel(kernel, KERNEL_SIZE);

#pragma omp parallel for
    for (size_t idx = 0; idx < arr_size; ++idx)
    {
        result[idx] = apply_convolution(arr, array_size, idx, kernel, KERNEL_SIZE);
    }

    return result;
}
