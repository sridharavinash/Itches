#!/usr/bin/python
# simple python program to generate a valid word list from input letters
# To use this program download the word list file and put it in the same folder as this file:
# http://code.google.com/p/dotnetperls-controls/downloads/detail?name=enable1.txt

import sys
import itertools

def main(inW):
    print "Finding Scrabble words for:", inW
    mylist = [x for x in inW]
    out = []
    for i in xrange(2,len(inW)+1):
        t = (itertools.permutations(mylist,i))
        for each in t:
            out.append(''.join(each))
    
    f = open('enable1.txt')
    flist = (x.strip() for x in f)
    olist = set.intersection(set(out),set(flist))
    olist = sorted(olist,key=len)
    olist.reverse()
    print olist
                    
if __name__ == "__main__":
    try:
        main(sys.argv[1])      
    except IndexError:
        print "usage:",sys.argv[0], "letters_combination"
