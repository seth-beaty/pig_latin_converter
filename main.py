"""Convert a word to pig latin"""

import string
import textwrap
import pyperclip

consonant_cluster_size = 0


def is_vowel(char):
    vowels = ['a', 'e', 'i', 'o', 'u']
    if char in vowels:
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


def get_pig_latin_word(word):
    """Format given word in pig latin, taking punctuation into account"""

    # TODO: Implement quote handling
    # start_index = word.find('\"')
    #
    # if start_index != -1:
    #     word, end_index = capture_quotes(word, start_index)

    last_char_in_word = word[-1]
    word_ends_with_punctuation = False
    first_char_upper = False
    if last_char_in_word in string.punctuation:
        word_ends_with_punctuation = True

    if word[0].isupper():
        first_char_upper = True

    pig_latin_word = ""
    if word_ends_with_punctuation:
        # If the word starts with a vowel and has punctuation, add 'way'
        # and the punctuation to the end of the word.
        if is_vowel(word[0]):
            pig_latin_word = word[:-1].lower() + f"way{last_char_in_word}"
        elif starts_with_consonant_cluster(word):
            pig_latin_word = (word[consonant_cluster_size:].lower() +
                              word[0:consonant_cluster_size].lower() + f"ay{last_char_in_word}")
        else:
            # Else add the first letter to the end and append 'ay' if it is a consonant
            pig_latin_word = word[1:-1].lower() + word[0].lower() + f"ay{last_char_in_word}"

    else:
        if is_vowel(word[0]):
            pig_latin_word = word.lower() + f"way"
        elif starts_with_consonant_cluster(word):
            pig_latin_word = (word[consonant_cluster_size:].lower() +
                              word[0:consonant_cluster_size].lower() + f"ay")
        else:
            # Else add the first letter to the end and append 'ay' if it is a consonant
            pig_latin_word = word[1:].lower() + word[0].lower() + f"ay"

    if first_char_upper:
        pig_latin_word = list(pig_latin_word)
        pig_latin_word[0] = pig_latin_word[0].upper()
        pig_latin_word = "".join(pig_latin_word)

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
    # capture_quotes("\"relo\"", 0)


if __name__ == "__main__":
    main()
