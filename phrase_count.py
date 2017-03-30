from collections import defaultdict
# from collections import OrderedDict
from operator import itemgetter
import re, string

filename = "samuel_l_jackson.txt"
file_ = open(filename)

def split_sentences(ss):
    return re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", ss.strip()) # .strip() removes line breaks
    # in future consider how to check for "Mrs." as adding (?<!(Mrs)\.) creates a NoneType

def file_sentence_list(ff):
    sentence_list = []
    for line in ff:
        if line is not "\n":
            sentence_list.extend(split_sentences(line))
    return [strip_punctuation(sentence).lower() for sentence in sentence_list]

def strip_punctuation(ss):
    # future: consider addressing contractions and possessives
    punctuation = ",:.?!"
    return ''.join(char for char in ss if char not in punctuation)

def count_words(ss):
    word_count = defaultdict(int)
    for word in ss.split():
        word_count[strip_punctuation(word).lower()] += 1
    return word_count

sentences = file_sentence_list(file_)
words = count_words(" ".join(sentences))


print(sentences)
print(sorted(words.items(), reverse=True, key=itemgetter(1)))
# print(string.punctuation)
