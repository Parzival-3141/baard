### A Shakespeare quote/sentence generator using Markov Chains

# Todo: seperate word from punctuation. Will decrease duplicate words while keeping sentence structure, and prevent circular chains
# Todo: mark words with ending punctuation ('!', '.', '?', etc.) as 'end words', which can end sentence generation
# Todo: find larger dataset?

import random, sys

# 40,000 lines of Shakespeare from a variety of Shakespeare's plays.
# Source: https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt
# Edited by Julian Delsi
# Speakers are now one word, prefixed by a '%', for easy parsing
with open("input.txt") as file:
	text = file.read().split()

# {word: {next_word: frequency}}
words: dict[str, dict[str, float]] = {}

def fill_transition_tables(words):
	print("Filling word tables...")

	i = 0
	while(i < len(text) - 1):
		# if (i > 100): break

		word = text[i]
		if(word[0] == '%'): 
			i += 1
			continue

		# If key is in the dictionary, return its value. If not, insert key with a value of default and return default
		table = words.setdefault(word, {}) 

		next_word = "%"
		while(next_word[0] == '%' and i < len(text)): 
			i += 1
			next_word = text[i]

		table.setdefault(next_word, 0)
		table[next_word] += 1


def weighted_index(table: dict[str, float]) -> str:
	# inspired by https://ziglang.org/documentation/master/std/src/rand.zig.html#L394
	sum = 0
	for v in table.values():
		sum += v

	point = min(random.random() * sum, sys.float_info.epsilon)
	assert point < sum

	accumulator = 0
	for word, value in table.items():
		accumulator += value
		if(point < accumulator): 
			return word

	return "unreachable!"

def lookup_word(word: str):
	if(word in words):
		print(word, dict(reversed(sorted(words[word].items(), key=lambda item: item[1]))))
		# print(word, dict(sorted(words[word].items())))
	else:
		print(word, "not in words")

if __name__ == "__main__":
	fill_transition_tables(words)
	if(len(sys.argv) > 1):
		for arg in sys.argv[1:]:
			lookup_word(arg)
	else:
		print("Generating sentence...")
		start_word = random.choice(list(words))
		sentence = [start_word]

		for i in range(20):
			sentence.append(weighted_index(words[sentence[i]]))

		print(' '.join(sentence))





