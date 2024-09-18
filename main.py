"""Convert a word to pig latin"""

import string
import textwrap
import pyperclip

consonant_cluster_size = 0


def is_vowel(char):
    vowels = ['a', 'e', 'i', 'o', 'u']
    if char.lower() in vowels:
        return True
    return False


def set_consonant_cluster_size(consonant_count):
    global consonant_cluster_size
    consonant_cluster_size = consonant_count


def starts_with_consonant_cluster(word):
    consonant_count = 0
    index = 0
    if len(word) > 2:
        # Check the first 3 letters of the word
        while index < len(word[:3]):
            if index > 0:
                # If the first two letters are consonants, then increment the counter
                if not is_vowel(word[index]) and not is_vowel(word[index - 1]):
                    consonant_count += 1
            else:
                if not is_vowel(word[index]):
                    consonant_count += 1
            index += 1

    if consonant_count > 1:
        set_consonant_cluster_size(consonant_count)
        return True
    return False


# TODO: Implement quote handling
def capture_quotes(word, start_index):
    end_index = word.find('\"', start_index + 1)
    word = word.strip('\"')
    if end_index != -1:
        return word, end_index
    return word


def process_word(word, suffix, prepend_quote=False, append_quote=False):
    if prepend_quote and append_quote:
        return "\"" + word + suffix + "\""
    elif prepend_quote and not append_quote:
        return "\"" + word + suffix
    elif append_quote and not prepend_quote:
        return word + suffix + "\""
    else:
        return word + suffix


def get_pig_latin_word(word):
    """Format given word in pig latin, taking punctuation into account"""

    # Preprocessing

    # Handle double quotes
    start_index = word.find('\"')

    append_quote = False
    prepend_quote = False

    if start_index != -1:
        end_index = word.find('\"', start_index + 1)
        if start_index == 0:
            prepend_quote = True
        if end_index != -1 or start_index == word.find(word[-1]):
            append_quote = True
        word = word.strip('\"')

    # Set needed variables
    last_char_in_word = word[-1]

    # Boolean determinants
    word_ends_with_punctuation = False
    first_char_upper = False
    word_upper = False

    if last_char_in_word in string.punctuation:
        word_ends_with_punctuation = True

    if word[0].isupper() and not word.isupper():
        first_char_upper = True

    if word.isupper():
        word_upper = True

    # Data manipulation
    pig_latin_word = ""
    if word_ends_with_punctuation:
        # If the word starts with a vowel and has punctuation, add 'way'
        # and the punctuation to the end of the word.
        if is_vowel(word[0]):
            pig_latin_word = process_word(word[:-1].lower(),
                                          f"way{last_char_in_word}", prepend_quote, append_quote)

        elif starts_with_consonant_cluster(word):
            pig_latin_word = process_word(word[consonant_cluster_size:-1].lower() +
                                          word[0:consonant_cluster_size].lower(), f"ay{last_char_in_word}",
                                          prepend_quote, append_quote)
        else:
            # Else add the first letter to the end and append 'ay' if it is a consonant
            pig_latin_word = process_word(word[1:-1].lower() + word[0].lower(), f"ay{last_char_in_word}",
                                          prepend_quote, append_quote)
    else:
        if is_vowel(word[0]):
            pig_latin_word = process_word(word.lower(), f"way", prepend_quote, append_quote)
        elif starts_with_consonant_cluster(word):
            pig_latin_word = process_word(word[consonant_cluster_size:].lower() +
                                          word[0:consonant_cluster_size].lower(), f"ay",
                                          prepend_quote, append_quote)
        else:
            # Else add the first letter to the end and append 'ay' if it is a consonant
            pig_latin_word = process_word(word[1:].lower() + word[0].lower(), f"ay", prepend_quote, append_quote)

    if first_char_upper:
        pig_latin_word = list(pig_latin_word)
        pig_latin_word[0] = pig_latin_word[0].upper()
        pig_latin_word = "".join(pig_latin_word)

    elif word_upper:
        pig_latin_word = pig_latin_word.upper()

    return pig_latin_word


def main():
    """Take a word from the user and convert it to pig latin."""

    print("\n\n")
    print("Welcome to the Pig Latin converter.")

    while True:
        user_input = input("Please enter a word or phrase.\n")

        # Split the string into a list
        input_list = user_input.split()

        result_text = ' '.join([get_pig_latin_word(w) for w in input_list])
        print(textwrap.fill(result_text))

        pyperclip.copy(result_text)
        print("\n****************************************************************************")
        print("Result copied to clipboard.")

        try_again = input("\n\nTry again? (Press Enter else n to quit)\n ")
        if try_again.lower() == "n":
            break


if __name__ == "__main__":
    main()
