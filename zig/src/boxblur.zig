const std = @import("std");

fn index(x: usize, y: usize, sideSize: usize) usize {
    return x * sideSize + y;
}

fn indexTo2d(idx: usize, sideSize: usize) [2]usize {
    return .{ idx / sideSize, idx % sideSize };
}

fn generateBoxBlurKernel(size: usize) []f64 {
    const allocator = std.heap.page_allocator;

    var kernel: []f64 = try allocator.alloc(f64, size * size);
    defer allocator.free(kernel);

    for (kernel, 0..size) |_, i| {
        for (kernel, 0..size) |_, j| {
            kernel[index(i, j, size)] = @as(f64, 1.0 / (size * size));
        }
    }

    return kernel;
}

fn applyConvolution(arr: []u8, arraySize: usize, elementIds: usize, kernel: []f64, kernelSize: usize) u8 {
    var sum: f64 = 0.0;

    for (kernel, 0..kernelSize) |_, i| {
        for (kernel, 0..kernelSize) |_, j| {
            const ret2d = indexTo2d(elementIds, arraySize);
            var x = ret2d[0] + (i - kernelSize / 2);
            var y = ret2d[1] + (j - kernelSize / 2);

            if ((x < 0) || (y < 0) || (x >= arraySize) || (y >= arraySize)) {
                continue;
            }

            sum += @as(f64, arr[index(x, y, arraySize)]) * kernel[index(i, j, kernelSize)];
        }
    }

    return @as(u8, sum);
}

pub fn sequential(vec: []u8) []u8 {
    const kernelSize: usize = 19;
    const arraySize = @as(usize, @intFromFloat(std.math.sqrt(@as(f64, @floatFromInt(vec.len)))));

    const kernel = generateBoxBlurKernel(kernelSize);

    for (vec, 0..vec.len) |_, i| {
        vec[i] = applyConvolution(vec, arraySize, i, kernel, kernelSize);
    }

    return vec;
}

pub fn parallel(vec: []u8) []u8 {
    return vec;
}
