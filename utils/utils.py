


"""
# Usage example

>>> query_yes_no("Is cabbage yummier than cauliflower?")
Is cabbage yummier than cauliflower? [Y/n] oops
Please respond with 'yes' or 'no' (or 'y' or 'n').
Is cabbage yummier than cauliflower? [Y/n] y
>>> True

"""
import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("respond with 'y' or 'n'.\n")



import collections
def unique_words(corpus_file):
    words = collections.Counter()
    for line in corpus_file:
        words.update(line.decode('utf-8').split())

    most_used = tuple(['', 0])
    unique = 0
    largest_word = ''
    for word, count in words.iteritems():
        unique += 1
        if len(word) > len(largest_word) and word.isalpha():
            largest_word = word
        if count > most_used[1] and len(word) > 5:
            most_used = (word, count)

    print 'most frequently used (' + str(most_used[1]) + '): ' + most_used[0]
    print 'largest word: ' +  largest_word
    print 'unique words: ' + str(unique)
