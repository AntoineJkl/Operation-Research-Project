# -*- coding: utf-8 -*-

#Classe représentant le concept d'arbre d'énumération

class ArbreEnumeration:
    
    def __init__(self,d1,p1):
            self.nombre_noeuds=1
            self.tree=[Noeud("Problème Initial",())]
            self.dual_bounds=[d1]
            self.primal_bounds=[p1]
    
    def ajouterBranchement(self,noeud1,noeud2):
        self.nombre_noeuds+=2
        self.tree= self.tree+[noeud1,noeud2]

class Noeud:
    
    def __init__(self,description,position):
        self.description=description
        self.position=position #tupple pour définir la position donnant les directions qu'il faut emprunter du début de l'arbre jusqu'à la fin
    
    
if __name__ == "__main__":
    a = ArbreEnumeration(1000,0)
    print(a.tree[0].position)
    a.ajouterBranchement(Noeud("1",(1)),Noeud("2",(2)))
    print(a.tree[1].position)
