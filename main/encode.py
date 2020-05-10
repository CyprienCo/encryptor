from main.config import ALPHABET_POWER, CODE_BASIS, SYMBOL_STR, ALPHABET_LETTER_CODE, \
                        ALPHABET_CODE_LETTER, CODE_BIN, BIT_COUNT


class Encoder:

    def __init__(self, key):
        self.key = key

    def calc(self, symbol: str, position: int, subcomm: str):
        pass

    def encode(self, text: str, subcomm: str):
        result = []
        if subcomm == 'decode':
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
        code_a = ALPHABET_LETTER_CODE['A'] if symbol.isupper() else ALPHABET_LETTER_CODE['a']
        return ALPHABET_CODE_LETTER[code_a + (ALPHABET_LETTER_CODE[symbol] - code_a + self.key) % ALPHABET_POWER]


class VigenereEncoderDecoder(Encoder):

    def __init__(self, key):
        key = key.lower()
        if not key.isalpha():
            raise KeyError('Key must be single word')
        super().__init__(key)

    def calc(self, symbol: str, position: int, subcomm: str):
        code_a = ALPHABET_LETTER_CODE['A'] if symbol.isupper() else ALPHABET_LETTER_CODE['a']

        ind = ALPHABET_LETTER_CODE[self.key[position % len(self.key)]] - ALPHABET_LETTER_CODE['a']
        if subcomm == 'decode':
            ind = -ind

        return ALPHABET_CODE_LETTER[code_a + (ALPHABET_LETTER_CODE[symbol] - code_a + ind) % ALPHABET_POWER]


class VernamEncoder:

    def __init__(self, key):
        self.key = int(key)

    def encode(self, text):
        binary_text = []
        for symbol in text:
            if symbol not in SYMBOL_STR:
                raise IndexError(f'Alphabet does not contain symbol: {symbol}, {ord(symbol)}. Impossible to encode')
            binary_text.append(CODE_BIN[symbol])
        return bin(int(''.join(binary_text), 2) ^ self.key)[2:]


class VernamDecoder:

    def __init__(self, key):
        self.key = int(key)

    def encode(self, text: str):
        binary_result = bin(self.key ^ int(text, 2))[2:]
        result = []
        for symbol in range(0, len(binary_result), BIT_COUNT):
            index = int(binary_result[symbol:symbol + BIT_COUNT], 2) - CODE_BASIS
            try:
                result.append(SYMBOL_STR[index])
            except IndexError:
                print(f'There is no symbol #{index}')
        return ''.join(result)
