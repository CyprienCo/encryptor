import argparse
import json
import sys
import abc
import string
import copy



ALPHABET_POWER = 26
ASCII_BIT_COUNT = 7


class Encoder:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, key):
        self.key = key

    @abc.abstractmethod
    def calc(self, symbol: str, position: int):
        pass

    def encode(self, text: str):
        result = []
        position = 0
        for symbol in text:
            if symbol.isalpha():
                result.append(self.calc(symbol, position))
                position += 1
            else:
                result.append(symbol)
        return ''.join(result)


class CaesarEncoder(Encoder):

    def __init__(self, key):
        key = int(key) % ALPHABET_POWER
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a + self.key) % ALPHABET_POWER)


class VigenereEncoder(Encoder):

    def __init__(self, key):
        key = key.lower()
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(
            code_a + (ord(symbol) + ord(self.key[position % len(self.key)]) - code_a - ord('a')) % ALPHABET_POWER)


class CaesarDecoder(Encoder):

    def __init__(self, key):
        key = int(key) % ALPHABET_POWER
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a + ALPHABET_POWER - self.key) % ALPHABET_POWER)


class VigenereDecoder(Encoder):

    def __init__(self, key):
        key = key.lower()
        if not key.isalpha():
            raise Exception('Key must be single word')
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a - ord(self.key[position % len(self.key)]) + ord(
            'a') + ALPHABET_POWER) % ALPHABET_POWER)


class VernamEncoder:

    def __init__(self, key):
        self.key = int(key)

    def encode(self, text):
        binary_text = []
        for symbol in text:
            binary_text.append(bin(ord(symbol))[2:])
        return bin(int(''.join(binary_text), 2) ^ self.key)[2:]


class VernamDecoder:

    def __init__(self, key):
        self.key = int(key)

    def encode(self, text: str):
        binary_result = bin(self.key ^ int(text, 2))[2:]
        result = []
        for symbol in range(0, len(binary_result), ASCII_BIT_COUNT):
            result.append(chr(int(binary_result[symbol:symbol + ASCII_BIT_COUNT], 2)))
        return ''.join(result)

class Trainer:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def feed(self, text: str):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def get_model(self):
        pass

    def get_json_model(self):
        return json.dumps(self.get_model())


class DefaultTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.count = {}
        self.letter_count = 0

    def feed(self, text: str):
        for symbol in text.lower():
            if symbol.isalpha():
                self.count[symbol] = self.count.get(symbol, 0) + 1
                self.letter_count += 1

    def clear(self):
        self.count.clear()
        self.letter_count = 0

    def get_model(self):
        result = {'coincidence_index': 0}

        for letter in string.ascii_lowercase:
            result[letter] = self.count.get(letter, 0) / self.letter_count
            if self.letter_count > 1:
                result['coincidence_index'] += (self.count.get(letter, 0) * (self.count.get(letter, 0) - 1)) / \
                                     (self.letter_count * (self.letter_count - 1))

        return result


class BonusTrainer(Trainer):

    def __init__(self, n):
        super().__init__()
        self.count = {}
        self.n = n

    def feed(self, text: str):
        text = text.lower()
        for index in range(0, len(text) - self.n + 1):
            current_slice = text[index:index + self.n]
            if current_slice.isalpha():
                self.count[current_slice] = self.count.get(current_slice, 0) + 1

    def clear(self):
        self.count = {}

    def get_model(self):
        return self.count


class TextChecker:

    @staticmethod
    def check(text: str):
        for letter in text:
            if letter.isalpha() and ord(letter) > 122:
                raise Exception('Text cannot contain non-english alphabet letters')


class Hacker:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, model):
        self.model = model

    @abc.abstractmethod
    def hack(self, text: str):
        pass


class CaesarHacker(Hacker):

    def __init__(self, model):
        super().__init__(model)
        self.caesar_decoders = [CaesarDecoder(shift) for shift in range(ALPHABET_POWER)]
        self.trainer = DefaultTrainer()

    def hack(self, text: str):
        results = [0 for shift in range(ALPHABET_POWER)]
        shift_result = 0

        self.trainer.feed(text)
        current_model = self.trainer.get_model()

        for shift in range(ALPHABET_POWER):
            for letter in string.ascii_lowercase:
                results[shift] += (self.model.get(letter, 0) - current_model.get(letter, 0)) ** 2

            if results[shift] < results[shift_result]:
                shift_result = shift

            next_model = deepcopy(current_model)
            for letter_id in range(ALPHABET_POWER):
                next_model[string.ascii_lowercase[letter_id]] = current_model[
                    string.ascii_lowercase[(letter_id + 1) % ALPHABET_POWER]]

            current_model = next_model

        self.trainer.clear()

        return self.caesar_decoders[shift_result].encode(text)


class CaesarBonusHacker(Hacker):

    def __init__(self, model, n):
        super().__init__(model)
        self.n = n
        self.caesar_decoders = [CaesarDecoder(shift) for shift in range(ALPHABET_POWER)]

    def hack(self, text: str):
        results = [0 for shift in range(ALPHABET_POWER)]
        shift_result = 0

        for shift in range(ALPHABET_POWER):
            current_text = self.caesar_decoders[shift].encode(text).lower()

            for index in range(0, len(current_text) - self.n + 1):
                current_slice = current_text[index:index + self.n]
                if current_slice.isalpha():
                    results[shift] += self.model.get(current_slice, 0)

            if results[shift] > results[shift_result]:
                shift_result = shift

        return self.caesar_decoders[shift_result].encode(text)


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
                count[ord(letter.lower()) - ord('a')] += 1
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

        key_len = 1
        for length, coincidence_index in enumerate(len_ic):
            if self.coincidence_index < coincidence_index:
                key_len = length + 1
                break
            if abs(coincidence_index - self.coincidence_index) < abs(len_ic[key_len - 1] - self.coincidence_index):
                key_len = length + 1

        strings = ['' for index in range(key_len)]
        for position, symbol in enumerate(letter_text):
            strings[position % key_len] += symbol

        caesar_hacker = CaesarHacker(self.model)

        for index in range(key_len):
            strings[index] = caesar_hacker.hack(strings[index])

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

        return ''.join(result)


def encode(args):
    if args.cipher == 'vernam':
        encoder = VernamEncoder(args.key)
    else:
        encoder = CaesarEncoder(args.key) if args.cipher == 'caesar' else VigenereEncoder(args.key)
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(encoder.encode(text))
    else:
        sys.stdout.write(encoder.encode(text))


def decode(args):
    if args.cipher == 'vernam':
        decoder = VernamDecoder(args.key)
    else:
        decoder = CaesarDecoder(args.key) if args.cipher == 'caesar' else VigenereDecoder(args.key)
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(decoder.encode(text))
    else:
        sys.stdout.write(decoder.encode(text))


def train(args):
    trainer = BonusTrainer(args.n) if args.bonus_mode else DefaultTrainer()
    text = args.text_file.read() if args.text_file else sys.stdin.read()
    TextChecker.check(text)
    trainer.feed(text)
    args.model_file.write(trainer.get_json_model())


def hack(args):
    try:
        model = json.load(args.model_file)
    except json.JSONDecodeError:
        raise Exception('Incorrect model file')
    if args.bonus_mode:
        if args.cipher == 'vigenere':
            raise NotImplementedError('Current version does not support bonus hack for vigenere cipher')
        else:
            hacker = CaesarBonusHacker(model, args.n)
    else:
        hacker = CaesarHacker(model) if args.cipher == 'caesar' else VigenereHacker(model)
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(hacker.hack(text))
    else:
        sys.stdout.write(hacker.hack(text))


def parse_args():
    parser = argparse.ArgumentParser(description='Allows you to work with caesar/vigenere/vernam ciphers.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    # encode
    parser_encode = subparsers.add_parser('encode', help='Encode help')
    parser_encode.set_defaults(mode='encode', func=encode)
    parser_encode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type', required=True)
    parser_encode.add_argument('--key', help='Cipher key', required=True)
    parser_encode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_encode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # decode
    parser_decode = subparsers.add_parser('decode', help='Decode help')
    parser_decode.set_defaults(mode='decode', func=decode)
    parser_decode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type', required=True)
    parser_decode.add_argument('--key', help='Cipher key', required=True)
    parser_decode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_decode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # train
    parser_train = subparsers.add_parser('train', help='Train help')
    parser_train.set_defaults(mode='train', func=train)
    parser_train.add_argument('--text-file', type=argparse.FileType('r'), help='Input file')
    parser_train.add_argument('--model-file', type=argparse.FileType('w'), help='Model file', required=True)
    parser_train.add_argument('--bonus', dest='bonus_mode', action='store_true')
    parser_train.add_argument('--n', type=int, help='Size of a n-chart model')

    # hack
    parser_hack = subparsers.add_parser('hack', help='Hack help')
    parser_hack.set_defaults(mode='hack', func=hack)
    parser_hack.add_argument('--cipher', choices=['caesar', 'vigenere'], help='Cipher type', required=True)
    parser_hack.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_hack.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')
    parser_hack.add_argument('--model-file', type=argparse.FileType('r'), help='Model file', required=True)
    parser_hack.add_argument('--bonus', dest='bonus_mode', action='store_true')
    parser_hack.add_argument('--n', type=int, help='Size of a n-chart model')

    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    arguments.func(arguments)
