const std = @import("std");

pub fn sort(vec: []u8) []u8 {
    while (true) {
        var troca: bool = false;
        for (0..vec.len - 1) |elem| {
            const j: u64 = elem + 1;
            if (vec[elem] > vec[j]) {
                const x: u8 = vec[elem];
                const y: u8 = vec[j];
                vec[elem] = y;
                vec[j] = x;
                troca = true;
            }
        }

        if (!troca) {
            break;
        }
    }

    return vec;
}
