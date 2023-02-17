const std = @import("std");
const dbg_print = std.debug.print;
// const ArrayList = std.ArrayList;
// const AutoHashMap = std.AutoHashMap;
const StringHashMap = std.StringHashMap;

// 40,000 lines of Shakespeare from a variety of Shakespeare's plays.
// Source: https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt
// Edited by Julian Delsi
// Speakers are now one word, prefixed by a '%', for easy parsing
const input_file = @embedFile("input.txt");

// THE PLAN
// Parse shakespeare's plays/sonnets/quotes and generate a Markov Chain of words.
// Then use that to generate new random plays/sonnets/quotes.

fn parse_words(allocator: std.mem.Allocator) StringHashMap(StringHashMap(f32)) {
    var result = StringHashMap(StringHashMap(f32)).init(allocator);

    var text = std.mem.tokenize(u8, input_file, " \n");

    var i: usize = 0;
    while (text.next()) |curr_word| : (i += 1) {
        if (curr_word[0] == '%') continue;
        if (i > 100) break;

        dbg_print("|{s}|", .{curr_word});

        if (curr_word[curr_word.len - 1] == '.' or curr_word[curr_word.len - 1] == '?' or curr_word[curr_word.len - 1] == '!') {
            dbg_print("\n", .{});
        }

        var curr_gop = try result.getOrPut(curr_word);
        if (!curr_gop.found_existing) {
            curr_gop.value_ptr.* = StringHashMap(f32).init(allocator);
        }

        if (text.peek()) |next_word| {
            var next_gop = curr_gop.value_ptr.getOrPut(next_word);

            if (!next_gop.found_existing) {
                next_gop.value_ptr.* = 1;
            } else {
                next_gop.value_ptr.* += 1;
            }
        }
    }

    return result;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const words = parse_words(allocator);
}

pub fn print(comptime format: []const u8, args: anytype) !void {
    const stdout_file = std.io.getStdOut().writer();
    var bw = std.io.bufferedWriter(stdout_file);
    const stdout = bw.writer();

    try stdout.print(format, args);

    try bw.flush(); // don't forget to flush!
}
