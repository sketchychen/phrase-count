from collections import defaultdict
# from collections import OrderedDict
from operator import itemgetter
import re, string

filename = "samuel_l_jackson.txt"
file_ = open(filename)

# GENERATE LIST OF SENTENCES (phrases do not span sentences)
def split_into_sentences(ss):
    return re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", ss.strip()) # .strip() removes line breaks
    # in future consider how to check for "Mrs." as adding (?<!(Mrs)\.) creates a NoneType

# CONVERT TXT FILE TO LIST OF STRINGS (list of sentences)
def file_sentence_list(ff):
    sentence_list = []
    for line in ff:
        if line is not "\n":
            sentence_list.extend(split_into_sentences(line))
    return [strip_punctuation(sentence).lower() for sentence in sentence_list]

# REMOVE PUNCTUATION FOR BETTER DICTIONARY WORD COUNT
# "hello puppy. Puppy is happy" will count puppy as ("puppy", 2) instead of ("puppy.", 1), ("Puppy", 1)
def strip_punctuation(ss):
    # future: consider addressing contractions and possessives
    punctuation = ",:.?!"
    return ''.join(char for char in ss if char not in punctuation)

# COUNT OCCURRENCE OF WORDS (as phrases are generally made up of words)
# treating plural words as their own word for now
def count_words(ss):
    word_count = defaultdict(int)
    for word in ss.split():
        word_count[strip_punctuation(word).lower()] += 1
    return word_count

sentences = file_sentence_list(file_)

# sentences is a list of strings while file_ is a file object, so might as well
# use what's already got strings instead of converting file_ to string again
# to get the list of words
words = count_words(" ".join(sentences))

# WORDS THAT ONLY APPEAR ONCE IMPLY THAT THE PHRASES THEY'RE IN ALSO OCCUR ONCE
single_occurrence_words = [word_count[0] for word_count in words.items() if word_count[1] == 1]
    # words.items() returns list of tuples
# print(single_occurrence_words)

# SPLIT SENTENCES INTO FRAGMENTS BASED ON SINGLE-OCCURRING WORDS
def fragment_sentence_by_word(sentence, word_list):
    # input string and list, return list
    fragments = [sentence]
    # iterate through each word in word_list
    for word in word_list:
      temp = []
      # iterate through each "frag" (starts with a "full" sentence)
      for frag in fragments:
        # IGNORE EMPTY FRAGMENTS AND FRAGMENTS WITH WORD LENGTH < 3 WORDS (phrases are 3-10 words long)
        temp.extend([frag.strip() for frag in frag.split(word) if len(frag) > 0 and len(frag.split()) >= 3])
        # THIS DOES NOT TAKE INTO ACCOUNT WORDS "WITHIN" WORDS (so you don't remove "a" from "america" and end up with "americ")
      fragments = temp
    return fragments

# COMPILE ALL PHRASE-FEASIBLE FRAGMENTS INTO ONE LIST
def fragment_sentence_list(sentence_list, word_list):
    fragments = []
    for sentence in sentence_list:
        fragments.extend(fragment_sentence_by_word(sentence, word_list))
    return fragments


print(fragment_sentence_list(sentences, single_occurrence_words))

# print(sentences)
# print(sorted(words.items(), reverse=True, key=itemgetter(1)))
# print(string.punctuation)
# print([word_count[0] for word_count in words.items() if word_count[1] == 1])
