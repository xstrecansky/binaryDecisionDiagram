#Trieda jednej nody
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
#Vypise vsetky zaporne prvky
def leftString(funkcie):
    nonA = ""
    for item in funkcie:
        if item.find("!A")==0:
            if len(item)==2:
                item.replace("!A",'')
            else:
                item.replace("!A.",'')
            nonA = nonA + item + ' ' 
    if item.find("A")==-1:
        nonA = nonA + item + ' '   
    return nonA
#Vypise vsetky kladne prvky
def rightString(funkcie):
    posA = ""
    for item in funkcie:
        if item.find("A")==0:
            if len(item)==1:
                item.replace('A','')
            else:
                item.replace('A.','')
            posA = posA + item + ' '
        if item.find("A")==-1:
            posA = posA + item + ' '
    return posA

bfunkcia = input('Zadaj funkciu v DNF:\n')
funkcie = bfunkcia.split('+')
#poradie = input('Zadaj poraadie funkcie:\n')

print(leftString(funkcie) + '\n' + rightString(funkcie))
