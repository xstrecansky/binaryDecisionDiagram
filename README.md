# binaryDecisionDiagram
Binárny Rozhodovací Diagram
Zadanie 2, Dátové Štruktúry a Algoritmy
Id: 116298, 2021/2022

Maximilián Strečanský



Riešenie redukcie:
•	Pri vytváraní binárneho diagramu rekurzívne vytvárame najprv ľavé a potom pravé prvky (Inorder). Pred každým pridaním prvku sa najprv pozrieme či daný prvok už v strome neexistuje -> takto docielime redukciu. 
•	Redukujeme celý strom, nie len samostatný riadok. Po redukcií nám neostanú v strome duplikáty.
•	Taktiež ak sa nám obaja potomkovia jedného uzla rovnajú 0 alebo 1, tak zmeníme tento uzol na hodnotu potomka -> takto vymažeme nepotrebné prvky a docielime efektívnejšie prehľadávanie


Riešenie kombinácie:
•	Pri funkcii BDD_create prechádzame strom podľa vstupnej kombinácie. Podľa poradia prechádzame strom.
•	Príklad booleovskej funkcie AB+C -> kombinácia 010



#                ______________['AB', 'C'],id:1_____________________________________                  
#               /                                                                  	\                 
#      ____['C'],id:2_____                                    				 ______________['B', 'C'],id:5_____     
#     /                   \                                   				/                                  \    
#['0'],id:3          ['1'],id:4                     				    ____['C'],id:2_____                     ['1'],id:4
#                                                				    /    	               \                             
#                                              					['0'],id:3          ['1'],id:4               
#
  
•	Ako prvé prejdeme do ľavej hodnoty C keďže keď za A dosadíme 0 dostaneme C. Ďalej keď dosadíme za B 1 ostaneme stále v rovnakom uzle a až podľa hodnoty C ovplyvníme výsledok
•	Takto dokážeme korektne redukovať strom na najmenšie množstvo prvkov








Vlastné Štruktúry:
•	V triede NODE ukladáme pravý a ľavý prvok, hodnotu prvku a unikátne id pomocou ktorého vieme pri vypisovaní prvkov vidieť, že prvky sú rovnaké
•	V triede BDD si ukladáme smerník na počiatočnú hodnotu binárneho diagramu ako aj počet unikátnych uzlov diagramu, poradie v tvare (ABC...) a počet premenných.




Jednotlivé funkcie
•	Na vstupe dostaneme kombináciu v tvare 000, 010, 110... a binárny diagram. Cyklicky prejdeme cez uzle diagramu v závislosti od kombinácie. Ak dostaneme na vstupe 0 posunieme sa doľava, ak 1 doprava. Najprv sa ale pozrieme, či sa v NODE nachádza písmeno poradia. Ak áno, posunieme sa podľa kombinácie a ak nie, ostaneme v NODE.
•	Vo funkcii BDD_create máme na vstupe BDD diagram, aktuálnu NODE, poradie a booleovskú funkciu. Ako prvé sa pozrieme či existuje v poradí nejaký prvok, ak nie, vieme, že sme na konci diagramu ak áno pokračujeme. Rozložíme si booleovskú funkciu na pravý a ľavý prvok a postupne prechádzame. Ako prvé máme prípad kedy máme aktuálny NODE rovnaký s pravým a ľavým. Vrátime ďalšiu inštanciu
•	Ďalší prípad je keď máme pravú a ľavú stranu rovnakú, takto sa pozrieme či sa v strome nenachádza ďalšia rovnaká hodnota. Ak nie, nastavíme pravý prvok na ľavý a pokračujeme v ľavom prvku
•	Tretí prípad je obyčajný, najprv sa snažíme nájsť duplikát a ak ho nenájdeme, spustíme BDD_create na ľavý prvok. Ak sa v aktuálnej NODE nachádza 1 alebo 0 toto robiť nemusíme
•	Rovnako toto spravíme pre pravý prvok
•	Ako posledný krok sa pozrieme či nie je pravý a ľavý potomok rovnaký s hodnotami 1 alebo 0 ak áno, nastavíme aktuálny uzol na hodnotu ľavého
 
•	Keďže sa vždy pred pridaním prvku pozrieme, či sa už daná hodnota nenachádza v strome, docielime takto redukciu. V niektorých prípadoch ani nemusíme pokračovať v pridávaní potomkov. 
Spôsob testovania

