### A Shakespeare quote/sentence generator using Markov Chains

# Todo: seperate word from punctuation. Will decrease duplicate words while keeping sentence structure, and prevent circular chains
# Todo: mark words with ending punctuation ('!', '.', '?', etc.) as 'end words', which can end sentence generation
# Todo: find larger dataset?

import random, sys

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


fill_transition_tables(words)

# check = "proceed"
# if(check in words):
# 	print(check, dict(reversed(sorted(words[check].items(), key=lambda item: item[1]))))
# 	print("sum", sum([freq for freq in words[check].values()]))
# else:
# 	print(check, "not in words")

print("Generating sentence...")
start_word = random.choice(list(words))
sentence = [start_word]

for i in range(20):
	sentence.append(weighted_index(words[sentence[i]]))

print(' '.join(sentence))

