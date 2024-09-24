"""Convert a word to pig latin"""

import string
import textwrap
import pyperclip


def is_vowel(char, word):
    if 'y' in word.lower() and len(word) >= 3 and word[1] == 'y':
        return char.lower() in 'aeiouy'
    return char.lower() in 'aeiou'


def starts_with_consonant_cluster(word):
    word = word.lower()
    consonant_cluster_size = 0
    if len(word) >= 2:
        for i, char in enumerate(word[:3]):
            if not is_vowel(char, word):
                consonant_cluster_size += 1
            else:
                break

    return consonant_cluster_size if consonant_cluster_size > 1 else 0


def handle_quotes(word):
    prepend_quote = word.startswith('\"')
    append_quote = word.endswith('\"')
    word = word.strip('\"')
    return word, prepend_quote, append_quote


def process_word(word, suffix, prepend_quote=False, append_quote=False):
    if prepend_quote:
        word = "\"" + word
    if append_quote:
        word += "\""
    return word + suffix


def get_pig_latin_word(word):
    """Format given word in pig latin, taking punctuation into account"""

    word, prepend_quote, append_quote = handle_quotes(word)

    last_char = word[-1] if word[-1] in string.punctuation else ''
    word = word[:-1] if last_char else word

    first_char_upper = word[0].isupper()
    word_upper = word.isupper()

    if is_vowel(word[0], word):
        pig_latin_word = word + "way"
    else:
        cluster_size = starts_with_consonant_cluster(word)
        if cluster_size:
            pig_latin_word = word[cluster_size:] + word[:cluster_size] + "ay"
        else:
            pig_latin_word = word[1:] + word[0] + "ay"

    if first_char_upper:
        pig_latin_word = pig_latin_word.capitalize()

    if word_upper:
        pig_latin_word = pig_latin_word.upper()

    return process_word(pig_latin_word, last_char, prepend_quote, append_quote)


def main():
    """Take a word from the user and convert it to pig latin."""

    print("\n\n")
    print("Welcome to the Pig Latin converter.")

    while True:
        user_input = input("Please enter a word or phrase.\n")

        result_text = ' '.join([get_pig_latin_word(word) for word in user_input.split()])
        print(textwrap.fill(result_text))

        pyperclip.copy(result_text)
        print("\n****************************************************************************")
        print("Result copied to clipboard.")

        try_again = input("\n\nTry again? (Press Enter else n to quit)\n ")
        if try_again.lower() == "n":
            break


if __name__ == "__main__":
    main()
