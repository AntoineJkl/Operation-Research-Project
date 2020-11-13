# -*- coding: utf-8 -*-

#Classe représentant le concept d'arbre d'énumération

class ArbreEnumeration:
    
    def __init__(self,d1,p1):
            self.nombre_noeuds=1
            self.nombre_noeuds_non_traites = 1
            self.noeuds = [Noeud("Problème initiale",False)]
            self.indice_noeuds_non_traites= [0]
            self.dual_bounds=d1
            self.primal_bounds=p1
    
    def breadth_first_method(self,descript1,descript2,indice,position):
        self.nombre_noeuds+=2
        self.nombre_noeuds_non_traites+=2 #a voir si 1 ou 2
        self.noeuds += [Noeud(descript1,position,indice),Noeud(descript2,position,indice)]
        self.indice_noeuds_non_traites += [self.nombre_noeuds-2,self.nombre_noeuds-1]
        
    def depth_first_method(self,descript1,descript2,indice,position):
        self.nombre_noeuds+=2
        self.nombre_noeuds_non_traites+=2 #a voir si 1 ou 2
        self.noeuds += [Noeud(descript1,position,indice),Noeud(descript2,position,indice)]
        self.indice_noeuds_non_traites = [self.nombre_noeuds-2,self.nombre_noeuds-1] + self.indice_noeuds_non_traites
        
    def best_first_method(self,descript1,descript2,indice,position):
        
        return 0 ##on peut utiliser ici tas min binaire pour aller plus vite

class Noeud:
    
    def __init__(self,description,pos,indice=-1):
        self.description=description
        self.position = pos #branche : 0 ou une feuille : 1
        self.indice_pere = indice #-1 si noeud racine
    
if __name__ == "__main__":
    a = ArbreEnumeration(1000,0)
    
def branch_and_bound(instance):
    arbre=ArbreEnumeration()
    

