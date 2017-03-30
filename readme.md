## challenge:

Given a string representing a document, write a function which returns the top 10 most frequent repeated phrases. A phrase is a stretch of three to ten consecutive words and cannot span sentences. Only include a phrase if it is not a subset of another, longer phrase (if “calm cool” and “calm cool and collected” are repeated, do not include “calm cool” in the returned set).

## current game plan:
- convert txt file to list of strings (sentence)
- make everything lowercase and remove punctuation from words
- count frequency of words (removing punctuation will allow "human," to count as "human", "help." as "help", and etc.)
- use one-time-occurring words to eliminate one-time-occurring phrases (to reduce what we have to search through)
- find some way to iterate through remaining fragments for phrases taking into account subsets
