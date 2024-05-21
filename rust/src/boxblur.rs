use num_cpus;
use std::sync::Arc;
use threadpool::ThreadPool;

fn index(x: usize, y: usize, side_size: usize) -> usize {
    x * side_size + y
}

fn index_to_2d(idx: usize, side_size: usize) -> (usize, usize) {
    (idx / side_size, idx % side_size)
}

fn generate_box_blur_kernel(size: usize) -> Vec<f64> {
    let num_of_elements = size * size;
    let mut kernel = vec![0.0; num_of_elements];

    for i in 0..num_of_elements {
        kernel[i] = 1.0 / (num_of_elements as f64);
    }

    kernel
}

fn apply_convolution(
    arr: &[u8],
    array_size: usize,
    element_idx: usize,
    kernel: &[f64],
    kernel_size: usize,
) -> u8 {
    let mut sum = 0.0;
    for i in 0..kernel_size {
        for j in 0..kernel_size {
            let (mut x, mut y) = index_to_2d(element_idx, array_size);
            x = x.wrapping_add(i).wrapping_sub(kernel_size / 2);
            y = y.wrapping_add(j).wrapping_sub(kernel_size / 2);
            if x >= array_size || y >= array_size {
                continue;
            }
            sum += f64::from(arr[index(x, y, array_size)]) * kernel[index(i, j, kernel_size)];
        }
    }
    sum.round() as u8
}

pub fn sequential(arr: Vec<u8>) -> Vec<u8> {
    const KERNEL_SIZE: usize = 19;
    let array_size = (arr.len() as f64).sqrt() as usize;

    let kernel = generate_box_blur_kernel(KERNEL_SIZE);

    (0..arr.len())
        .map(|idx| apply_convolution(&arr, array_size, idx, &kernel, KERNEL_SIZE))
        .collect()
}

pub fn parallel(arr: Vec<u8>) -> Vec<u8> {
    const KERNEL_SIZE: usize = 19;
    let array_size = (arr.len() as f64).sqrt() as usize;
    let num_elements = arr.len();

    let kernel = generate_box_blur_kernel(KERNEL_SIZE);

    // Determine the number of available CPUs
    let num_threads = num_cpus::get();
    let pool = ThreadPool::new(num_threads);

    // Shared result vector
    let result = Arc::new(arr.clone()); // Arc is holding the original array

    for idx in 0..num_elements {
        let kernel = kernel.clone();
        let result = Arc::clone(&result);
        pool.execute(move || {
            let value = apply_convolution(&result, array_size, idx, &kernel, KERNEL_SIZE);
            // Unsafe: Directly modify result without synchronization
            unsafe {
                let ptr = result.as_ptr().add(idx) as *mut u8;
                *ptr = value;
            }
        });
    }

    // Wait for all threads to finish
    pool.join();

    // Return the result
    Arc::try_unwrap(result).expect("Failed to unwrap Arc")
}
