use std::thread;

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
    arr: Vec<u8>,
    array_size: usize,
    element_idx: usize,
    kernel: Vec<f64>,
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
        .map(|idx| apply_convolution(arr.clone(), array_size, idx, kernel.clone(), KERNEL_SIZE))
        .collect()
}

pub fn parallel(arr: Vec<u8>) -> Vec<u8> {
    const KERNEL_SIZE: usize = 19;
    let array_size = (arr.len() as f64).sqrt() as usize;
    let num_elements = arr.len();

    let kernel = generate_box_blur_kernel(KERNEL_SIZE);

    // Create a vector to hold the handles of the spawned threads
    let mut handles = vec![];

    // Create a vector to store the result
    let result = vec![0u8; num_elements];

    // Use an atomic reference counter to safely share the result vector across threads
    use std::sync::{Arc, Mutex};
    let result = Arc::new(Mutex::new(result));

    for idx in 0..num_elements {
        let arr = arr.clone();
        let kernel = kernel.clone();
        let result = Arc::clone(&result);

        // Spawn a thread for each element
        let handle = thread::spawn(move || {
            let value = apply_convolution(arr, array_size, idx, kernel, KERNEL_SIZE);
            let mut result = result.lock().unwrap();
            result[idx] = value;
        });

        handles.push(handle);
    }

    // Wait for all threads to finish
    for handle in handles {
        handle.join().unwrap();
    }

    // Extract the result from the Arc
    Arc::try_unwrap(result).unwrap().into_inner().unwrap()
}
