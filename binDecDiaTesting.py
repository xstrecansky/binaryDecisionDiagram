import random
import time
import tracemalloc


# Trieda jednej nody
class Node(object):
    def __init__(self, value, i):
        self.left = None
        self.right = None
        self.value = value
        # Unikatne id na pocitanie poctu prvkov
        self.id = i

    # Kod prevzaty z https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
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
    def everynumber(self, text, size):
        if len(text) <= size:
            self.everynumber(text + "0", size)
            if len(text) == size:
                print(self.BDD_use(text), end="")
            self.everynumber(text + "1", size)

    def badeverynumber(self, text, size):
        if len(text) <= size:
            self.badeverynumber(text + "0", size)
            if len(text) == size:
                print(self.badBDD_use(text), end="")
            self.badeverynumber(text + "1", size)

    # Funckia na vytvorenie binarneho diagramu
    # Bez oplimalizacie a odstranenia duplikatov
    def BDD_createWithDuplicates(self, root, poradie):
        if ("0" in root.value) or ("1" in root.value):
            return root
        if poradie:
            root.left = Node(leftString(root.value, poradie[0]), self.incValues(1))
            root.left = self.BDD_createWithDuplicates(root.left, poradie[1:])
            root.right = Node(rightString(root.value, poradie[0]), self.incValues(1))
            root.right = self.BDD_createWithDuplicates(root.right, poradie[1:])
        return root

    # Vyhladavanie pre neoptimalizovany BDD
    def badBDD_use(self, combination):
        tempRoot = self.root
        for letter in combination:
            if "1" in tempRoot.value:
                return "1"
            if "0" in tempRoot.value:
                return "0"
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
                continue
            # Pripad kedy sa nachadza vo funkcii C
            if item.find(letter) == 0 and item[0] != "!":
                # Odstranime pismeno a pridame do listu
                new = item.replace(letter, "")
                posA.append(new)
            # Ak sa nenachadza C vo funkcii pridame
            if item.find(letter) == -1:
                posA.append(item)
        if len(posA) == 0:
            posA.append("0")
            return posA
        # Odstranime duplikaty
        if "" in posA:
            posA.remove("")
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
def compareBDD(bdd1, bdd2, array):
    for item in array:
        if bdd1.badBDD_use(item) != bdd2.BDD_use(item):
            return False
    return True


def createCombinations(text, size, array):
    if len(text) <= size:
        createCombinations(text + "0", size, array)
        if len(text) == size:
            array.append(text)
        createCombinations(text + "1", size, array)
    return array


# Metoda na vytvorenie nahodnej boolovskej funkcie
def createRandomFunction(velkost, dlzka):
    abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    temp = ""
    cislo = 0
    i = 0
    while i < dlzka:
        if cislo >= velkost - 1:
            temp += "+"
            cislo = 0
        if random.randint(0, 2) == 0:
            temp += "!"
        cislo = random.randint(cislo, velkost - 1)
        temp += abeceda[cislo]
        cislo += 1
        i += 1
    plus = False
    for j in range(0, velkost - 1):
        if abeceda[j] not in temp:
            if plus == False:
                temp += "+"
                plus = True
            if random.randint(0, 1) == 0:
                temp += "!"
            temp += abeceda[j]
    return temp


# Metoda na vytvorenie poradia
def getPoradie(bfunkcia):
    abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    poradie = ""
    for pismeno in abeceda:
        if pismeno in bfunkcia:
            poradie += pismeno
    return poradie


# Metoda nam vrati string z array listu
def listToString(fList):
    s = ""
    for item in fList:
        s += item
    return s


def DNFtoVector(temp, poradie):
    combinations = createCombinations("", len(poradie), [])
    vector = ""
    for combination in combinations:
        bfunkcia = temp
        for i in range(0, len(combination)):
            pismeno = poradie[i]
            if pismeno not in bfunkcia:
                continue
            if ("!" + pismeno) in bfunkcia:
                if combination[i] == "0":
                    bfunkcia = bfunkcia.replace("!" + pismeno, "1")
                else:
                    bfunkcia = bfunkcia.replace("!" + pismeno, "0")
            if pismeno in bfunkcia:
                if combination[i] == "0":
                    bfunkcia = bfunkcia.replace(pismeno, "0")
                else:
                    bfunkcia = bfunkcia.replace(pismeno, "1")
        fList = bfunkcia.split("+")
        counter = 0
        for item in fList:
            if "0" in item:
                counter += 1
        if counter == len(fList):
            vector += "0"
        else:
            vector += "1"
    return vector


# Zadavame v tvare A!C+ABC+!AB+!BC
def main():
    print()
    for velkost in range(5, 16):
        pocet1 = 0
        pocet2 = 0
        timecounter = 0
        testtimecounter = 0
        maxsize = 0
        for j in range(0, 251):
            dlzka = velkost * 2
            tempf = createRandomFunction(velkost, dlzka)
            bfunkcia = tempf.split("+")
            poradie = getPoradie(tempf)

            bad = BDD(poradie, bfunkcia)
            bad.root = bad.BDD_createWithDuplicates(bad.root, poradie)
            # Zacneme meriat vyuzitie pamate
            tracemalloc.start()
            start_time = time.time()
            # Zacneme meriat cas
            good = BDD(poradie, bfunkcia)
            # Vytvorime redukovany strom a zapiseme maximalne vyuzitie pamate a casu
            good.root = good.BDD_create(good.root, poradie, bfunkcia)
            maxsize += int(tracemalloc.get_traced_memory()[1])
            end_time = time.time()
            tracemalloc.stop()
            # Vytvorime vektor
            vektor = DNFtoVector(tempf, poradie)

            temp = createCombinations("", len(poradie), [])
            # Vytvorime si vysledny vektor cez dekompoziciu a porovnavame s vytvorenym vektorom
            test_start_time = time.time()
            vysledok = ""
            for item in temp:
                vysledok += good.BDD_use(item)
            test_end_time = time.time()
            # Ak sa vysledky nerovnaju vypiseme chybu
            if vysledok != vektor:
                print("Chyba")
                return
            # Pripocitame hodnoty
            pocet1 += good.values
            pocet2 += bad.values
            timecounter += end_time - start_time
            testtimecounter += test_end_time - test_start_time

        print(
            "Vytvorenie redukovaneho stromu pre:",
            (str(velkost)),
            "pismen je v priemere:\t{:.6f}".format(timecounter / 250),
            "sekund",
            "\nTestovanie vsetkych hodnot je v priemere:\t\t\t{:.6f}".format(
                testtimecounter / 250
            ),
            "sekund",
            "\nMiera zredukovanie je:\t\t\t\t\t\t{:.3f}".format(
                (100 - ((pocet1) / ((pocet2) / 100)))
            ),
            "%",
            "\nVyuzitie pamati je v priemere:\t\t\t\t\t{:.0f}".format(maxsize / 250),
            "KiB\n\n",
        )


main()
