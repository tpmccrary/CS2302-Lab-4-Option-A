# **********************************************************************************************************************
# NAME: Timothy P. McCrary
# CLASS: CS 2302
# LAB 4 OPTION A
# INSTRUCTOR: Diego Aguirre
# TA: Manoj Pravaka Saha
# DATE: 11/09/2018
# PURPOSE: The purpose of this lab is to effectively implement a Hash Table in order to achieve better running times.
# **********************************************************************************************************************
import time

hash_function_choice = 2  # 1 or 2.


def main():
    hash_table_size = 436121  # .75 = 327091 / hash_table_size
    print('The hash table size is:', hash_table_size)
    start_time = time.time()
    hash_table = file_to_hash_table(hash_table_size)
    print("\nRunning time of inserting file items into hash table = %s seconds" % (time.time() - start_time))
    print('Average number of comparisons: ', hash_table.avg_comparisons())
    print('Load Factor of Hash Table:', hash_table.compute_load_factor())


# Base of equations from: https://www.minus40.info/sky/alphabetcountdec.html
# Converts word to base 26 number.
def word_to_base26_num(word):
    if len(word) == 1:
        # Base Case. Converts character to unicode integer.
        # Lower case words start on 97, so 96 is subtracted to keep it a base 26 number.
        return ord(word) - 96
    else:
        # Returns word without first letter. Calculates a letters base 26 number in regards to position.
        return word_to_base26_num(word[1:]) + (26 ** (len(word) - 1)) * (ord(word[0]) - 96)


# Takes information from file and stores it into hash table.
def file_to_hash_table(table_size):
    hash_table = HashTable(table_size)
    file = open("glove.6B.50d.txt", encoding="utf8")

    for line in file:
        s = line.split(" ", 1)
        if s[0].isalpha():
            string_embeddings = s[1].split(" ")
            float_embeddings = [float(i) for i in string_embeddings]
            hash_table.insert(s[0], float_embeddings)

    return hash_table


# Counts number of lines in file.
def usable_file_lines():
    file = open("glove.6B.50d.txt", encoding="utf8")
    count = 0

    for line in file:
        s = line.split(" ", 1)
        if s[0].isalpha():
            count = count + 1

    file.close()
    return count


# Class for a hash table node.
class HashTableNode:
    def __init__(self, word, embedding, next):
        self.word = word
        self.embedding = embedding
        self.next = next


# Class for hash table.
class HashTable:
    def __init__(self, table_size):
        self.table = [None] * table_size

    # First hash function. Uses pythons hash() function to make word a number.
    def hash_function1(self, word):
        return hash(word) % len(self.table)

    # Second hash function. Uses word_to_base26_num to convert a word to a base 26 number.
    def hash_function2(self, word):
        return word_to_base26_num(word) % len(self.table)

    # Inserts a new hash node with items word and embedding. Hash function depends on hash_function_choice.
    def insert(self, word, embedding):
        if hash_function_choice == 1:
            location = self.hash_function1(word)
        elif hash_function_choice == 2:
            location = self.hash_function2(word)

        self.table[location] = HashTableNode(word, embedding, self.table[location])

    # Searches and returns node using word as key. Hash function depends on hash_function_choice.
    def search(self, word):
        if hash_function_choice == 1:
            location = self.hash_function1(word)
        elif hash_function_choice == 2:
            location = self.hash_function2(word)

        current_node = self.table[location]
        while current_node is not None:
            if current_node.word == word:
                return current_node

            current_node = current_node.next

        return None

    # Returns number of comparisons made in order to find a certain word. Hash function depends on hash_function_choice.
    def num_comparisons_search(self, word):
        if hash_function_choice == 1:
            location = self.hash_function1(word)
        elif hash_function_choice == 2:
            location = self.hash_function2(word)
        count = 0

        current_node = self.table[location]
        while current_node is not None:
            if current_node.word == word:
                return count
            count = count + 1
            current_node = current_node.next
        print("Could not find word.")
        return -1

    # Finds average number of comparisons for the whole hash table.
    def avg_comparisons(self):
        file = open("glove.6B.50d.txt", encoding="utf8")

        comp_table = []
        comp_counter = 0

        for line in file:
            s = line.split(" ", 1)
            if s[0].isalpha():
                comp_table.append(self.num_comparisons_search(s[0]))

        for i in range(len(comp_table)):
            comp_counter = comp_counter + comp_table[i]

        average = comp_counter / len(comp_table)
        return average

    # Computes the load factor. load factor = number of items / number of buckets.
    def compute_load_factor(self):
        num_buckets = len(self.table)
        word_count = 0

        for bucket in self.table:
            temp = bucket
            while temp is not None:
                word_count = word_count + 1
                temp = temp.next

        load_factor = word_count / num_buckets
        return load_factor


if __name__ == '__main__':
    main()