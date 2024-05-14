const std = @import("std");

fn index(x: usize, y: usize, sideSize: usize) usize {
    return x * sideSize + y;
}

fn indexTo2d(idx: usize, sideSize: usize) [2]usize {
    return .{ idx / sideSize, idx % sideSize };
}

fn generateBoxBlurKernel(size: usize) ![]f64 {
    const allocator = std.heap.page_allocator;
    const numOfElements = size * size;

    var kernel = try allocator.alloc(f64, numOfElements);

    for (kernel, 0..numOfElements) |_, i| {
        kernel[i] = @as(f64, 1.0 / @as(f64, @floatFromInt(numOfElements)));
    }

    return kernel;
}

fn applyConvolution(arr: []u8, arraySize: usize, elementIds: usize, kernel: []f64, kernelSize: usize) u8 {
    var sum: f64 = 0.0;

    for (kernel, 0..kernelSize) |_, i| {
        for (kernel, 0..kernelSize) |_, j| {
            const ret2d = indexTo2d(elementIds, arraySize);
            var x: usize = ret2d[0] + (i - kernelSize / 2);
            var y: usize = ret2d[1] + (j - kernelSize / 2);

            if ((x < 0) or (y < 0) or (x >= arraySize) or (y >= arraySize)) {
                continue;
            }

            sum += @as(f64, @floatFromInt(arr[index(x, y, arraySize)])) * kernel[index(i, j, kernelSize)];
        }
    }

    return @as(u8, @intFromFloat(sum));
}

pub fn sequential(vec: []u8) ![]u8 {
    const kernelSize: usize = 3;
    const arraySize = @as(usize, @intFromFloat(std.math.sqrt(@as(f64, @floatFromInt(vec.len)))));

    std.debug.print("Before\n", .{});
    var kernel = generateBoxBlurKernel(kernelSize) catch {
        return vec;
    };
    std.debug.print("After\n", .{});

    for (vec, 0..vec.len) |_, i| {
        vec[i] = applyConvolution(vec, arraySize, i, kernel, kernelSize);
    }

    return vec;
}

pub fn parallel(vec: []u8) ![]u8 {
    return vec;
}
