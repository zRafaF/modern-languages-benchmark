const std = @import("std");

pub const bubbleSort = @import("bubblesort.zig");
pub const gaussianBlur = @import("gaussianblur.zig");

fn readBinFile(path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    const allocator = std.heap.page_allocator;
    const stats = try file.stat();

    var buffer: []u8 = try allocator.alloc(u8, stats.size);
    var bytesRead = try file.read(buffer[0..]);
    return buffer[0..bytesRead];
}

fn saveBinFile(path: []const u8, data: []u8) !void {
    const file = try std.fs.cwd().createFile(path, .{});
    defer file.close();

    const writer = file.writer();

    // Write the data array to the file
    try writer.writeAll(data);
}

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

    const path = argsIterator.next() orelse {
        std.debug.print("No path provided\n", .{});
        return;
    };

    const benchType = argsIterator.next() orelse {
        std.debug.print("No benchmark type provided\n", .{});
        return;
    };

    const benchTypeInt = try std.fmt.parseInt(i8, benchType, 10);

    // Reads the .raw file
    const vec = try readBinFile(path);

    switch (benchTypeInt) {
        1 => {
            const res = bubbleSort.sort(vec);
            try saveBinFile("zig_result.raw", res);
        },
        2 => {
            const res = gaussianBlur.sequential(vec);
            try saveBinFile("zig_result.raw", res);
        },
        3 => {
            const res = gaussianBlur.parallel(vec);
            try saveBinFile("zig_result.raw", res);
        },
        else => {
            std.debug.print("Invalid benchmark type\n", .{});
        },
    }
}
