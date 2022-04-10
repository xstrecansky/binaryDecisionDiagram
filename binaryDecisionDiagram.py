#Trieda jednej nody
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
#Trida binarneho rozhodovacieho diagramu
class BDD:
    def __init__(self) -> None:
        pass
#Vypise vsetky zaporne prvky
def leftString(fList, letter):
    nonA = ""
    for item in fList:
        if len(item)==2:
            new = item.replace('!'+letter,'')
        else:
            new = item.replace('!'+letter+'.','')
        if item.find('!'+letter)==0:
            nonA = nonA + new + ' ' 
        if item.find(letter)==-1:
            nonA = nonA + item + ' '   
    return nonA
#Vypise vsetky kladne prvky
def rightString(fList, letter):
    posA = ""
    for item in fList:
        if len(item)==1:
            new = item.replace(letter,'')
        else:
            new = item.replace(letter+'.','')
        if item.find(letter)==0:
            posA = posA + new + ' '
        if item.find(letter)==-1:
            posA = posA + item + ' '
    return posA

bfunkcia = input('Zadaj funkciu v DNF:\n')
fList = bfunkcia.split('+')
poradie = input('Zadaj poraadie fList:\n')

print(leftString(fList,poradie[0]) + '\n' + rightString(fList,poradie[0]))
