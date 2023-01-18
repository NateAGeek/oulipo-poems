import pandas;
import re;

def poem_magic(poem, dictionary: pandas.DataFrame):
    words = re.split('\s+| +|; |, |\n|\r', poem);
    new_poem = [];

    for word in words:
        clean_word = word.replace(".", "").replace(",", "");
        dic_words = dictionary.loc[((dictionary['Word'] == clean_word.capitalize())) & (dictionary['POS'] == "\"n.\"")]
        if not dic_words.empty:
            indexs = dic_words.index.values
            new_word = next_words_after(indexs[-1], 7, dictionary)
            if "," in word:
                new_word = str(new_word).lower() + ","
            elif "." in word:
                new_word = str(new_word).lower() + "."
            
            if "." in new_poem[-1]:
                new_word = str(new_word).capitalize()
                
            new_poem.append(new_word)
        else:
            new_poem.append(word)
    return " ".join(new_poem)

def next_words_after(index, number_of_words, dictionary: pandas.DataFrame):
    word_count = 1;
    word = dictionary.loc[index + 1]['Word'];

    for idx in range(index, dictionary.size):
        if word != dictionary.loc[idx]['Word']:
            word = dictionary.loc[idx]['Word'];
            word_count += 1

        if word_count >= number_of_words:
            return dictionary.loc[idx]['Word']

def main():
    poems = pandas.read_csv("./PoetryFoundationData.csv")
    dictionary = pandas.read_csv("./OPTED-Dictionary.csv")
    new_poem = poem_magic(poems.loc[0]['Poem'], dictionary);
    print(poems.loc[0]['Poem'])
    print(new_poem)


if __name__ == '__main__':
    main()