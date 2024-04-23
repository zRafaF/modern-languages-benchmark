const std = @import("std");

pub fn sort(vec: []u8) []u8 {
    std.debug.print("Bubble Sort on vec of size: {}\n", .{vec.len});
    return vec;
}
