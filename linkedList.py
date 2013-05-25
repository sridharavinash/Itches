"""
A simple linked list node implementation that will follow and print the chain and detect if there is a circular ref.
"""
class node(object):
    def __init__(self,nodeValue,nextNode=None):
        self.nodeVal = nodeValue
        self.nextNode = nextNode

    def setNextNode(self,nextNode):
        self.nextNode = nextNode

    def __str__(self):
        if(self.nextNode is not None):
            return "%s --> %s" %(self.nodeVal,self.nextNode.nodeVal)
        else:
            return "%s --> None" %(self.nodeVal)

def printChain(node):
        currNode = node
        seenNodes = []
        while(currNode is not None):
            if(currNode in seenNodes):
                print currNode.nodeVal, '(Circular reference detected)'
                return
            seenNodes.append(currNode)
            print currNode.nodeVal, '->',
            currNode = currNode.nextNode
        print 'None'

def main():
    nodeValueList = ['A','B','A','D','E','F','G','H']
    nodeObjectsList = []
    for value in nodeValueList:
        nodeObjectsList.append(node(value))

    for i in xrange(len(nodeObjectsList)-1):
        nodeObjectsList[i].setNextNode(nodeObjectsList[i+1])

    #set last object to make a circular ref
    nodeObjectsList[-1].setNextNode(nodeObjectsList[3])

    printChain(nodeObjectsList[0])

    
    
if __name__ == '__main__':
    main()

