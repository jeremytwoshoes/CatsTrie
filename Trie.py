class Node:
    """
    The node class for the trie.
    It holds the link, which is a list of 27 elements, one for each letter and one for the special character to
    indicate the end of the trie. It holds the frequency of the whole sentence when it reaches the end of the trie. It also
    holds the frequency of the best/most frequent sub-sentence.

    Time Complexity: O(1)

    Space Complexity: O(1)
    """

    def __init__(self):
        self.link = [None] * 27
        self.frequency = 0
        self.best_sub_frequency = 0


class CatsTrie:
    def __init__(self, sentences):
        """
        Function Description: Constructor for the trie. It creates the root node and calls the insert_recur function for each sentence in the sentence list.

        Function Approach: The insert_recur function inserts each sentence into the trie by traversing the trie and creating new nodes as needed.
        When it reaches the end of the word to insert, it will store the frequency of that word at the end node. As the
        recursive calls return, it will update the best_sub_frequency of each node to be the frequency of the most frequent
        sub-sentence.

        :param sentences: A list of sentences to be inserted into the trie.

        Time Complexity: O(nm) where n is the number of sentences and m is the length of the longest sentence.
            Calculation:
                - The for loop iterates through each sentence in the sentence list, so it is O(n).
                - The insert_recur function traverses the trie, and worst case is that all the words are the longest sentence so O(m).
                - The insert_recur function is called for each sentence, so O(n) * O(m) = O(nm).

        Space Complexity: O(nm) where n is the number of sentences and m is the length of the longest sentence.
                          This is because we have n sentences and in the worst case each will have length m.

        """
        self.root = Node()

        # Insert each sentence into the trie by looping through the sentence list
        for sentence in sentences:
            self.insert_recur(sentence)

    def autoComplete(self, prompt):
        """
        Function Description: This function finds the most frequent word based on the input prompt.

        Function Approach: It calls the findNode function to find the node that corresponds to the last letter of the prompt.
                            If the node is not found, it returns None. If the node is found, it calls the autoCompleteAux function to find the most frequent word.
                            The findNode funtion will find the corresponding node by traversing the trie. If the node is not found, it returns None.
                            The autoCompleteAux function traverses the trie and finds the most frequent word by comparing the best_sub_frequency of each node.
                            It returns the most frequent word. If there is a tie, it returns the word that comes first lexicographically as
                            it will not continue further down the trie if an end node with an equal or greater frequency is found.

        :param prompt: the prompt to find the most frequent word for
        :return: the most frequent word based on the prompt

        Time complexity: O(X + Y) where X is the length of the prompt and Y is the length of the most frequent sentence.
            Calculation: This is because it take O(X) to find the node that corresponds to the last letter of the prompt, by using the findNode function.
                            Then, it takes O(Y) to find the most frequent word, by using the autoCompleteAux function.

        Space Complexity: O(1)
        """

        # set the max_frequency to -1
        max_frequency = -1
        node = self.findNode(prompt) # the findNode function finds the node that corresponds to the last letter of the prompt

        # returns None if the node is not found, meaning the sentence list in empty
        if node is None:
            return None
        return self.autoCompleteAux(node, max_frequency, prompt)

    def autoCompleteAux(self, node, max_frequency, word):
        """
        Function Description: Based on the starting node, this function will traverse the trie and find the most frequent word.

        Function Approach: It will compare the best_sub_frequency of each node and return the most frequent word. Because
                            we store the best_sub_frequency at each node, comparison at each level in O(1). If there is a tie, it will return
                            the word that comes first lexicographically as it will not continue further down the trie. If an end node with an equal
                            or greater frequency is found it means that the current word at this node is tied as most frequent word,
                            so we return this and do not continue traversing the trie


        :param node: The node to start searching from
        :param max_frequency: The maximum frequency of the most frequent word found so far
        :param word: The word that has been found so far
        :return: The most frequent word based on the prompt

        Time Complexity: O(Y) where Y is the length of the most frequent sentence.

        """
        current = node

        # checks if there are any other links from the current node, if not, it means we reached the end of the word
        if all(link is None for link in current.link[1:]):
            return word  # Return the completed word

        max_frequency = -1
        best_sub_node = None

        # loops through all the items in the link, and finds the node with the highest best_sub_frequency but updates the max_frequency
        for i in range(1, 27):
            if current.link[i] is not None and current.link[i].best_sub_frequency > max_frequency:
                max_frequency = current.link[i].best_sub_frequency
                best_sub_node = current.link[i]
                index = i

        # if the current node has a frequency greater than the max_frequency, it will return the word
        # it means that the current word at this node is tied as most frequent word, so we return this and do not continue traversing the trie
        if current.link[0] is not None:
            current = current.link[0]
            if current.frequency >= max_frequency:
                return word

        # if the best_sub_node is not None, convert index to a char, so we build the word as we traverse the trie
        if best_sub_node is not None:
            char = chr(index + 96)  # Convert index back to character
            return self.autoCompleteAux(best_sub_node, max_frequency, word + char)

        return None

    def findNode(self, prompt):
        """
        Function Description: This function finds the node that corresponds to the last letter of the prompt.
                            If the node is not found, it returns None

        Function Approach: It traverses the trie and returns the node that corresponds to the last letter of the prompt.
                            If the node is not found, it returns None. It will iterate through the prompt and traverse the trie
                            based on the characters in the prompt. If the character is not found, it will return None,
                            meaning the word does not exist. If the prompt is empty, it will return the root node.

        :param prompt: The suffix of a sentence to find the node for
        :return: The node that corresponds to the last letter of the prompt

        Time complexity: O(X) where X is the length of the prompt.
        Space complexity: O(X) where X is the length of the prompt.
        """
        current = self.root
        # loops through the characters in the prompt and traverses the trie based on the characters in the prompt
        for char in prompt:
            index = ord(char) - 97 + 1
            # if the character is not None, means we continue traversing the trie, else we return None
            if current.link[index] is not None:
                current = current.link[index]
            else:
                return None
        return current

    def insert_recur(self, key):
        """
        Function Description: This function inserts a sentence into the trie. It calls the insert_recur_aux function to
        insert the sentence into the trie.

        Function Approach: Sets the current node to the root and calls the insert_recur_aux function to insert the sentence
        :param key: The sentence to be inserted

        Time Complexity: O(m) where m is the length of the sentence.
            Calculation: The insert_recur_aux function traverses the trie as many times as the word is long, therefore O(m).

        Space Complexity: O(m) where m is the length of the sentence.
        """

        current = self.root
        self.insert_recur_aux(current, key)

    def insert_recur_aux(self, current, key):
        """
        Function Description: This function inserts a sentence into the trie. It calls the insert_recur_aux function to
        insert the sentence into the trie.

        Function Approach: The insert_recur_aux function inserts the sentence into the trie by traversing the trie and creating
        new nodes as needed. When it reaches the end of the word to insert, it will store the frequency of that word at the
        end node. As the recursive calls return, it will update the best_sub_frequency of each node to be the frequency of
        the most frequent sub-sentence.

        :param current: The current node to insert the sentence into
        :param key: The sentence to insert
        :return: The best_sub_frequency of the current node, used to update the best_sub_frequency of the previous node

        Time Complexity: O(m) where m is the length of the sentence.
        Space Complexity: O(m) where m is the length of the sentence.
        """

        # Base case
        if len(key) == 0:
            # what happens when I have gone through all my alphabets in key
            if current.link[0] is None:
                current.link[0] = Node()
            current = current.link[0]
            current.frequency += 1
            if current.frequency > current.best_sub_frequency:
                current.best_sub_frequency = current.frequency

            return current.best_sub_frequency
        else:
            # calculate index
            # $ = 0, a = 1, b = 2
            index = ord(key[0]) - 97 + 1
            # if path exists
            if current.link[index] is not None:
                current = current.link[index]
            # if path does not exist
            else:
                # create a new node
                current.link[index] = Node()
                current = current.link[index]

            # returns the sub_frequency of the previous node
            sub_frequency = self.insert_recur_aux(current, key[1:])

            # if the sub_frequency is greater, update the best_sub_frequency
            if sub_frequency > current.best_sub_frequency:
                current.best_sub_frequency = sub_frequency

            return current.best_sub_frequency


if __name__ == "__main__":
    sentences = ["abc", "abazacy", "dbcef", "xzz", "gdbc", "abazacy", "xyz",
                 "abazacy", "dbcef", "xyz", "xxx", "xzz"]
    # Creating a CatsTrie object
    mycattrie = CatsTrie(sentences)

    # A simple example
    prompt = "ab"
    print(mycattrie.autoComplete(prompt)) # should return "abazacy"