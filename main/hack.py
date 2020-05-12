import string
from copy import deepcopy
from collections import defaultdict

from main.config import ALPHABET_POWER, ALPHABET_LETTER_CODE
from main.encode import CaesarEncoderDecoder
from main.train import DefaultTrainer


class Hacker:

    def __init__(self, model):
        self.model = defaultdict(float, model)

    def hack(self, text: str):
        pass


class CaesarHacker(Hacker):

    def __init__(self, model):
        super().__init__(model)
        self.caesar_decoders = [CaesarEncoderDecoder(shift) for shift in range(ALPHABET_POWER)]
        self.trainer = DefaultTrainer()

    def hack(self, text: str):
        results = [0 for shift in range(ALPHABET_POWER)]
        shift_result = 0

        self.trainer.feed(text)
        current_model = self.trainer.get_model()
        for shift in range(ALPHABET_POWER):
            for letter in string.ascii_lowercase:
                results[shift] += (self.model[letter] - current_model[letter]) ** 2
            if results[shift] < results[shift_result]:
                shift_result = shift
            next_model = current_model.copy()
            for letter_id in range(ALPHABET_POWER):
                next_model[string.ascii_lowercase[letter_id]] = current_model[
                    string.ascii_lowercase[(letter_id + 1) % ALPHABET_POWER]]

            current_model = next_model.copy()

        self.trainer.clear()

        return self.caesar_decoders[shift_result].encode(text, 'decode')


class VigenereHacker(Hacker):

    def __init__(self, model):
        super().__init__(model)
        try:
            self.coincidence_index = self.model['coincidence_index']
        except KeyError:
            raise KeyError('Wrong model format')

    def calc_coincidence_index(self, text: str):
        count = [0 for letter in range(ALPHABET_POWER)]
        sum_count = 0

        for letter in text:
            if letter.isalpha():
                count[ALPHABET_LETTER_CODE[letter.lower()] - ALPHABET_LETTER_CODE['a']] += 1
                sum_count += 1

        if sum_count <= 2:
            return 0

        result = 0
        for letter in range(ALPHABET_POWER):
            result += (count[letter] * (count[letter] - 1)) / (sum_count * (sum_count - 1))

        return result

    def check_length(self, text: str, length: int):
        current_text = []
        for position in range(0, len(text), length):
            current_text.append(text[position])
        return self.calc_coincidence_index(''.join(current_text))

    def calc_key_len(self, len_ic: list):
        key_len = 1
        for length, coincidence_index in enumerate(len_ic):
            if self.coincidence_index < coincidence_index:
                key_len = length + 1
                break
            if abs(coincidence_index - self.coincidence_index) < abs(len_ic[key_len - 1] - self.coincidence_index):
                key_len = length + 1
        return key_len

    def calc_result(self, text: str, key_len: int, strings: list):
        result = []

        letter_id = 0
        for letter in text:
            if letter.isalpha():
                symbol = strings[letter_id % key_len][letter_id // key_len]
                if letter.isupper():
                    symbol = symbol.upper()
                result.append(symbol)
                letter_id += 1
            else:
                result.append(letter)
        return result

    def hack(self, text: str):
        letters = []
        for letter in text:
            if letter.isalpha():
                letters.append(letter.lower())

        letter_text = ''.join(letters)

        len_ic = []
        current_length = 1
        while current_length * current_length < len(letter_text):
            len_ic.append(self.check_length(letter_text, current_length))
            current_length += 1

        key_len = self.calc_key_len(len_ic)

        strings = ['' for index in range(key_len)]
        for position, symbol in enumerate(letter_text):
            strings[position % key_len] = ''.join((strings[position % key_len],  symbol))

        caesar_hacker = CaesarHacker(self.model)
        for index in range(key_len):
            strings[index] = caesar_hacker.hack(strings[index])

        result = self.calc_result(text, key_len, strings)

        return ''.join(result)
