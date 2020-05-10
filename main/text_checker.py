from main.config import ALPHABET_LETTER_CODE


class TextChecker:

    @staticmethod
    def check(text: str):
        for letter in text:
            if letter.isalpha() and ALPHABET_LETTER_CODE[letter] > ALPHABET_LETTER_CODE['z']:
                raise Exception('Text cannot contain non-english alphabet letters')