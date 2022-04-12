COUNT = [10]
#Trieda jednej nody
class Node(object):
    def __init__(self, value, id):
        self.left = None
        self.right = None
        self.value = value
        #Unikatne id na pocitanie poctu prvkov
        self.id = id
    #Inorder binary tree traversal
    def inorder(self):
        if self.left:
            self.left.inorder()
        print(self.value)
        if self.right:
            self.right.inorder()
    #Rekurzivne prejdeme vsetky, prvky a ak najdeme vstupnu hodnotu, vratime nodu
    def checkForDuplicates(self, value):
        if value == self.value:
            return self
        if self.left:
            return self.left.checkForDuplicates(value)
        if self.right:
            return self.right.checkForDuplicates(value)
        return None

#Trida binarneho rozhodovacieho diagramu
class BDD(object):
    def __init__(self, poradie, fList):
        self.root = Node(fList, 1)
        self.values = 1
        self.poradie = poradie
    def incValues(self):
        self.values += 1
        return self.values
    def getValues(self):
        return self.values
    #Funckia na vytvorenie binarneho diagramu
    #Bez oplimalizacie a odstranenia duplikatov
    def BDD_createWithDuplicates(self, root, poradie):
        if poradie:
            root.left = Node(leftString(root.value,poradie[0]), self.incValues())
            root.left = self.BDD_createWithDuplicates(root.left, poradie[1:])
            root.right = Node(rightString(root.value,poradie[0]), self.incValues())
            root.right = self.BDD_createWithDuplicates(root.right, poradie[1:])
            return root
        return None
    #Funkcia na vytvorenie binarneho diagramu
    def BDD_create(self, root, poradie):
        if poradie:
            #TODO:
            if '1' not in root.value and '0' not in root.value:
                tempLeftString = leftString(root.value,poradie[0])
                tempRightString = rightString(root.value,poradie[0])
                if root.checkForDuplicates(tempLeftString) == None:
                    root.left = Node(tempLeftString, self.incValues())
                    root.left = self.BDD_create(root.left, poradie[1:])
                #Ak najdeme duplikat, nastavime ho ako smernik na lavy prvok
                else:
                    root.left = root.checkForDuplicates(tempLeftString)
                if root.checkForDuplicates(tempRightString) == None:
                    root.right = Node(tempRightString, self.incValues())
                    root.right = self.BDD_create(root.right, poradie[1:])
                #Ak najdeme duplikat, nastavime ho ako smernik na pravy prvok
                else:
                    root.right = root.checkForDuplicates(tempRightString)
            return root
        return None
    #Metoda pre vypis vysledku
    def BDD_use(self, combination):
        tempRoot = self.root
        for letter in combination:
            if letter =='0':
                #Pozrieme sa ci vobec existuje lavy prvok kezde
                #v pripade rovnakeho praveho a laveho prvku ulozime iba pravy
                if tempRoot.left:
                    tempRoot = tempRoot.left
                else:
                    if tempRoot.right:
                        tempRoot = tempRoot.right
            else:
                tempRoot = tempRoot.right
        print(tempRoot.value)
    #Spusti vypisanie 2D prvkov
    def print2D(self):
        print2DUtil(self.root, 0)
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
#Vypisanie stromu 2D z internetu
#https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
def print2DUtil(root, space) :
    if (root == None) :
        return
    space += COUNT[0]
    print2DUtil(root.right, space)
    print()
    for i in range(COUNT[0], space):
        print(end = " ")
    print(root.value, end = " ,id: ")
    print(str(root.id))
    print2DUtil(root.left, space)
#Zadavame v tvare A!C+ABC+!AB+!BC
while(True):
    fList = input('Zadaj funkciu v DNF:\n').split('+')
    #Zadavame v tvare ABCDE
    poradie = input('Zadaj poradie:\n')+ " "
    #Testujeme pre optimalizovy diagram
    bddroot = BDD(poradie, fList)
    bddroot.root = bddroot.BDD_create(bddroot.root, poradie)
    bddroot.print2D()
    print(bddroot.getValues())
    """
    print("--------------------------------------------------------------------------------\n")
    #Testujeme pre neoptimalizovany diagram
    bad = BDD(poradie, fList)
    bad.root = bad.BDD_createWithDuplicates(bad.root, poradie)
    bad.print2D()
    """
    kombinacia = input('Zadaj kombinaciu:\n')
    bddroot.BDD_use(kombinacia)