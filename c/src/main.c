#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "boxblur.h"

// Load binary file into buffer
unsigned char *load_binary_file(const char *file_path, size_t *size)
{
    FILE *file = fopen(file_path, "rb");
    if (!file)
    {
        fprintf(stderr, "Failed to open file: %s\n", strerror(errno));
        exit(1);
    }

    fseek(file, 0, SEEK_END);
    *size = ftell(file);
    fseek(file, 0, SEEK_SET);

    unsigned char *buffer = (unsigned char *)malloc(*size);
    if (!buffer)
    {
        fprintf(stderr, "Failed to allocate memory\n");
        exit(1);
    }

    if (fread(buffer, 1, *size, file) != *size)
    {
        fprintf(stderr, "Failed to read the file\n");
        exit(1);
    }

    fclose(file);
    return buffer;
}

// Save data to binary file
void save_data_to_bin_file(const unsigned char *data, size_t size, const char *file_name)
{
    FILE *file = fopen(file_name, "wb");
    if (!file)
    {
        fprintf(stderr, "Failed to create file: %s\n", strerror(errno));
        exit(1);
    }

    if (fwrite(data, 1, size, file) != size)
    {
        fprintf(stderr, "Failed to write to file\n");
        exit(1);
    }
    printf("Data saved to %s\n", file_name);

    fclose(file);
}

int main(int argc, char *argv[])
{
    // Check if we received exactly two arguments
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <path_to_bin_file> <number>\n", argv[0]);
        exit(1);
    }

    // Parse command line arguments
    const char *file_path = argv[1];
    int benchmark_type = atoi(argv[2]);
    if (benchmark_type < 1 || benchmark_type > 3)
    {
        fprintf(stderr, "Error: The second argument must be a valid number (1, 2, or 3).\n");
        exit(1);
    }

    // Load binary file content into a buffer
    size_t file_size;
    unsigned char *buffer = load_binary_file(file_path, &file_size);

    unsigned char *result = NULL;

    // Switch between benchmarks
    switch (benchmark_type)
    {
    case 1: // Placeholder for bubble sort, ignored as requested
        break;
    case 2:
        result = sequential(buffer, file_size);
        break;
    case 3:
        result = parallel(buffer, file_size);
        break;
    default:
        fprintf(stderr, "Error: Invalid benchmark type.\n");
        free(buffer);
        exit(1);
    }

    if (result)
    {
        save_data_to_bin_file(result, file_size, "c_result.raw");
        free(result);
    }

    free(buffer);
    return 0;
}
