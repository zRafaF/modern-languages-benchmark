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

fn parallelWorkBulk(vecPtr: *const []u8, vec: []u8, arraySize: usize, startIdx: usize, endIdx: usize, kernel: []f64, kernelSize: usize) void {
    for (startIdx..endIdx) |i| {
        vecPtr.*[i] = applyConvolution(vec, arraySize, i, kernel, kernelSize);
    }
}

pub fn parallel(vec: []u8) ![]u8 {
    const kernelSize: usize = 19;
    const arraySize = @as(usize, @intFromFloat(std.math.sqrt(@as(f64, @floatFromInt(vec.len)))));

    var kernel = try generateBoxBlurKernel(kernelSize);

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var pool: std.Thread.Pool = undefined;
    try pool.init(.{ .allocator = allocator });
    defer pool.deinit();

    const cpus = try std.Thread.getCpuCount();
    var outVec = try allocator.alloc(u8, vec.len);
    var vecPtr = &outVec;
    for (0..cpus) |i| {
        const startIdx = (vec.len / cpus) * i;
        const endIdx = ((vec.len / cpus) * (i + 1));

        if (i == cpus - 1) {
            try pool.spawn(parallelWorkBulk, .{ vecPtr, vec, arraySize, startIdx, vec.len, kernel, kernelSize });
            break;
        }

        try pool.spawn(parallelWorkBulk, .{ vecPtr, vec, arraySize, startIdx, endIdx, kernel, kernelSize });
    }

    return outVec;
}
