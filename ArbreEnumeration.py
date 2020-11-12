# -*- coding: utf-8 -*-

#Classe représentant le concept d'arbre d'énumération

class ArbreEnumeration:
    
    def __init__(self,d1,p1):
            self.nombre_noeuds=1
            self.tree=[Noeud("Problème Initial",[0],"No")]
            self.dual_bounds=[d1]
            self.primal_bounds=[p1]
    
    def ajouterBranchement(self,descript1,descript2,pos):
        self.nombre_noeuds+=2
        self.tree= self.tree+[Noeud(descript1,pos+[1],"No"),Noeud(descript2,pos+[2],"No")]

class Noeud:
    
    def __init__(self,description,position,state):
        self.description=description
        self.position=position #list pour définir la position donnant les directions qu'il faut emprunter du début de l'arbre jusqu'à la fin
        #ou sinon position en largeur et en longueur permet de diminuer considérablement la recherche je pense !!
        self.state=state
    
if __name__ == "__main__":
    a = ArbreEnumeration(1000,0)
    print(a.tree[0].position)
    a.ajouterBranchement("1","2",[0])
    print(a.tree[2].position)
