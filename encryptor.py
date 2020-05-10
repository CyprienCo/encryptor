import argparse
import json
import sys

from main.encode import CaesarEncoderDecoder, VigenereEncoderDecoder, VernamEncoder, VernamDecoder
from main.hack import CaesarHacker, VigenereHacker
from main.text_checker import TextChecker
from main.train import DefaultTrainer, BonusTrainer


def print_res(args, func):
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(func(text))
    else:
        sys.stdout.write(func(text))


def encode_decode(args):
    if args.cipher == 'vernam':
        class_k = VernamEncoder(args.key)
    elif args.cipher == 'caesar':
        class_k = CaesarEncoderDecoder(int(args.key))
    else:
        class_k = VigenereEncoderDecoder(args.key)
    print_res(args, class_k.encode)


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

    hacker = CaesarHacker(model) if args.cipher == 'caesar' else VigenereHacker(model)
    print_res(args, hacker.hack)


def parse_args():
    parser = argparse.ArgumentParser(description='Allows you to work with caesar/vigenere/vernam ciphers.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    # encode
    parser_encode = subparsers.add_parser('encode', help='Encode help')
    parser_encode.set_defaults(mode='encode', func=encode_decode, subcomm='encode')
    parser_encode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type', required=True)
    parser_encode.add_argument('--key', help='Cipher key', required=True)
    parser_encode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_encode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # decode
    parser_decode = subparsers.add_parser('decode', help='Decode help')
    parser_decode.set_defaults(mode='decode', func=encode_decode, subcomm='decode')
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

