import time
s = time.time()
import sys
import copy
import string
input = open('input7.txt', 'r')
myList = []
for line in input:
    myList.append(line.rstrip())
for item in myList:
    if item == '':
        myList.remove(item)
row = int(myList[0])
col = row
N = int(myList[1])
t = float(myList[2])
graph = []
for item in range(3, len(myList)):
    temp = []
    for k in range(0, row):
        if myList[item][k] == '*':
            temp.append('*')
        else:
            temp.append(int(myList[item][k]))
    graph.append(temp)

result = 0
position = []
L = 2
#Connected Components Algorithm using DFS


def isSafe(i,j,explored,fruitType):
    return(i >=0 and i < row and j >= 0 and j < col and not explored[i][j] and graph[i][j] == fruitType)

def DFS(i,j,explored,fruitType,cluster):
    rowPos = [0,-1,0,1]
    colPos = [-1,0,1,0]
    explored[i][j] = True
    for pos in range(4):
        if isSafe(i + rowPos[pos], j + colPos[pos], explored,fruitType):
            cluster.append([i + rowPos[pos], j + colPos[pos]])
            DFS(i + rowPos[pos], j + colPos[pos], explored,fruitType,cluster)
    return cluster

def countConnectedFruits(row,col,graph):
    hashMap = {}
    explored = [[False for j in range(0,col)]for i in range(0,row)]
    for i in range(0,row):
        for j in range(0,col):
            if explored[i][j] == False and graph[i][j] != '*':
                totalClusters = []
                fruitType = graph[i][j]
                totalClusters = (DFS(i,j,explored,fruitType,[[i,j]]))
                if (len(totalClusters)!=0):
                    if fruitType in hashMap:
                        hashMap[fruitType].append(totalClusters)
                    else:
                        hashMap[fruitType] = [totalClusters]
    return hashMap



#Pick elements : Selects the cluster to be replaced by '*'
def pickElement(cell,fruitType,hashMap):
    for element in hashMap[fruitType]:
        for item in element:
            if cell == item:
                return(element)



#Drop Element : Replaces the cluster with '*'
def dropElement(element,graph):
    newGraph = copy.deepcopy(graph)
    for item in element:
        #assert isinstance(newGraph, object)
        newGraph[item[0]][item[1]] = '*'
    return newGraph

#element = pickElement([3,2],0)
#starredGraph = dropElement(element)


def star(omatrix):
    matrix = copy.deepcopy(omatrix)
    for j in range(0,col):
        r = row - 1
        i = row - 1
        while(i >= 0):
            if matrix[i][j] == '*':
                i -= 1
            elif not(matrix[i][j]) == '*' and matrix[r][j] == '*':
                temp = matrix[i][j]
                matrix[i][j] = matrix[r][j]
                matrix[r][j] = temp
                i -= 1
                r -= 1
            else:
                i -= 1
                r -= 1
    return matrix

#Evaluation Function : returns the difference between the two players scores
def evalFunc(player1,player2):
    return player1 - player2

def allStar(matrix):
    flag = True
    for i in range(0,row):
        for j in range(0,col):
            if not(matrix[i][j] == '*'):
                return False
    return flag

def convert(position):
    r = range(1,27)
    c = list(string.ascii_uppercase)
    h = r[position[0]]
    v = c[position[1]]
    return v,h

#MinMax Function with Alpha Beta Pruning
def minVal(state,level,alpha,beta,player1,player2):
    if(level == L or allStar(state)):
        return evalFunc(player1,player2)
    hashmap = countConnectedFruits(row, col, state)
    for key in hashmap:
        for element in hashmap[key]:
            dropped = copy.deepcopy(dropElement(element,state))
            replaceStar = copy.deepcopy(star(dropped))
            player2New = player2 + pow(len(element),2)
            beta = min(beta,maxVal(replaceStar,level+1,alpha,beta,player1,player2New,False))
            if(beta <= alpha):
                return alpha
    return beta




def maxVal(state,level,alpha,beta,player1,player2,val):
    if(level == L or allStar(state) ):
        return evalFunc(player1,player2)
    hashmap = countConnectedFruits(len(state), len(state[0]), state)
    for key in hashmap:
        for element in hashmap[key]:
            dropped = copy.deepcopy(dropElement(element,state))
            replaceStar = copy.deepcopy(star(dropped))
            previous = copy.deepcopy(alpha)
            player1New = player1 + pow(len(element),2)
            alpha = max(alpha,minVal(replaceStar,level+1,alpha,beta,player1New,player2))
            if (not(alpha == previous) and val):
                global result
                result = replaceStar
                global position
                position = element[0]
                if(alpha >= beta):
                    return beta
    return alpha


maxVal(graph,0,-sys.maxsize - 1,sys.maxsize,0,0,True)
x = convert(position)
f = open('output.txt','w')
f.write(x[0])
f.write('%d' % x[1])
f.write('\n')
f.writelines(''.join(str(j) for j in i) + '\n' for i in result)
f.close()

e = time.time()
print(e-s)











