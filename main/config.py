import string
import math

ALPHABET_STR = string.ascii_letters
SYMBOL_STR = ALPHABET_STR + string.punctuation + string.digits

ALPHABET_POWER = int(len(ALPHABET_STR) / 2)
BIT_COUNT = math.frexp(len(SYMBOL_STR) * 2)[1]
CODE_BASIS = pow(2, BIT_COUNT - 1)

ALPHABET_LETTER_CODE = {ALPHABET_STR[code]: code for code in range(len(ALPHABET_STR))}
ALPHABET_CODE_LETTER = {code: ALPHABET_STR[code] for code in range(len(ALPHABET_STR))}
CODE_BIN = {SYMBOL_STR[code]: bin(CODE_BASIS + code)[2:] for code in range(len(SYMBOL_STR))}

CODE_LOWER = ALPHABET_LETTER_CODE[string.ascii_lowercase[0]]
CODE_UPPER = ALPHABET_LETTER_CODE[string.ascii_uppercase[0]]


if __name__ == '__main__':
    print(int(CODE_BIN['\n']))
