ALPHABET_POWER = 26
BIT_COUNT = 9
CODE_BASIS = pow(2, BIT_COUNT - 1)

ALPHABET_STR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
SYMBOL_STR = ALPHABET_STR + '\n ~!@#$%^&*()_+`\"№;%:?*-=\\/\',.><1234567890'

ALPHABET_LETTER_CODE = {ALPHABET_STR[code]: code for code in range(len(ALPHABET_STR))}
ALPHABET_CODE_LETTER = {code: ALPHABET_STR[code] for code in range(len(ALPHABET_STR))}
CODE_BIN = {SYMBOL_STR[code]: bin(CODE_BASIS + code)[2:] for code in range(len(SYMBOL_STR))}
