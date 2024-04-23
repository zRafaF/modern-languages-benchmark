const std = @import("std");
pub const bubbleSort = @import("bubblesort.zig");
pub const gaussianBlur = @import("gaussianblur.zig");

pub fn main() !void {
    // Initialize an allocator
    // Can be any one of them, this is the most basic one
    const allocator = std.heap.page_allocator;

    // Initialize arguments
    // Then deinitialize at the end of scope
    var argsIterator = try std.process.ArgIterator.initWithAllocator(allocator);
    defer argsIterator.deinit();

    // Skip executable
    _ = argsIterator.next();

    var counter: i8 = 0;
    var path: []const u8 = undefined;
    var benchType: []const u8 = undefined;

    // Handle cases accordingly
    while (argsIterator.next()) |arg| {
        counter += 1;
        switch (counter) {
            // First argument is the path
            1 => path = arg,
            // Second argument is the benchmark type
            2 => benchType = arg,
            // If there are more than 2 arguments, print an error
            else => {
                std.debug.print("Too many arguments\n", .{});
                return;
            },
        }
    }

    const benchTypeInt = try std.fmt.parseInt(i8, benchType, 10);

    switch (benchTypeInt) {
        1 => {
            try bubbleSort.sort();
        },
        2 => {
            try gaussianBlur.sequential();
        },
        3 => {
            try gaussianBlur.parallel();
        },
        else => {
            std.debug.print("Invalid benchmark type\n", .{});
        },
    }
}
