const std = @import("std");

pub fn sequential(vec: []u8) []u8 {
    std.debug.print("Sequential Gaussian blur on vec of size: {}\n", .{vec.len});
    return vec;
}

pub fn parallel(vec: []u8) []u8 {
    std.debug.print("Parallel Gaussian blur on vec of size: {}\n", .{vec.len});
    return vec;
}
