const std = @import("std");

pub fn main() !void {
    // Initialize an allocator
    // Can be any one of them, this is the most basic one
    var allocator = std.heap.page_allocator;

    // Initialize arguments
    // Then deinitialize at the end of scope
    var argsIterator = try std.process.ArgIterator.initWithAllocator(allocator);
    defer argsIterator.deinit();

    // Skip executable
    _ = argsIterator.next();

    // Handle cases accordingly
    while (argsIterator.next()) |path| {
        std.debug.print("File path: {s}\n", .{path});
    }
}
