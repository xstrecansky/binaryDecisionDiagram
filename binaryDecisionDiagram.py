#Trieda jednej nody
from operator import le


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
    #Funkcia na vytvorenie binarneho diagramu
    def BDD_create(self, fList, poradie):
        if len(fList)>2:
            self.value = fList
            self.left = self.BDD_create((leftString(fList,poradie[0])), (fList[1:]))
            self.right = self.BDD_create((rightString(fList,poradie[0])), (fList[1:]))
            return self
        return self
    #Funkcia na zistenie hodnoty podla vstupu
    def BDD_use(self, vstup):
        for item in vstup:
            if item == '0':
                self = self.left
            if item == '1':
                self = self.right
        return self.value
    #Inorder vypisanie stromu
    def inorder(self, root): 
        if(root is None): 
            return
        self.inorder(self.left) 
        print(self.value,end = ' ') 
        self.inorder(self.right)
#Trida binarneho rozhodovacieho diagramu
class BDD:
    def __init__(self, poradie):
        self.root = Node()
        self.values = 0
        self.poradie = poradie
#Vypise vsetky zaporne prvky
def leftString(fList, letter):
    nonA = []
    for item in fList:
        new = item.replace('!'+letter,'')
        if item.find('!'+letter)==0:
            nonA.append(new)
        if item.find(letter)==-1:
            nonA.append(item)
    if '' in nonA:
        nonA.remove('')
    if len(nonA)==0:
        nonA.append('0')
        return nonA
    return list(dict.fromkeys(nonA))
#Vypise vsetky kladne prvky
def rightString(fList, letter):
    posA = []
    for item in fList:
        new = item.replace(letter,'')
        if item.find(letter)==0 and item[0]!='!':
            posA.append(new)
        if item.find(letter)==-1:
            posA.append(item)
    if '' in posA:
        posA.remove('')
    if len(posA)==0:
        posA.append('1')
        return posA
    return list(dict.fromkeys(posA))
#Zadavame v tvare AB+CE+!AEF...
bfunkcia = input('Zadaj funkciu v DNF:\n')
fList = bfunkcia.split('+')
#Zadavame v tvare ABCDE...
poradie = input('Zadaj poraadie fList:\n')
left = fList
right = fList
print(fList)
for element in range(0, len(poradie)):
    left = leftString(left, poradie[element])
    right = rightString(right, poradie[element])
    print(left)
    print(right)

