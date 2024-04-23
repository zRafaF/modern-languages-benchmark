const std = @import("std");

pub fn sequential() !void {
    std.debug.print("Sequential\n", .{});
}

pub fn parallel() !void {
    std.debug.print("Parallel\n", .{});
}
