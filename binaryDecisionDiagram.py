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
#Vypise vsetky zaporne prvky
def leftString(fList, letter):
    #Pripad kedy mame !C v lavej strane -> vzdy 1
    if '!'+letter in fList:
        return '1'
    else:
        nonA = []
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
    if letter in fList:
        return '1'
    else:
        posA = []
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
#Preorder vypisanie stromu
def preorder(root): 
    if root:
        print(root.value)
        preorder(root.left)
        preorder(root.right)
    return root
#Funkcia na vytvorenie binarneho diagramu
def BDD_create(root, poradie):
    if len(poradie)==0:
        return None
    root.left = Node((leftString(root.value,poradie[0])))
    root.right = Node((rightString(root.value,poradie[0])))
    root.left = BDD_create(root.left, poradie[1:])
    root.right = BDD_create(root.right, poradie[1:])
    return root
#Zadavame v tvare A!C+ABC+!AB+!BC
#bfunkcia = input('Zadaj funkciu v DNF:\n')
bfunkcia = "A!C+ABC+!AB+!BC"
fList = bfunkcia.split('+')
#Zadavame v tvare ABCDE
#poradie = input('Zadaj poraadie fList:\n')
poradie = "ABC"
bddroot = BDD(poradie, fList)
bddroot.root = BDD_create(bddroot.root, poradie)
preorder(bddroot.root)