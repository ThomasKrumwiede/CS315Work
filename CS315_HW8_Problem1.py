import string


# class for the construction of nodes
class TrieNode:
    def __init__(self, n):
        # Create the array of pointers to child nodes
        self.children = [None] * n
        # the paylod is initially empty
        self.payload = None
        # inittialy this will not correspond to a word
        self.isEndOfWord = False


# call to create a new node
def TrieCreateNode(n):
    return TrieNode(n)


# Inserts a key into a Trie
def TrieInsertKey(N, key, j, p):

    # Check if there are any symbols left in the key
    if j == len(key):
        # Mark this node as being the end of a word and store the payload
        N.isEndOfWord = True
        N.payload = p
        return

    # If there are symbols left in the key, see if there is already a node for the next symbol
    symbol = key[j]
    i = ord(symbol) - ord('a')
    if 0 <= i < len(N.children):
        if N.children[i] is None:
        # This symbol hasn't been seen yet so create a new node
            N.children[i] = TrieCreateNode(26)
        # Recursively insert the remainder of the key
        TrieInsertKey(N.children[i], key, j + 1, p)
    else:
        print(f"Illegal character encountered: {symbol}")


# Fetches a key from a Trie and returns the associated payload
def TrieFetchKey(N, key, j):

    # Check if all the symbols in the key have been accounted for
    if j == len(key):
        # Make sure this node has been marked as a word
        if N.isEndOfWord:
            return True, N.payload
        else:
            return False, None

    # Otherwise get the next symbol from the key and the
    # position of this symbol in the alphabet
    symbol = key[j]
    i = ord(symbol) - ord('a')

    # Fetch the child node corresponding to this index
    child = N.children[i]
    if child is None:
        return False, None
    # Recursively fetch the next part of the key
    return TrieFetchKey(child, key, j + 1)


# Finds all the words in the Trie with the given prefix
def TrieSuggest(N, prefix, j, sofar, suggestions):

    # Check if we have matched the whole prefix
    if j < len(prefix):
        # Follow the letters of the prefix through the Trie in the same manner as fetching a key
        symbol = prefix[j]
        i = ord(symbol) - ord('a')
        child = N.children[i]
        if child is not None:
            sofar += symbol
            TrieSuggest(child, prefix, j + 1, sofar, suggestions)
    else:
        # We have exhausted the prefix. Check if the prefix is itself a known word.
        if N.isEndOfWord:
            suggestions.append(sofar)

        # Find any words that match this prefix
        for i, child in enumerate(N.children):
            if child is not None:
                symbol = chr(i + ord('a'))
                TrieSuggest(child, prefix, j, sofar + symbol, suggestions)


# Input the words from the dictionary into the trie

# Create the root
root = TrieCreateNode(26)


# Function to check if a word contains punctuation
def has_punctuation(word):
    for char in word:
        if char in string.punctuation:
            return True
    return False


# Reed through the entire american-english dictionary and place each word
# that is only made up of letters into the thr tire
with open('C:/Users/Thoma/Desktop/CS315/american-english', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line into words
        line = line.strip()
        # Process each word
        if line:
            # Convert word to lowercase
            words = line.split()
            # Check if word contains punctuation
            for word in words:
                word = word.lower()
                if not has_punctuation(word) and "'" not in word and "ã" not in word:
                    TrieInsertKey(root, word, 0, word[0].upper)


#Homework probelms

#Problem a)
print(TrieFetchKey(root, "boat", 0))

#Proiblem b)
print(TrieFetchKey(root, "xyzzy", 0))

#problem c)
print("\nSuggestions for prefix 'fro':")
suggestions = []
TrieSuggest(root, "fro", 0, "", suggestions)
print(suggestions)