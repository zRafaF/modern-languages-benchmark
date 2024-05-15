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
                // std.debug.print("x: {}, y: {}\n", .{ x, y });
                continue;
            }

            // for (kernel) |elem| {
            //     std.debug.print("elem: {}\n", .{elem});
            // }
            // std.debug.print("i: {}, j: {}, size: {}, elem: {}\n", .{ i, j, kernelSize, index(i, j, kernelSize) });

            // std.debug.print("x: {}, y: {}, kernel {}\n", .{ (x), (y), kernel[index(i, j, kernelSize)] });
            sum += @as(f64, @floatFromInt(arr[index(@intCast(x), @intCast(y), arraySize)])) * kernel[index(i, j, kernelSize)];
        }
    }

    return @as(u8, @intFromFloat(sum));
}

pub fn sequential(vec: []u8) ![]u8 {
    const kernelSize: usize = 19;
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
