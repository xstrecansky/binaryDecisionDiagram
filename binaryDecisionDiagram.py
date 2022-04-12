COUNT = [10]
#Trieda jednej nody
class Node(object):
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
#Trida binarneho rozhodovacieho diagramu
class BDD(object):
    def __init__(self, poradie, fList):
        self.root = Node(fList)
        self.values = 0
        self.poradie = poradie
    def BDD_use(self, combination):
        tempRoot = self.root
        for letter in combination:
            if letter =='0':
                #Pozrieme sa ci vobec existuje lavy prvok kezde
                #v pripade rovnakeho praveho a laveho prvku ulozime iba pravy
                if tempRoot.left:
                    tempRoot = tempRoot.left
            else:
                tempRoot = tempRoot.right
        print(tempRoot.value)
#Vypise vsetky zaporne prvky
def leftString(fList, letter):
    #Pripad kedy mame !C v lavej strane -> vzdy 1
    nonA = []
    if '!'+letter in fList:
        nonA.append('1')
        return nonA
    else:
        for item in fList:
            #Pripad kedy sa nachadza vo funkcii !C
            if item.find('!'+letter)==0:
                #Odstranime pismeno a pridame do listu
                new = item.replace('!'+letter,'')
                nonA.append(new)
                #Ak sa nenachadza !C vo funkcii pridame
            if item.find(letter)==-1:
                nonA.append(item)
        if '' in nonA:
            nonA.remove('')
        if len(nonA)==0:
            nonA.append('0')
            return nonA
        #Odstranime duplikaty
        return list(dict.fromkeys(nonA))
#Vypise vsetky kladne prvky
def rightString(fList, letter):
    #Pripad kedy mame C v pravej strane -> vzdy 1
    posA = []
    if letter in fList:
        posA.append('1')
        return posA
    else:
        for item in fList:
            #Pripad kedy sa nachadza vo funkcii C
            if item.find(letter)==0 and item[0]!='!':
                #Odstranime pismeno a pridame do listu
                new = item.replace(letter,'')
                posA.append(new)
            #Ak sa nenachadza C vo funkcii pridame
            if item.find(letter)==-1:
                posA.append(item)
        if '' in posA:
            posA.remove('')
        if len(posA)==0:
            posA.append('1')
            return posA
        #Odstranime duplikaty
        return list(dict.fromkeys(posA))
#Vypisanie stromu 2D
#Skopirovane z internetu
#https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
def print2DUtil(root, space) :
    if (root == None) :
        return
    space += COUNT[0]
    print2DUtil(root.right, space)
    print()
    for i in range(COUNT[0], space):
        print(end = " ")
    print(root.value)
    print2DUtil(root.left, space)
def print2D(root):
    print2DUtil(root, 0)
#Funkcia na vytvorenie binarneho diagramu
def BDD_create(root, poradie):
    if poradie:
        if '0' not in root.value and '1' not in root.value:
            tempLeftString = leftString(root.value,poradie[0])
            tempRightString = rightString(root.value,poradie[0])
            #Ak nenajdeme duplikat v pravej a lavej strane
            if tempLeftString != tempRightString:
                root.left = Node(tempLeftString)
                root.left = BDD_create(root.left, poradie[1:])
            root.right = Node(tempRightString) 
            root.right = BDD_create(root.right, poradie[1:])
        return root
    return None
#Zadavame v tvare A!C+ABC+!AB+!BC
while(True):
    bfunkcia = input('Zadaj funkciu v DNF:\n')
    fList = bfunkcia.split('+')
    #Zadavame v tvare ABCDE
    poradie = input('Zadaj poradie:\n')
    poradie = poradie + " "
    bddroot = BDD(poradie, fList)
    bddroot.root = BDD_create(bddroot.root, poradie)
    print2D(bddroot.root)
    kombinacia = input('Zadaj kombinaciu:\n')
    bddroot.BDD_use(kombinacia)
