import sys
import itertools

def main(inW):
    mylist = [x for x in inW]
    out = []
    for i in xrange(2,len(inW)+1):
        t = (itertools.permutations(mylist,i))
        for each in t:
            out.append(''.join(each))
    
    f = open('enable1.txt')
    flist = (x.strip() for x in f)
    olist = set.intersection(set(out),set(flist))
    print olist
                    
if __name__ == "__main__":
    main(sys.argv[1])