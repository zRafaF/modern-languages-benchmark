const std = @import("std");

pub const bubbleSort = @import("bubblesort.zig");
pub const gaussianBlur = @import("gaussianblur.zig");

fn readBinFile(path: []const u8) ![]u8 {
    var file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    const allocator = std.heap.page_allocator;
    const stats = try file.stat();

    var buffer: []u8 = try allocator.alloc(u8, stats.size);
    var bytesRead = try file.read(buffer[0..]);
    return buffer[0..bytesRead];
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

    var path = argsIterator.next() orelse {
        std.debug.print("No path provided\n", .{});
        return;
    };

    var benchType = argsIterator.next() orelse {
        std.debug.print("No benchmark type provided\n", .{});
        return;
    };

    const benchTypeInt = try std.fmt.parseInt(i8, benchType, 10);

    // Reads the .raw file
    var vec = try readBinFile(path);

    switch (benchTypeInt) {
        1 => {
            _ = bubbleSort.sort(vec);
        },
        2 => {
            _ = gaussianBlur.sequential(vec);
        },
        3 => {
            _ = gaussianBlur.parallel(vec);
        },
        else => {
            std.debug.print("Invalid benchmark type\n", .{});
        },
    }
}
