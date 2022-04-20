import random


# Trieda jednej nody
class Node(object):
    def __init__(self, value, i):
        self.left = None
        self.right = None
        self.value = value
        # Unikatne id na pocitanie poctu prvkov
        self.id = i

    # Kod prezaty z https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        if self.right is None and self.left is None:
            line = "%s" % self.value + ",id:" + str(self.id)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = "%s" % self.value + ",id:" + str(self.id)
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = "%s" % self.value + ",id:" + str(self.id)
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = "%s" % self.value + ",id:" + str(self.id)
        u = len(s)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
        second_line = (
            x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "
        )
        if p < q:
            left += [n * " "] * (q - p)
        elif q < p:
            right += [m * " "] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * " " + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


# Trida binarneho rozhodovacieho diagramu
class BDD(object):
    def __init__(self, poradie, fList):
        self.root = Node(fList, 1)
        self.values = 1
        self.poradie = poradie
        self.pocetPremennych = len(poradie)

    def incValues(self, i):
        self.values += i
        return self.values

    # Vypiseme vsetky hodnoty pomocou BDD_use
    def everynumber(self, text, size, array):
        if len(text) <= size:
            self.everynumber(text + "0", size, array)
            if len(text) == size:
                array.append(self.BDD_use(text))
            self.everynumber(text + "1", size, array)
        if len(text) == size and "0" not in text:
            print(array)
            return

    # Funckia na vytvorenie binarneho diagramu
    # Bez oplimalizacie a odstranenia duplikatov
    def BDD_createWithDuplicates(self, root, poradie):
        if poradie:
            root.left = Node(leftString(root.value, poradie[0]), self.incValues(1))
            root.left = self.BDD_createWithDuplicates(root.left, poradie[1:])
            root.right = Node(rightString(root.value, poradie[0]), self.incValues(1))
            root.right = self.BDD_createWithDuplicates(root.right, poradie[1:])
            return root
        return root

    # Vyhladavanie pre neoptimalizovany BDD
    def badBDD_use(self, combination):
        tempRoot = self.root
        for letter in combination:
            if letter == "0":
                tempRoot = tempRoot.left
            elif letter == "1":
                tempRoot = tempRoot.right
            else:
                return "-1"
        if "1" in tempRoot.value:
            return "1"
        return "0"

    # Funkcia na vytvorenie binarneho diagramu
    def BDD_create(self, root, poradie, bfunkcia):
        if poradie:
            tempLeft = leftString(bfunkcia, poradie[0])
            tempRight = rightString(bfunkcia, poradie[0])
            # Pripad kedy je root rovnaky s pravou a lavou stranou
            # Prejdeme na dalsiu instanciu
            if root.value == tempLeft and root.value == tempRight:
                root = self.BDD_create(root, poradie[1:], root.value)
            # Ak mame pravu a lavu stranu rovnaku
            elif tempLeft == tempRight:
                answerRoot = checkForDuplicates(self.root, tempLeft, None)
                # Ak sa hodnota uz nachadza v strome iba ju nastavime ako lavy prvok
                if answerRoot:
                    root.left = answerRoot
                else:
                    # Ak sa v nom nachadza 1 alebo 0 -> nepokracujeme v nasledovnom vytvarani
                    if "1" in tempLeft or "0" in tempLeft:
                        root.left = Node(tempLeft, self.incValues(1))
                    else:
                        root.left = Node(tempLeft, self.incValues(1))
                        root.left = self.BDD_create(root.left, poradie[1:], tempLeft)
                root.right = root.left
            else:
                # Obycajny pripad, najprv sa pozrieme na lavy prvok
                answerRoot = checkForDuplicates(self.root, tempLeft, None)
                # Ak sa hodnota uz nachadza v strome iba ju nastavime ako lavy prvok
                if answerRoot:
                    root.left = answerRoot
                else:
                    # Ak sa v nom nachadza 1 alebo 0 -> nepokracujeme v nasledovnom vytvarani
                    if "1" in tempLeft or "0" in tempLeft:
                        root.left = Node(tempLeft, self.incValues(1))
                    else:
                        root.left = Node(tempLeft, self.incValues(1))
                        root.left = self.BDD_create(root.left, poradie[1:], tempLeft)
                # Obycajny pripad, najprv sa pozrieme na pravy prvok
                answerLeftRoot = checkForDuplicates(self.root, tempRight, None)
                if answerLeftRoot:
                    root.right = answerLeftRoot
                else:
                    # Ak sa v nom nachadza 1 alebo 0 -> nepokracujeme v nasledovnom vytvarani
                    if "1" in tempRight or "0" in tempRight:
                        root.right = Node(tempRight, self.incValues(1))
                    else:
                        root.right = Node(tempRight, self.incValues(1))
                        root.right = self.BDD_create(root.right, poradie[1:], tempRight)
            # Na konci sa pozrieme na rovnake hodnoty v jednej node
            # Ak sa obe rovnaju 1 alebo 0 nemusime zapisovat aktualnu nodu
            if "0" not in root.value and "1" not in root.value:
                if root.left.value == root.right.value:
                    if "0" in root.left.value or "1" in root.left.value:
                        root = root.left
                        self.incValues(-1)
        return root

    # Metoda pre vypis vysledku
    def BDD_use(self, combination):
        tempRoot = self.root
        for i in range(0, len(combination)):
            number = combination[i]
            if "1" in tempRoot.value:
                return "1"
            if "0" in tempRoot.value:
                return "0"
            if self.poradie[i] in listToString(tempRoot.value):
                if number == "0":
                    tempRoot = tempRoot.left
                elif number == "1":
                    tempRoot = tempRoot.right
                else:
                    return "-1"
            else:
                continue
        if "1" in tempRoot.value:
            return "1"
        return "0"

    # Spusti vypisanie 2D prvkov
    def print2D(self):
        print2DUtil(self.root, 0)


# Vypise vsetky zaporne prvky
def leftString(fList, letter):
    # Pripad kedy mame !C v lavej strane -> vzdy 1
    nonA = []
    if "!" + letter in fList:
        nonA.append("1")
        return nonA
    else:
        for item in fList:
            # Pripad kedy sa nachadza vo funkcii !C
            if item.find("!" + letter) == 0:
                # Odstranime pismeno a pridame do listu
                new = item.replace("!" + letter, "")
                nonA.append(new)
                # Ak sa nenachadza !C vo funkcii pridame
            if item.find(letter) == -1:
                nonA.append(item)
        if "" in nonA:
            nonA.remove("")
        if len(nonA) == 0:
            nonA.append("0")
            return nonA
        # Odstranime duplikaty
        return list(dict.fromkeys(nonA))


# Vypise vsetky kladne prvky
def rightString(fList, letter):
    # Pripad kedy mame C v pravej strane -> vzdy 1
    posA = []
    if letter in fList:
        posA.append("1")
        return posA
    else:
        for item in fList:
            if item.find("!" + letter) == 0:
                posA.append("")
                continue
            # Pripad kedy sa nachadza vo funkcii C
            if item.find(letter) == 0 and item[0] != "!":
                # Odstranime pismeno a pridame do listu
                new = item.replace(letter, "")
                posA.append(new)
            # Ak sa nenachadza C vo funkcii pridame
            if item.find(letter) == -1:
                posA.append(item)
        if "" in posA:
            posA.remove("")
        if len(posA) == 0:
            posA.append("0")
            return posA
        # Odstranime duplikaty
        return list(dict.fromkeys(posA))


# Rekurzivne prejdeme vsetky, prvky a ak najdeme vstupnu hodnotu, vratime nodu
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


# Vypisanie stromu 2D z internetu
# https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
def print2DUtil(root, space):
    COUNT = [10]
    if root == None:
        return
    space += COUNT[0]
    print2DUtil(root.right, space)
    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    print(root.value, end=" ,id: ")
    print(str(root.id))
    print2DUtil(root.left, space)


# Metoda na porovnanie hodnot dvoch BDD
def compareBDD(bdd1, bdd2, text, size):
    if len(text) <= size:
        compareBDD(bdd1, bdd2, text + "0", size)
        if len(text) == size:
            if bdd1.badBDD_use(text) != bdd2.BDD_use(text):
                return False
        compareBDD(bdd1, bdd2, text + "1", size)
    return True


# Metoda na vytvorenie nahodnej boolovskej funkcie
def createRandomFunction():
    velkost = random.randint(1, 6)
    abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    temp = ""
    cislo = 0
    for i in range(0, random.randint(0, 15)):
        if cislo >= velkost:
            temp += "+"
            cislo = 0
        if random.randint(0, 1) == 0:
            temp += "!"
        cislo = random.randint(cislo, velkost)
        temp += abeceda[cislo]
        cislo += 1
    if temp == "":
        return createRandomFunction()
    temp = temp.split("+")
    return list(dict.fromkeys(temp))


# Metoda na vytvorenie poradia
def getPoradie(bfunckia):
    abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    poradie = ""
    for pismeno in abeceda:
        if pismeno in bfunckia:
            poradie += pismeno
    return poradie


# Metoda nam vrati string z array listu
def listToString(fList):
    s = ""
    for item in fList:
        s += item
    return s


# Zadavame v tvare A!C+ABC+!AB+!BC
while True:

    while True:
        bfunkcia = createRandomFunction()
        poradie = getPoradie(listToString(bfunkcia))
        bad = BDD(poradie, bfunkcia)
        bad.root = bad.BDD_createWithDuplicates(bad.root, poradie)
        bddroot = BDD(poradie, bfunkcia)
        bddroot.root = bddroot.BDD_create(bddroot.root, poradie, bfunkcia)
        if compareBDD(bad, bddroot, "", len(poradie)) == False:
            break
        else:
            bddroot.root.display()
            bddroot.everynumber("", len(poradie), [])
            input()

    bfunkcia = input("Zadaj funkciu v DNF, poradie je zoradene podla abecedy:\n")
    poradie = getPoradie(bfunkcia)
    fList = bfunkcia.split("+")

    bad = BDD(poradie, fList)
    bad.root = bad.BDD_createWithDuplicates(bad.root, poradie)
    bad.root.display()

    print("\n")

    bddroot = BDD(poradie, fList)
    bddroot.root = bddroot.BDD_create(bddroot.root, poradie, fList)
    bddroot.root.display()

    print(
        "\nPocet prvkov BDD je:",
        bddroot.values,
        "a pocet prvkov neredukovaneho BDD je:",
        bad.values,
    )
    if compareBDD(bad, bddroot, "", len(poradie)) == True:
        print("Hodnoty stromu su rovnake po reduckii")
    while True:
        kombinacia = input(
            "Zadaj kombinaciu pre " + poradie + " alebo stlac enter pre novu funkciu\n"
        )
        if kombinacia == "":
            break
        print("Vysledok neredukovaneho stromu:", bad.badBDD_use(kombinacia))
        print("Vysledok redukovaneho stromu:", bddroot.BDD_use(kombinacia))
