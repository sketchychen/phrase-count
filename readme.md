## challenge:

Given a string representing a document, write a function which returns the top 10 most frequent repeated phrases. A phrase is a stretch of three to ten consecutive words and cannot span sentences. Only include a phrase if it is not a subset of another, longer phrase (if “calm cool” and “calm cool and collected” are repeated, do not include “calm cool” in the returned set).

## current game plan:
- ~LEARN HOW TO REGEX~
- convert txt file to list of strings.
  - more specifically list of sentences, as phrases do not span sentences.
- make everything lowercase and remove major punctuation (",:.?!") from words.
  - sometimes a phrase may occur before a comma but again before a period, but it's still the same phrase.
  - apostrophes and hyphens are usually used to combine words rather than clauses or phrases, so I won't remove those.
- generate list of all phrases possible from each sentence with word lengths 3 to 10.
- go through list and create a dictionary counting the occurrence of each phrase.
- sort list by string length and check each string (starting with the shortest) against the rest until a subset is found with the appropriate phrase count condition.
  - remove subset with correct phrase count condition from list and continue check with the next shortest phrase.
- return resulting list, sorted by phrase count in descending order, calling out the first ten in the list.
<!-- - count frequency of words (removing punctuation will allow "human," to count as "human", "help." as "help", and etc.).
  - plural words are counted as distinct from their singular form.
  - similarly, all verb tenses are counted as distinct from one another.
  - phrases are therefore assumed consistent across the board plurality-wise, spelling-wise, punctuation-wise, etc.
  - I mean, hopefully people think to proofread for typos and consistent punctuation rules (even if ultimately misused).
  - It's really just to make it easier for me right now but it's entirely possible to add in an additional "parser" later as a future feature.
- use one-time-occurring words to eliminate one-time-occurring phrases (to reduce what we have to search through). -->
