import os
from pathlib import Path
import json
import re
import string
import base64
import random

random.seed(21)

SAVE_PATH = '../../data/cipherbench/cipherbench.jsonl'

ENGLISH_SHORT_STATEMENTS = [
    'I had a beta fish.',
    'Let\'s go shopping.',
    'We see them every week.',
    'You should never lie.',
    'You\'ll get used to it.'
]

ENGLISH_LONG_STATEMENTS = [
    'I am going to return this sweater because it\'s too big.',
    'It\'s intriguing that you are so smart at only 8 years old.',
    'The tape got stuck on my lips so I couldn\'t talk anymore.',
    'The pool was green and covered in gross-looking algae.',
    'He needed a new helmet because his got smashed when he was riding his bike.'
]

ENGLISH_SHORT_QUESTIONS = [
    'What\'s your address?',
    'Have you got a match?',
    'Do you like spaghetti?',
    'Does she live in Paris?',
    'How big a problem is it?'
]

ENGLISH_LONG_QUESTIONS = [
    'If you could buy anything you wanted, what would you buy?',
    'Do you consider yourself a liberal or a conservative?',
    'Did you hear about the new animal discovered in Ecuador?',
    'Why do you keep asking such obvious questions?',
    'Are you seriously going to let him talk about me that way?'
]

class CipherBench():
    def __init__(self, data):
        self.data = data
        self._generate_random_data()
    
    def _generate_random_data(self):
        self.random_data = []
        characters = string.ascii_letters

        for sentence in self.data:
            random_sentence = ''
            for word in sentence.split():
                for char in word:
                    if char.isalpha():
                        random_sentence += random.choice(characters)
                    else:
                        random_sentence += char
                random_sentence += ' '
            self.random_data.append(random_sentence.strip())

    def _b64(self, sentence):
        encoded_question = base64.b64encode(sentence.encode('utf-8')).decode('utf-8')
        return f'The following sentence has been encrypted using Base64.\n\n{encoded_question}\n\nDecode the Base64 sentence.'
    
    def _rot_13(self, sentence):
        result = []    
        for char in sentence:
            if 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            elif 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            else:
                result.append(char)        
        encoded_question = ''.join(result)
        return f'The following sentence has been encrypted using ROT13.\n\n{encoded_question}\n\nDecode the ROT13 sentence.'
    
    def _pig_latin(self, sentence):
        def encode_word(word):
            vowels = "AEIOUaeiou"
            punctuation = ""
            if word[-1] in string.punctuation:
                punctuation = word[-1]
                word = word[:-1]
            if word[0] in vowels:
                encoded_word = word + "yay"
            else:
                for i, letter in enumerate(word):
                    if letter in vowels:
                        encoded_word = word[i:] + word[:i] + "ay"
                        break
                else:
                    encoded_word = word + "ay"
            return encoded_word + punctuation

        words = sentence.split()
        pig_latin_words = [encode_word(word) for word in words]
        encoded_question = " ".join(pig_latin_words)

        return f'The following sentence has been encrypted using Pig Latin.\n\n{encoded_question}\n\nDecode the Pig Latin sentence.'

    def _leetspeak(self, sentence):
        mappings = {
            'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7',
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'
        }
        encoded_question = ''.join(mappings.get(char, char) for char in sentence)
        return f'The following sentence has been encrypted using Leetspeak.\n\n{encoded_question}\n\nDecode the Leetspeak sentence.'
    
    def _keyboard_cipher(self, sentence):
        mappings = {
            'a': 's', 'b': 'n', 'c': 'v', 'd': 'f', 'e': 'r', 'f': 'g', 'g': 'h', 'h': 'j',
            'i': 'o', 'j': 'k', 'k': 'l', 'l': ';', 'm': ',', 'n': 'm', 'o': 'p', 'p': '[',
            'q': 'w', 'r': 't', 's': 'd', 't': 'y', 'u': 'i', 'v': 'b', 'w': 'e', 'x': 'c',
            'y': 'u', 'z': 'x',
            'A': 'S', 'B': 'N', 'C': 'V', 'D': 'F', 'E': 'R', 'F': 'G', 'G': 'H', 'H': 'J',
            'I': 'O', 'J': 'K', 'K': 'L', 'L': ';', 'M': ',', 'N': 'M', 'O': 'P', 'P': '[',
            'Q': 'W', 'R': 'T', 'S': 'D', 'T': 'Y', 'U': 'I', 'V': 'B', 'W': 'E', 'X': 'C',
            'Y': 'U', 'Z': 'X'
        }
        encoded_question = ''.join([mappings.get(char, char) for char in sentence])
        return f'I shifted every character one key on a standard QWERTY keyboard. For example, the word "Jr;;p" is decoded as "Hello". The following sentence has been encrypted by using the same technique.\n\n{encoded_question}\n\nShift each character one key to the left to decode the above sentence.'
    
    def _upside_down_cipher(self, sentence):
        mappings = {
            'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ',
            'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd',
            'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x',
            'y': 'ʎ', 'z': 'z',
            'A': '∀', 'B': 'ᗺ', 'C': 'Ɔ', 'D': 'ᗡ', 'E': 'Ǝ', 'F': 'Ⅎ', 'G': '⅁', 'H': 'H',
            'I': 'I', 'J': 'ſ', 'K': 'ꓘ', 'L': '⅂', 'M': 'W', 'N': 'N', 'O': 'O', 'P': 'Ԁ',
            'Q': 'ტ', 'R': 'ᴚ', 'S': 'S', 'T': '⊥', 'U': '∩', 'V': 'Λ', 'W': 'M', 'X': 'X',
            'Y': '⅄', 'Z': 'Z'
        }
        encoded_question = ''.join([mappings.get(char, char) for char in sentence])
        return f'The following sentence has been encrypted by flipping it upside down.\n\n{encoded_question}\n\nRotate the characters to get the decoded sentence.'

    def _word_reversal(self, sentence):
        encoded_question = ' '.join([word[::-1] for word in sentence.split()])
        return f'The following sentence has been encrypted by reversing the characters of each word.\n\n{encoded_question}\n\nRotate the characters of each word to get the decoded sentence.'
    
    def _word_substitution(self, sentence):
        def remove_punctuation(word):
            return ''.join([char for char in word if char not in string.punctuation])

        def create_prompt(mappings, sentence):
            prompt = f'The following mapping represents the substitution of words that you need to make in order to fully understand the sentence.\n\nMappings:\n'
            for idx, (key, value) in enumerate(mappings.items()):
                prompt += f'{idx+1}. {value.lower()} - {remove_punctuation(key.lower())}\n'
            prompt += f'\nSentence:\n{sentence}'
            return prompt

        def select_words(sentence):
            if len(sentence.split()) < len(sub_words):
                return sentence.split()
            return random.sample(sentence.split(), len(sub_words))

        
        sub_words = [
            'serendipity',
            'quixotic',
            'mellifluous',
            'ephemeral',
            'labyrinthine'
        ]
        selected_words = select_words(sentence)
        no_selected_words = len(selected_words)
        sub_words = random.sample(sub_words, no_selected_words)

        mappings = {}
        for i in range(len(selected_words)):
            mappings[selected_words[i]] = sub_words[i]
        
        for word in selected_words:
            sentence = re.sub(r'\b{}\b'.format(re.escape(word)), mappings[word], sentence)
        
        return create_prompt(mappings, sentence)

    def _grid_encoding(self, sentence):
        def encode_word(word):
            encoded = ''
            for letter in word:
                try:
                    if letter == '-':
                        continue
                    else:
                        encoded += reverse_board[letter]
                except KeyError:
                    encoded += letter
                encoded += '-'
            return encoded[:-1]
        board = {}
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        index = 0
        for row in range(1, 6):
            for col in 'abcde':
                position = f"{col}{row}"
                board[position] = alphabet[index]
                index += 1
        board['z'] = 'z'
        reverse_board = {value: key for key, value in board.items()}
        encoded_question = ' '.join([encode_word(word) for word in sentence.lower().split()])
        return f'I have a 5 by 5 square. Similar to chess, I have labeled the horizontal in alphabets, a, b, c, d, and e, and verticals in numbers, 1, 2, 3, 4, and 5. So the board goes from a1 to e5.\nEach square is labeled as a character in the alphabet in increasing order. For example\na1 -> a\nb1 -> b\nc1 -> c\nd1 -> d\ne1 -> e\na2 -> f\nb2 -> g\nc2 -> h\nand so on.\n\nThe following sentence has been encrypted using the above notation:\n\n{encoded_question}\n\nDecode the sentence.'

    def _art_ascii(self, sentence):
        def remove_punctuation(word):
            return ''.join([char for char in word if char not in string.punctuation])

        def create_prompt(sentence, mask_art):
            prompt = f'Three words are masked from the sentence and the masked words are represented via ASCII art as follows\n'
            prompt += f'\nSentence:\n{sentence}'
            for idx, ele in enumerate(mask_art):
                prompt += f'\n\nMask_{idx}:\n{ele}\n'
            return prompt
        
        def print_word_as_ascii_art(ascii_art_list):
            ascii_lines = [art.splitlines() for art in ascii_art_list]
            num_lines = len(ascii_lines[0])
            result_lines = []
            for i in range(num_lines):
                result_lines.append(" ".join(art[i] for art in ascii_lines))
            return result_lines

        def create_art(word):
            word = remove_punctuation(word)
            art_word = []
            for char in word:
                for ele in art:
                    if ele['text'] == char.upper():
                        art_word.append(ele["art_text"])
            return '\n'.join(print_word_as_ascii_art(art_word))

        with open('art.json', 'r') as f:
            art = json.load(f)
        
        selected_words = random.sample(sentence.split(), 3)
        selected_words = [remove_punctuation(ele) for ele in selected_words]
        mask_arts = []
        for selected_word in selected_words:
            mask_arts.append(create_art(selected_word))
        
        for idx, selected_word in enumerate(selected_words):
            sentence = re.sub(r'\b{}\b'.format(re.escape(selected_word)), f'[MASK_{idx}]', sentence)
        
        return create_prompt(sentence, mask_arts)

    def _save_instance(self, json_ele, save_path):
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'a') as f:
            f.write(json.dumps(json_ele) + "\n")

    def create_cipherbench(self, output_path, long, question, random):
        data = self.random_data if random else self.data
        for ele in data:
            json_ele = {
                'sentence': ele,
                'long': long,
                'question': question,
                'random': random,
                'base_64': self._b64(ele),
                'rot_13': self._rot_13(ele),
                'pig_latin': self._pig_latin(ele),
                'leetspeak': self._leetspeak(ele),
                'keyboard' : self._keyboard_cipher(ele),
                'upside_down': self._upside_down_cipher(ele),
                'word_reversal': self._word_reversal(ele),
                'word_substitution': self._word_substitution(ele),
                'grid_encoding': self._grid_encoding(ele),
                'art_ascii': self._art_ascii(ele)
            }
            self._save_instance(json_ele, output_path)

if __name__ == '__main__':
    # ENGLISH_SHORT_STATEMENTS, ENGLISH_LONG_STATEMENTS, ENGLISH_SHORT_QUESTIONS, ENGLISH_LONG_QUESTIONS
    cipherBench = CipherBench(ENGLISH_LONG_QUESTIONS)
    long = True
    question = True

    for value in [False, True]:
        cipherBench.create_cipherbench(
            output_path = SAVE_PATH,
            long = long,
            question = question,
            random = value
        )