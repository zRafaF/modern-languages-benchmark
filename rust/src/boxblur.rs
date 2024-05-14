fn index(x: usize, y: usize, side_size: usize) -> usize {
    x * side_size + y
}

fn index_to_2d(idx: usize, side_size: usize) -> (usize, usize) {
    (idx / side_size, idx % side_size)
}

fn generate_box_blur_kernel(size: usize) -> Vec<f64> {
    let mut kernel = vec![0.0; size * size];
    let size_f64 = size as f64;
    for i in 0..size {
        for j in 0..size {
            kernel[index(i, j, size)] = 1.0 / (size_f64 * size_f64);
        }
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

    let mut handles = vec![];

    for element_idx in 0..num_elements {
        let arr = arr.clone();
        let kernel = kernel.clone();
        let handle = std::thread::spawn(move || {
            let val = apply_convolution(arr, array_size, element_idx, kernel, KERNEL_SIZE);
            val
        });
        handles.push(handle);
    }

    let result: Vec<u8> = handles
        .into_iter()
        .map(|handle| handle.join().unwrap())
        .collect();
    arr
}
