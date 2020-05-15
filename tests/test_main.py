import random
import string

import pytest

from main.encode import CaesarEncoderDecoder, VigenereEncoderDecoder, VernamEncoder, VernamDecoder
from main.hack import VigenereHacker, CaesarHacker
from main.train import DefaultTrainer


def get_random_string(text_length):
    return ''.join([random.choice(string.ascii_letters) for _ in range(text_length)])


class TestEncodeDecode:

    @pytest.mark.parametrize("text_length, key", [
        (1, 2),
        (1000, 26),
        (10000, 31),
        (100000, 11)
    ])
    def test_caesar_encoder_decoder(self, text_length, key):
        text = get_random_string(text_length)
        caesar_encoder = CaesarEncoderDecoder(key)
        encrypted_text = caesar_encoder.encode(text, 'encode')
        caesar_decoder = CaesarEncoderDecoder(key)
        assert caesar_decoder.encode(encrypted_text, 'decode') == text

    @pytest.mark.parametrize("text_length, key_length", [
        (1, 3),
        (1000, 5),
        (10000, 300),
        (100000, 7),
        (100000, 30)
    ])
    def test_vigenere_encoder_decoder(self, text_length, key_length):
        text = get_random_string(text_length)
        key = get_random_string(key_length)
        vigenere_encoder = VigenereEncoderDecoder(key)
        encrypted_text = vigenere_encoder.encode(text, 'encode')
        vigenere_decoder = VigenereEncoderDecoder(key)
        assert vigenere_decoder.encode(encrypted_text, 'decode') == text

    @pytest.mark.parametrize("text_length, key", [
        (1, 2),
        (1000, 26),
        (10000, 31),
        (100000, 11)
    ])
    def test_vernam_encoder_decoder(self, text_length, key):
        text = get_random_string(text_length)
        vernam_encoder = VernamEncoder(key)
        encrypted_text = vernam_encoder.encode(text, 'encode')
        vername_decoder = VernamDecoder(key)
        assert vername_decoder.encode(encrypted_text, 'decode') == text


class TestTrainerHacker:

    @pytest.mark.parametrize("train_filename, text_filename, key", [
        ('tests/src/1.txt', 'tests/src/2.txt', 5),
        ('tests/src/3.txt', 'tests/src/4.txt', 7),
        ('tests/src/2.txt', 'tests/src/3.txt', 11),
        ('tests/src/4.txt', 'tests/src/2.txt', 13)
    ])
    def test_main_caesar_hacker(self, train_filename, text_filename, key):
        train_file = open(train_filename, 'r')
        text_file = open(text_filename, 'r')

        trainer = DefaultTrainer()
        trainer.feed(train_file.read())
        model = trainer.get_model()

        text = text_file.read()

        caesar_encoder = CaesarEncoderDecoder(key)
        encrypted_text = caesar_encoder.encode(text, 'encode')

        hacker = CaesarHacker(model)
        assert hacker.hack(encrypted_text) == text

    @pytest.mark.parametrize("train_filename, text_filename, key_length", [
        ('tests/src/1.txt', 'tests/src/2.txt', 2),
        ('tests/src/3.txt', 'tests/src/4.txt', 97),
        ('tests/src/2.txt', 'tests/src/3.txt', 31),
        ('tests/src/4.txt', 'tests/src/2.txt', 14)
    ])
    def test_vigenere_hacker(self, train_filename, text_filename, key_length):
        train_file = open(train_filename, 'r')
        text_file = open(text_filename, 'r')

        trainer = DefaultTrainer()
        trainer.feed(train_file.read())
        model = trainer.get_model()

        text = text_file.read()

        key = get_random_string(key_length)
        vigenere_encoder = VigenereEncoderDecoder(key)
        encrypted_text = vigenere_encoder.encode(text, 'encode')

        hacker = VigenereHacker(model)
        assert hacker.hack(encrypted_text) == text
