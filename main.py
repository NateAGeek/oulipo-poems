import pandas;
import re;

# Do some magic to the poem to make it like cool
def poem_magic(poem, dictionary: pandas.DataFrame):
    # Poems have all kinds of formatting and I just wanna split out and get the words
    # This does leave some '', but I ignore them/don't care
    words = re.split('\s+| +|; |, |\n|\r', poem);
    # This will be an array of words that will
    new_poem = [];

    # Out of all the words, pull a word out and put it in the word var
    for word in words:

        # Need to remove the . and , that can follow words. I need just the word to look up in dic
        clean_word = word.replace(".", "").replace(",", "");
        # Using the capitalize clean_word(since the dict has all words capitalized) I look to see if the word and the pos i a n
        dic_words = dictionary.loc[((dictionary['Word'] == clean_word.capitalize())) & (dictionary['POS'] == "\"n.\"")]
        
        # If we were able to find a noun in the dict, then we probably have a list of defs
        if not dic_words.empty:
            # Get all the indexes(row numbers) for all the defs
            indexes = dic_words.index.values

            # Using the last index, get the next words that follow, by 7 in this case
            new_word = next_words_after(indexes[-1], 7, dictionary)

            # Some words have commas or . at the end, I want to keep those
            if "," in word:
                new_word = str(new_word).lower() + ","
            elif "." in word:
                new_word = str(new_word).lower() + "."
            
            # If a word follows a word with a . then I need to make sure it is capitalized
            if "." in new_poem[-1]:
                new_word = str(new_word).capitalize()

            # Append the new word
            new_poem.append(new_word)
        else:
            # If it is not a noun, then just put it into the the poem
            new_poem.append(word)
    # join them all by spaces and call it a day 
    return " ".join(new_poem)

# Finds the next n words after an index in a dict
def next_words_after(index, number_of_words, dictionary: pandas.DataFrame):
    # Starting off with one word
    word_count = 1;
    word = dictionary.loc[index + 1]['Word'];

    # Go through the whole dict
    for idx in range(index, dictionary.size):
        # If we come to an index that is a new word than we have searched for
        # we increment our searched word_count.
        if word != dictionary.loc[idx]['Word']:
            word = dictionary.loc[idx]['Word'];
            word_count += 1

        # once we reach our word_count, return our new word for the poem
        if word_count >= number_of_words:
            return dictionary.loc[idx]['Word']

def main():
    poems = pandas.read_csv("./PoetryFoundationData.csv")
    dictionary = pandas.read_csv("./OPTED-Dictionary.csv")
    new_poem = poem_magic(poems.loc[0]['Poem'], dictionary);
    # Only does first poem, but a for loop can make it all
    print(poems.loc[0]['Poem'])
    print(new_poem)


if __name__ == '__main__':
    main()