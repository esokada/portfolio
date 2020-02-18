import random


def processtext(filename, startcue=None, skipcue=None, endcue=None):
    # Open the book file, strip it of header/footer,
    # and return a list of words.
    with open(filename, "r", encoding="utf8") as f:
        trimmedlines = ""
        startpoint = False
        for line in f:
            # Eliminate the header, chapter headings, and footer.
            if startcue:
                if startcue in line:
                    startpoint = True
                    continue
            else:
                startpoint = True
            if skipcue:
                    if skipcue in line:
                        continue
            if endcue:
                if endcue in line:
                    break
            # Remove most punctuation. Keep periods and capitalization
            # to produce more natural sentence starts/ends.
            if startpoint is True:
                line = line.replace(",", "")
                line = line.replace("“", "")
                line = line.replace("”", "")
                line = line.replace(":", "")
                line = line.replace("_", "")
                line = line.replace("—", " ")
                line = line.replace("?", ".")
                line = line.replace("!", ".")
                trimmedlines += line
    words = trimmedlines.split()
    return words


def build_trigrams(words):
    """
    Build up the trigrams dict from the list of words.

    Return a dict with:
       keys: word pairs
       values: list of followers
    """
    trigrams = {}
    for i in range(len(words) - 2):
        pair = words[i:i + 2]
        follower = words[i + 2]
        # If the pair of words is already a key in the dictionary,
        # add the follower to it. Otherwise, add a new key.
        if tuple(pair) in trigrams:
            trigrams[tuple(pair)].append(follower)
        else:
            trigrams.update({tuple(pair): [follower]})
    return trigrams


def generate_text(trigrams):
    # Use the trigrams dictionary to generate a string of random text.
    text_list = []
    # Choose a random location to begin the text and add the first two words.
    first_word_location = random.randint(0, len(words) - 2)
    text_list.append(words[first_word_location])
    text_list.append(words[first_word_location + 1])
    # Add more words.
    while True:
        prevword = text_list[-2]
        currword = text_list[-1]
        options = []
        if (prevword, currword) in trigrams:
            options = trigrams[(prevword, currword)]
            selection = random.choice(options)
            text_list.append(selection)
        # Stop if we end up with a pair that's not in the trigrams.
        else:
            break
        # Set a maximum length for the text.
        if len(text_list) >= 200:
            break
    finaltext = " ".join(text_list)
    # Add a final period to the end of the text.
    if finaltext[-1] != ".":
        finaltext += "."
    # Capitalize the first letter of the text and print.
    print(finaltext[0].upper() + finaltext[1:])


if __name__ == "__main__":
    words = processtext("styles.txt", "Contents",
                        "CHAPTER", "End of Project Gutenberg's")
    trigrams = build_trigrams(words)
    generate_text(trigrams)