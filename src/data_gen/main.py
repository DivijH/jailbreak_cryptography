from encode_prompts import EncodeDataset

from b64 import Base_64
from rot13 import ROT13
from upside_down import UpsideDown
from keyboard import KeyboardCipher # type: ignore
from word_reversal import WordReversal
from grid import GridEncoding
from word_substitution import WordSubstitution


# Dataset should contain keys: ['question', 'category', 'priming_sentence']
DATASET_PATH = '../../data/advbench.jsonl'
SAVE_DIR = '../../data/encrypted_variants'

if __name__ == '__main__':
    for class_instance in EncodeDataset.__subclasses__():
        class_instance(DATASET_PATH, SAVE_DIR).encode_dataset()