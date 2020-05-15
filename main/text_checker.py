import string


class TextChecker:

    @staticmethod
    def check(text: str):
        for letter in text:
            if letter not in string.ascii_letters:
                raise Exception('Text cannot contain non-english alphabet letters')
