def standardization(KB):                 ##Standardizing the the common named varaibles used in different logical statements
    for i,s in enumerate(KB):
        newS = ''
        splitKB = KB[i].split(' | ')
        for n,item in enumerate(splitKB):
            pos = item.find('(')
            temp = item[0:pos] + '('
            a = item[pos+1:len(item)-1].split(',')
            l = len(a)
            for k in range(0,l):
                if len(a[k]) == 1 and type(a[k])==str:
                    a[k] = a[k] + str(i)
                if k<len(a)-1:
                    temp = temp+ a[k]+','
                else:
                    temp = temp + a[k] + ')'
            if n == 0:
                newS = temp
            elif n<=len(splitKB) - 1:
                newS = newS + ' | ' + temp
            else:
                newS = newS + temp
        KB[i] = newS

    return KB


## Predicate object definition
class Predicate:
    def __init__(self,s):
        k = s.find('(')
        self.predicateName = s[0:k]
        self.arguments = s[k+1:len(s) - 1].split(',')

def formPredicate(p):
    fp = p.predicateName + '('
    if len(p.arguments) == 1:
        fp = fp + p.arguments[0] + ')'
    else:
        for i in range(0,len(p.arguments)-1):
            fp = fp + p.arguments[i] + ','
            fp = fp + p.arguments[len(p.arguments) - 1] + ')'
    return fp

def separate(c):
    p = []
    temp = c.split(' | ')
    for i in temp:
        p.append(Predicate(i))
    return p

def conjunction(p1,p2):
    fpNew = []
    for p in p1:
        fpNew.append(formPredicate(p))
    for p in p2:
        fpNew.append(formPredicate(p))
    unique = list(set(fpNew))
    newClause = ''
    for i in range (0, len(unique) - 1):
        newClause = newClause + unique[i] + ' | '
    newClause = newClause + unique[len(unique) - 1]
    return newClause


## Substitute after Unification

def substitute(sub,predicate):
    for i in range(0,len(predicate.arguments)):
        for key in sub:
            if predicate.arguments[i] == key:
                predicate.arguments[i] = sub[key]
    return predicate
def totalSubstitution(sub,p1):
    for i in range(0,len(p1)):
        p1[i] = substitute(sub,p1[i])
    return p1

## UNIFICATION
def unifyVar(var,x,theta):
    if var in theta:
        return unify(theta[var],x,theta)
    elif x in theta:
        return unify(var,theta[x],theta)
    else:
        theta.update({var:x})
        return theta

def unify(x, y, theta):
    if (theta == None) or (x == y):
        return theta
    elif type(x) == str and x.isalnum():
        return unifyVar(x,y,theta)
    elif type(y) == str and y.isalnum():
        return unifyVar(y,x,theta)
    elif type(x) == list and type(y) == list:
        return unify(x[1:],y[1:],unify(x[0],y[0],theta))
    else:
        return None



## Resolution Function

def folResolve(c1,c2):
    p1 = separate(c1)
    p2 = separate(c2)
    flag = False
    clauses = []
    for index1,predicate1 in enumerate(p1):
        for index2,predicate2 in enumerate(p2):
            if predicate1.predicateName == '~' + predicate2.predicateName or predicate2.predicateName == '~' + predicate1.predicateName:

                sub = unify(predicate1.arguments,predicate2.arguments,{})
                if not(sub == None):
                    flag = True
                    newp1 = deepcopy(p1)
                    newp2 = deepcopy(p2)
                    #print(newp1[0].predicateName,newp1[0].arguments,predicate1.predicateName,predicate1.arguments)
                    #print(newp2[0].predicateName,predicate2.predicateName,predicate2.arguments)
                    newp1.remove(newp1[index1])
                    newp2.remove(newp2[index2])


                    newp1 = totalSubstitution(sub, newp1)
                    newp2 = totalSubstitution(sub, newp2)

                    if len(newp1) == 0 and len(newp2) == 0:
                        return clauses
                    clauses.append(conjunction(newp1,newp2))
    if flag == True:
        return clauses
    else:
        return ['Dont Append']

def folResolution(tempKB,q):
    clauses = deepcopy(tempKB)
    new = set([])
    while True:
        for i in range(0,len(clauses) - 1):
            for j in range(i+1,len(clauses)):
                resolvents = folResolve(clauses[i],clauses[j])
                print(resolvents,clauses[i],clauses[j])
                if len(resolvents) == 0:
                    if q == clauses[i] or q == clauses[j]:
                        flag = True
                        return True
                elif resolvents == ['Dont Append']:
                    #flag = False
                    continue
                else:
                    #flag = True
                    new.update(set(resolvents))
        if new.issubset(set(clauses)) or len(new)==0:
            return False
        else:
            for item in new:
                if item not in clauses:
                    clauses = [item] + clauses
            if (sys.getsizeof(clauses) > 10000):
                return False

from copy import deepcopy
import sys
input = open('input.txt', 'r')
myList = []
for line in input:
    myList.append(line.rstrip())
numQuery = int(myList[0])
Query = []
for i in range(1, numQuery + 1):
    if myList[i][0] == '~':
        Query.append(myList[i][1:len(myList[i])])
    else:
        Query.append('~'+myList[i])

KB = []

numClauses = int(myList[numQuery+1])
for i in range(numQuery+2,numQuery+numClauses+2):
    KB.append(myList[i])
KB = standardization(KB)
f = open('output.txt','w')
for q in Query:
    KB = [q] + KB
    flag = folResolution(KB,q)
    if flag == False:
        f.write('FALSE')
        f.write('\n')
        KB.remove(q)
    else:
        f.write('TRUE')
        f.write('\n')

