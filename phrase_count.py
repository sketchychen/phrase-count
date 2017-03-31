from collections import defaultdict
from operator import itemgetter
import re

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

# SPLIT SENTENCES INTO FRAGMENTS BASED ON SINGLE-OCCURRING WORDS
def fragment_sentence_by_word(sentence, word_list):
  # input string and list, return list
    fragments = [sentence]
    for word in word_list: # iterate through each word in word_list
      for frag in fragments: # iterate through each "frag" (starts with a "full" sentence)
        if word in frag.split():
          temp = frag.split()
          temp = temp[:temp.index(word)], temp[temp.index(word)+1:]
          # IGNORE FRAGMENTS WITH WORD LENGTH < 3 WORDS (phrases are 3-10 words long)
          fragments = [" ".join(words) for words in temp if len(words) >= 3]
    return fragments

# COMPILE ALL PHRASE-FEASIBLE FRAGMENTS INTO ONE LIST
def fragment_sentence_list(sentence_list, word_list):
    fragments = []
    for sentence in sentence_list:
        fragments.extend(fragment_sentence_by_word(sentence, word_list))
    return fragments

# GENERATE LIST OF PHRASES WITH WORD LENGTH INT N FROM GIVEN STRING
def get_n_word_phrases(ss, n):
  phrase_list = []
  ss_split = ss.split()
  if len(ss_split) >= n: # ideally we account for this in our input but it's here too just in case
    for i in range(0, len(ss_split)-n+1):
      phrase = " ".join(ss_split[i:i+n])
      phrase_list.append(phrase)
  return phrase_list # returns empty if n > len(ss_split)

def multiple_n_word_phrases(ss, phrase_lengths): # phrase_lengths is a list of positive integers, or range(i, j)
    phrase_list = []
    for n in phrase_lengths:
        phrase_list.extend(get_n_word_phrases(ss, n))
    return phrase_list

# GENERATE DEFAULTDICT OF POSSIBLE PHRASES AND THEIR COUNTS
def count_phrases(sentence_list, phrase_lengths): # both are list inputs
    phrase_count = defaultdict(int)
    for sentence in sentence_list:
        phrase_list = []
        # if the sentence is the minimum number of words
        if len(sentence.split()) == min(phrase_lengths):
            # run get_n_word_phrases only once
            phrase_list = get_n_word_phrases(sentence, len(sentence.split()))
        # if the sentence is less than the maximum number of words
        elif len(sentence.split()) < max(phrase_lengths):
            # run get_n_word_phrases from minimum to up to just the length of the sentence
            phrase_list = multiple_n_word_phrases(sentence, range(min(phrase_lengths), len(sentence.split())+1))
        # if the sentence is greater than the maximum number of words
        elif len(sentence.split()) >= max(phrase_lengths):
            # run get_n_word_phrases with the given phrase_lengths
            phrase_list = multiple_n_word_phrases(sentence, phrase_lengths)
        # else, sentence is probably less than the minimum number of words,
            # so don't do anything.

        # bookkeep every phrase generated from a sentence
        for phrase in phrase_list:
            phrase_count[phrase] += 1

    return phrase_count

# SORT DEFAULTDICT OF PHRASES BY PHRASE LENGTH AND COMPARE ITEMS IN DEFAULTDICT TO ONE ANOTHER
# TO FIND AND REMOVE SUBSETS WHERE APPROPRIATE
def find_subset_phrases(phrase_count_dict):
    sorted_by_len = sorted(phrase_count.items(), key=lambda s: len(s[0])) # sort the dict by phrase length ascending (and as tuples, looks like)
    # if a phrase1 is found in phrase2 but phrase1's count is higher, it's not a subset
    # if a phrase1 is found in phrase2 and has the same phrase count (or less? is that even possible?), it's a subset
    # so only remove a phrase if a same phrase count condition is met
    index1 = 0
    index2 = index1 + 1
    while index1 < len(sorted_by_len)-1:
        subset_found = False
        index2 = index1 + 1
        while index2 < len(sorted_by_len)-1 and not subset_found:
            phrase1 = sorted_by_len[index1]
            phrase2 = sorted_by_len[index2]
            if len(phrase1[0].split()) < len(phrase2[0].split()) and phrase1[0] in phrase2[0] and phrase1[1] <= phrase2[1]:
                subset_found = True
                del sorted_by_len[index1]
            else:
                index2 += 1
        if not subset_found:
            index1 += 1
        # print(sorted_by_len)
    return sorted(sorted_by_len, key=lambda s: s[1], reverse=True)



sentences = file_sentence_list(file_)

# sentences is a list of strings while file_ is a file object, so might as well
# use what's already got strings instead of converting file_ to string again
# to get the list of words
words = count_words(" ".join(sentences))

# WORDS THAT ONLY APPEAR ONCE IMPLY THAT THE PHRASES THEY'RE IN ALSO OCCUR ONCE
single_occurrence_words = [word_count[0] for word_count in words.items() if word_count[1] == 1]
    # words.items() returns list of tuples
# print(single_occurrence_words)

fragments = fragment_sentence_list(sentences, single_occurrence_words)
phrase_count = count_phrases(fragments, range(3, 10))

# print(fragments)
# print(get_n_word_phrases(fragments[8], 7))
# print(phrase_count)
# print(sorted(phrase_count.items(), key=lambda s: len(s[0])))
# print(sorted(phrase_count.items(), key=lambda s: s[1], reverse=True))
print(find_subset_phrases(phrase_count))
