"""
    Execution:
        python frequencyCounter.py L < input.txt
    Data files:   
        https://algs4.cs.princeton.edu/31elementary/tnyTale.txt
        https://algs4.cs.princeton.edu/31elementary/tale.txt
        https://algs4.cs.princeton.edu/31elementary/leipzig100K.txt
        https://algs4.cs.princeton.edu/31elementary/leipzig300K.txt
        https://algs4.cs.princeton.edu/31elementary/leipzig1M.txt

    Read in a list of words from standard input and print out
    the most frequently occurring word that has length greater than
    a given threshold.

    % python frequencyCounter.py 1 < tinyTale.txt
    it 10
  
    % python frequencyCounter.py 8 < tale.txt
    business 122
  
    % python frequencyCounter.py 10 < leipzig1M.txt
    government 24763
"""

import sys

import SequentialSearchST, BinarySearchST, BST, RedBlackBST 

class FrequencyCounter:

    @classmethod
    def count(cls):
        distinct = 0                    # number of distinct words in input.txt
        words = 0                       # number of words in input.txt 
        minlen = int(sys.argv[1])       # a threshold from command line

        st = RedBlackBST()      # initialize a symbol table from either SequentialSearchST, BinarySearchST, BST, RedBlackBST

        for line in sys.stdin:
            words = line.split()
            for word in words:
                if len(word) < minlen:
                    continue
                words += 1
                if not st.contains(word):
                    st.put(word, 1)
                    distinct += 1
                else:
                    st.put(word, st.get(word) + 1)

        # find a key with the highest frequency count
        Max = ""
        st.put(Max, 0)
        for word in st.keys():
            if st.get(word) > st.get(Max):
                Max = word
        print(Max, " ", st.get(Max))


if __name__ == '__main__':

    counter = FrequencyCounter()