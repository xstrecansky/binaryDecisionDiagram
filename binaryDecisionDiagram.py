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
#Trida binarneho rozhodovacieho diagramu
class BDD(object):
    def __init__(self, poradie, fList):
        self.root = Node(fList, 1)
        self.values = 1
        self.poradie = poradie
    def incValues(self):
        self.values += 1
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
            tempLeft = leftString(root.value,poradie[0])
            tempRight = rightString(root.value,poradie[0])
            #Pripad kedy je root rovnaky s pravou a lavou stranou
            #Prejdeme na dalsiu instanciu
            if(root.value == tempLeft and root.value == tempRight):
                return root
                #Musime sa nachadzat na konci BDD -> vratime None
                if ('1' or '0') in root.value:
                    return root
                #Inak prejdeme poradie a lavy a pravy prvok
                poradie = poradie[1:]
                tempLeft = leftString(tempLeft, poradie[0])
                tempRight = rightString(tempRight, poradie[0])
            #Ak mame pravu a lavu stranu rovnaku 
            if tempLeft == tempRight:
                answerRoot = checkForDuplicates(self.root, tempLeft, None)
                #Ak sa hodnota uz nachadza v strome iba ju nastavime ako lavy prvok
                if answerRoot:
                    root.left = answerRoot
                else:
                    #Ak sa v nom nachadza 1 alebo 0 -> nepokracujeme v nasledovnom vytvarani
                    if ('1' or '0') in tempLeft:
                        root.left = Node(tempLeft, self.incValues())
                    else:
                        root.left = Node(tempLeft, self.incValues())
                        root.left = self.BDD_create(root.left, poradie[1:])
                root.right = root.left
                return root
            else:
                #Obycajny pripad, najprv sa pozrieme na lavy prvok
                answerRoot = checkForDuplicates(self.root, tempLeft, None)
                #Ak sa hodnota uz nachadza v strome iba ju nastavime ako lavy prvok
                if answerRoot:
                    root.left = answerRoot
                else:
                    #Ak sa v nom nachadza 1 alebo 0 -> nepokracujeme v nasledovnom vytvarani
                    if ('1' or '0') in tempLeft:
                        root.left = Node(tempLeft, self.incValues())
                    else:
                        root.left = Node(tempLeft, self.incValues())
                        root.left = self.BDD_create(root.left, poradie[1:])
                #Obycajny pripad, najprv sa pozrieme na pravy prvok
                answerLeftRoot = checkForDuplicates(self.root, tempRight, None)
                if answerLeftRoot:
                    root.right = answerLeftRoot
                else:
                    #Ak sa v nom nachadza 1 alebo 0 -> nepokracujeme v nasledovnom vytvarani
                    if ('1' or '0') in tempRight:
                        root.right = Node(tempRight, self.incValues())
                    else:
                        root.right = Node(tempRight, self.incValues())
                        root.right = self.BDD_create(root.right, poradie[1:])
        return root
    #Metoda pre vypis vysledku
    def BDD_use(self, combination):
        tempRoot = self.root
        for letter in combination:
            if not tempRoot.right:
                print(tempRoot.value)
                return
            if letter =='0':
                #Pozrieme sa ci vobec existuje lavy prvok kezde
                #v pripade rovnakeho praveho a laveho prvku ulozime iba pravy
                tempRoot = tempRoot.left
            elif letter =='1':
                tempRoot = tempRoot.right
            #Chyba
            else:
                print('-1')
                return
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
#Rekurzivne prejdeme vsetky, prvky a ak najdeme vstupnu hodnotu, vratime nodu
def checkForDuplicates(root, value, temp):
    if temp:
        return temp
    if root:
        if value == root.value:
            temp = root
        if root.left:
            temp = checkForDuplicates(root.left, value, temp)
        if root.right:
            temp = checkForDuplicates(root.right, value, temp)
        return temp
#Vypisanie stromu 2D z internetu
#https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
def print2DUtil(root, space):
    COUNT = [10]
    if (root == None):
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
    poradie = input("Zadaj poradie:\n")

    bddroot = BDD(poradie, fList)
    bddroot.root = bddroot.BDD_create(bddroot.root, poradie)
    bddroot.print2D()
    
    #Testujeme pre neoptimalizovany diagram
    #bad = BDD(poradie, fList)
    #bad.root = bad.BDD_createWithDuplicates(bad.root, poradie)
    #bad.print2D()
    
    kombinacia = input('Zadaj kombinaciu:\n')
    bddroot.BDD_use(kombinacia)