import json
import string
from itertools import islice
from collections import defaultdict


class Trainer:

    def __init__(self):
        pass

    def feed(self, text: str):
        pass

    def clear(self):
        pass

    def get_model(self):
        pass

    def get_json_model(self):
        return json.dumps(self.get_model())


class DefaultTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.count = defaultdict(int)
        self.letter_count = 0

    def feed(self, text: str):
        for symbol in text.lower():
            if symbol.isalpha():
                self.count[symbol] += 1
                self.letter_count += 1

    def clear(self):
        self.count.clear()
        self.letter_count = 0

    def get_model(self):
        result = defaultdict(float)
        result['coincidence_index'] = 0

        for letter in string.ascii_lowercase:
            result[letter] = self.count[letter] / self.letter_count
            if self.letter_count > 1:
                result['coincidence_index'] += (self.count[letter] * (self.count[letter] - 1)) / \
                                               (self.letter_count * (self.letter_count - 1))

        return result
