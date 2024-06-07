import numpy as np
from scipy.signal import convolve2d
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


def generate_box_blur_kernel(size):
    num_of_elements = size * size
    return np.full((size, size), 1.0 / num_of_elements)


def apply_convolution(arr, kernel):
    # Use 'same' mode to keep the output size the same as the input size
    convolved = convolve2d(arr, kernel, mode="same", boundary="fill", fillvalue=0)
    return np.clip(convolved, 0, 255).astype(np.uint8)


def sequential(arr):
    kernel_size = 19
    array_size = int(np.sqrt(arr.size))
    kernel = generate_box_blur_kernel(kernel_size)

    arr = arr.reshape((array_size, array_size))
    result = apply_convolution(arr, kernel)

    return result.flatten()


def process_chunk(chunk, kernel):
    return apply_convolution(chunk, kernel)


def parallel(arr):
    kernel_size = 19
    array_size = int(np.sqrt(arr.size))
    kernel = generate_box_blur_kernel(kernel_size)

    arr = arr.reshape((array_size, array_size))

    num_chunks = multiprocessing.cpu_count()
    chunk_size = array_size // num_chunks
    chunks = [arr[i * chunk_size : (i + 1) * chunk_size, :] for i in range(num_chunks)]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks, [kernel] * num_chunks))

    result = np.vstack(results)

    return result.flatten()
