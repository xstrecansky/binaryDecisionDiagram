#include<stdio.h>
#include<stdlib.h>
#include<string.h>
//definujeme BDD
typedef struct node{
    int varCounter;
    int nodeCounter;
    struct BDD* root;
    struct node* left;
    struct node* right;
}node;
//Definujeme koren BDD
typedef struct BDD{
    struct node* left;
    struct node* right;
}BDD;
//Allokujeme pamat pre prvok 
//a nastavime jeho hodnoty na NULL, pretoze to je list
struct node* createNode(BDD* root){
    struct node* newNode = malloc(sizeof(node));
    if(newNode!=NULL){
        newNode->root = root;
        newNode->left = NULL;
        newNode->right = NULL;
    }
    return newNode;
}
//Alokujeme pamat pre koren BDD
BDD* createBDD(){
    struct BDD* newBDD = malloc(sizeof(BDD));
    if(newBDD!=NULL){
        newBDD->left = NULL;
        newBDD->right = NULL;
    }
    return newBDD;
}
//Funkcia BDD_create má slúžiť na zostavenie redukovaného binárneho rozhodovacieho diagramu, 
//ktorý má reprezentovať/opisovať zadanú Booleovskú funkciu, 
//ktorá je zadaná ako argument funkcie
BDD *BDD_create(char* bfunkcia, char* poradie){
    BDD* bdd = createBDD();

    return bdd;
}
//Funkcia BDD_use má slúžiť na použitie BDD pre zadanú (konkrétnu) kombináciu hodnôt 
//vstupných premenných Booleovskej funkcie azistenie výsledku Booleovskej funkcie pre 
//túto kombináciu vstupných premenných. 
char BDD_use(BDD *bdd, char* vstupy){
    return -1;
}
int main(){
    struct BDD* rootBDD = createBDD();
    char* vstup;
    printf("Vloz Boolovsku funkciu:\n");
    scanf("%s",vstup);
    rootBDD = BDD_create(vstup,"ABC");
    
    return 0;
}