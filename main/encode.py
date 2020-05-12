import abc

from main.config import ALPHABET_POWER, CODE_BASIS, SYMBOL_STR, ALPHABET_LETTER_CODE, \
                        ALPHABET_CODE_LETTER, CODE_BIN, BIT_COUNT, CODE_LOWER, CODE_UPPER


class Encoder:

    __metaclass__ = abc.ABCMeta

    def __init__(self, key):
        self.key = key

    @abc.abstractmethod
    def calc(self, symbol: str, position: int, subcomm: str):
        pass

    def encode(self, text: str, subcomm: str):
        result = []
        if subcomm == 'decode' and (isinstance(self.key, int) or self.key.isdigit()):
            self.key = -self.key
        position = 0
        for symbol in text:
            if symbol.isalpha():
                result.append(self.calc(symbol, position, subcomm))
                position += 1
            else:
                result.append(symbol)
        return ''.join(result)


class CaesarEncoderDecoder(Encoder):

    def __init__(self, key):
        key %= ALPHABET_POWER
        super().__init__(key)

    def calc(self, symbol: str, position: int, subcomm):
        code_a = CODE_UPPER if symbol.isupper() else CODE_LOWER
        return ALPHABET_CODE_LETTER[code_a + (ALPHABET_LETTER_CODE[symbol] - code_a + self.key) % ALPHABET_POWER]


class VigenereEncoderDecoder(Encoder):

    def __init__(self, key):
        key = key.lower()
        if not key.isalpha():
            raise KeyError('Key must be single word')
        super().__init__(key)

    def calc(self, symbol: str, position: int, subcomm: str):
        code_a = CODE_UPPER if symbol.isupper() else CODE_LOWER

        ind = ALPHABET_LETTER_CODE[self.key[position % len(self.key)]] - CODE_LOWER
        if subcomm == 'decode':
            ind = -ind

        return ALPHABET_CODE_LETTER[code_a + (ALPHABET_LETTER_CODE[symbol] - code_a + ind) % ALPHABET_POWER]


class VernamEncoder(Encoder):

    def __init__(self, key):
        super().__init__(key)

    def encode(self, text: str, subcomm: str):
        binary_text = []
        for symbol in text:
            if symbol not in SYMBOL_STR:
                raise IndexError(f'Alphabet does not contain symbol: {symbol}, {ord(symbol)}. Impossible to encode')
            binary_text.append(CODE_BIN[symbol])
        return bin(int(''.join(binary_text), 2) ^ self.key)[2:]

    def calc(self, symbol: str, position: int, subcomm: str):
        pass


class VernamDecoder(Encoder):

    def __init__(self, key):
        super().__init__(key)

    def encode(self, text: str, subcomm: str):
        binary_result = bin(self.key ^ int(text, 2))[2:]
        result = []
        for symbol in range(0, len(binary_result), BIT_COUNT):
            index = int(binary_result[symbol:symbol + BIT_COUNT], 2) - CODE_BASIS
            try:
                result.append(SYMBOL_STR[index])
            except IndexError:
                print(f'There is no symbol #{index}')
        return ''.join(result)

    def calc(self, symbol: str, position: int, subcomm: str):
        pass
