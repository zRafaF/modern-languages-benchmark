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

    for (0..numOfElements) |i| {
        kernel[i] = @as(f64, 1.0 / @as(f64, @floatFromInt(numOfElements)));
    }

    return kernel;
}

fn applyConvolution(arr: []u8, arraySize: usize, elementIdx: usize, kernel: []f64, kernelSize: usize) u8 {
    var sum: f64 = 0.0;
    for (0..kernelSize) |i| {
        for (0..kernelSize) |j| {
            const ret2d = indexTo2d(elementIdx, arraySize);
            var x: i32 = @intFromFloat(@as(f32, @floatFromInt(ret2d[0])) + (@as(f32, @floatFromInt(i)) - std.math.floor(@as(f32, @floatFromInt(kernelSize)) / 2.0)));
            var y: i32 = @intFromFloat(@as(f32, @floatFromInt(ret2d[1])) + (@as(f32, @floatFromInt(j)) - std.math.floor(@as(f32, @floatFromInt(kernelSize)) / 2.0)));

            if ((x < 0) or (y < 0) or (x > arraySize) or (y > arraySize)) {
                continue;
            }

            sum += @as(f64, @floatFromInt(arr[index(@intCast(x), @intCast(y), arraySize)])) * kernel[index(i, j, kernelSize)];
        }
    }
    return @as(u8, @intFromFloat(sum));
}

pub fn sequential(vec: []u8) ![]u8 {
    const kernelSize: usize = 19;
    const arraySize = @as(usize, @intFromFloat(std.math.sqrt(@as(f64, @floatFromInt(vec.len)))));

    var kernel = try generateBoxBlurKernel(kernelSize);

    for (0..vec.len) |i| {
        vec[i] = applyConvolution(vec, arraySize, i, kernel, kernelSize);
    }

    return vec;
}

fn parallelWork(vecPtr: *const []u8, vec: []u8, arraySize: usize, elementIdx: usize, kernel: []f64, kernelSize: usize) void {
    vecPtr.*[elementIdx] = applyConvolution(vec, arraySize, elementIdx, kernel, kernelSize);
}

pub fn parallel(vec: []u8) ![]u8 {
    const kernelSize: usize = 19;
    const arraySize = @as(usize, @intFromFloat(std.math.sqrt(@as(f64, @floatFromInt(vec.len)))));

    var kernel = try generateBoxBlurKernel(kernelSize);

    const allocator = std.heap.page_allocator;
    var handles = try allocator.alloc(std.Thread, vec.len);

    var vecPtr = &vec;

    for (0..vec.len) |i| {
        // handles[i] = try std.Thread.spawn(.{}, parallelWork, .{ vecPtr, vecCopy, arraySize, i, kernel, kernelSize });
        handles[i] = try std.Thread.spawn(.{}, parallelWork, .{ vecPtr, vec, arraySize, i, kernel, kernelSize });
    }

    for (handles) |h| {
        h.join();
    }

    return vec;
}
