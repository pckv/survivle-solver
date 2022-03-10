from collections import defaultdict
import random
import string

with open('survivle-words.txt') as f:
    words = [word for word in f.read().splitlines()]

def find_words_in_list(filtered_words, clue, required_letters):
    return [
        word for word in filtered_words 
        if all(letter in clue[i] for i, letter in enumerate(word))
        and all(word.count(letter) == count for letter, count in required_letters.items())
    ]


def find_words(clue, required_letters):
    for i in range(2,6):
        found_words = find_words_in_list(
            [word for word in words if len(set(word)) == i], clue, required_letters)
        if found_words:
            return found_words
    
    return []


def print_words(words):
    print('\t\n'.join(words) + '\n')


def update_clue(clue, required_letters, guess, hint):
    for i, (letter, letter_hint) in enumerate(zip(guess, hint)):
        if letter_hint == 'b':
            if letter in required_letters:
                clue[i].remove(letter)
            else:
                for j in range(len(clue)):
                    if letter in clue[j] and clue[j] != [letter]:
                        clue[j].remove(letter)
        elif letter_hint == 'y':
            if letter in clue[i]:
                clue[i].remove(letter)
            required_letters[letter] += 1
        elif letter_hint == 'g':
            clue[i] = [letter]


def choose_word(words):
    print('Choosing from the following words: ')
    print_words(words)
    
    word = random.choice(words)
    print(f'Try \'{word}\'')
    return word


def main():
    clue = {i: list(string.ascii_lowercase) for i in range(5)}

    print('Commands:')
    print('  [hints] (b = black, g = green, y = yellow)')
    print('  use [word] (Choose custom word)')
    print('  exit (Stop winning)\n')
    guessed_word = choose_word([word for word in words if len(set(word)) == 2])

    while True:
        required_letters = defaultdict(int)
        hints = ''
        while True:
            command = input('> ')
            if command == 'exit':
                return
            elif command.split()[0] == 'use':
                guessed_word = command.split()[1]
                print(f'Using \'{guessed_word}\'')
                continue
            else:
                hints = command
                break
        
        if hints == 'ggggg':
            print(f'Lett ått me, si. Du har vunnit!')
            break

        update_clue(clue, required_letters, guessed_word, hints)

        guessed_word = choose_word(find_words(clue, required_letters))

if __name__ == '__main__':
    main()
