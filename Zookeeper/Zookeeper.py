N = 4
L = 4
goalAchieved = False

class Node:
        def __init__(self, parentList, position,countLizardRemaining):
                self.parentList = parentList
                self.position = position
                self.countLizardRemaining = countLizardRemaining
      

        def isInitialNode(self):
                if (len(self.position) == 0 and len(self.parentList) == 0):
                        return True
                else:
                        return False

        def displayNodeData(self):
                print(self.parentList)
                print(self.position)
                print(self.countLizardRemaining)

initial = Node([],[],L)

class stack(object):
    items = []
    def _init_(self):
            self.items = []

    def isStackEmpty(self):
            if len(self.items) == 0:
                    return True
            else:
                    return False     
       
    def push(self,item):
            self.items.append(item)

    def pop(self):
            return self.items.pop()
        
    def size(self):
            return len(self.items)

    def displayStackItems(self):
            for item in self.items:
                    print(item)

        
        

frontier = stack()
frontier.push(initial)

def rowValidity(row, node):
        flag1 = True
        flag2 = True
        if (node.isInitialNode() == False):
                if row == node.position[0]:
                        return False
                print(node.parentList)
                for pos in node.parentList:
                        print(pos)
                        if row == pos[0]:
                                flag1 = False
                                break

        return flag1
        
def colValidity(col, node):
        flag1 = True
        #flag2 = True
        if (node.isInitialNode() == False):
                if col == node.position[1]:
                        return False
                for pos in node.parentList:
                        if col == pos[1]:
                                flag1 = False
                                break

        return flag1

def diagValidity(row,col,node):
        flagCD = True
        flagMD = True
        if (node.isInitialNode() == False):
                diff = row - col
                if (diff == (node.position[0] - node.position[1])) or ((row + col) == (node.position[0] + node.position[1])):
                        return False
                for pos in node.parentList:
                        if(diff == (pos[0] - pos[1])):
                                flagCD = False
                                break
                        if((row + col) == (pos[0] + pos[1])):
                                flagMD = False
                                break
                 
        return (flagCD and flagMD)
        



def actionFunc(node):
        childrenList = []
        
        newParentList = node.parentList
        #if (len(newParentList) == 0 and len(node.position) == 0) == False:
         #       newParentList.append(node.position)
        for row in range(0,N):
                for col in range(0,N):
                        
                        if(rowValidity(row,node) and colValidity(col,node) and diagValidity(row,col,node) == True):
                               # if node.isInitialNode() == True:
                                #        childrenList.append(Node([],[row,col],node.countLizardRemaining-1))
                                #elif len(node.parentList) == 0:
                                #        childrenList.append(Node([],[row,col],node.countLizardRemaining - 1))
                               # else:
                                        newList = []
                                        for element in newParentList:
                                                newList.append(element)
                                        if len(node.position) != 0:
                                                newList.append(node.position)
                                        childrenList.append(Node(newList,[row,col],node.countLizardRemaining - 1))
                                        
        return childrenList


while(frontier.isStackEmpty() == False):
        currentNode = frontier.pop()        
        if(currentNode.countLizardRemaining == 0):
                goalAchieved = True
                break
        else:
                #childrenList = []
                childrenList = actionFunc(currentNode)
                for child in reversed(childrenList):
                        frontier.push(child)

if goalAchieved == True:
        currentNode.displayNodeData()
else:
        print('Failure')
                        






        
                        
             
                                         
   
    







        

    





