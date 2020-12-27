# -*- coding: utf-8 -*-

#Classe représentant le concept d'arbre d'énumération

import Ordonnancement as order
import time

class ArbreEnumeration:
    
    def __init__(self,d1,p1):
            self.nombre_noeuds=1
            self.nombre_noeuds_non_traites = 1
            self.noeuds = [Noeud("Problème initiale",False)]
            self.indice_noeuds_non_traites= [0]
            self.dual_bound=d1
            self.primal_bound=p1
    
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
    
    def __init__(self,description,pos,info =[],indice=-1):
        self.description=description
        self.position = pos #branche : 0 ou une feuille : 1
        self.indice_pere = indice #-1 si noeud racine
        self.info = info
    
#Algorithme générique du branch-and-bound:
def branch_and_bound(instance,primale,borne_duale,Branchement):
    #Calcul de la borne primale initiale:
    p = primale(instance)
    #Création de l'arrbre d'énumération (pas de borne duale ???):
    arbre=ArbreEnumeration(0,p) 
    #Initialisation de la meilleure solution courante:
    Current_best_solution = []
    k = 1
    while(arbre.indice_noeuds_non_traites != []):
        #Récupération du premier noeud Pk dans Q
        Pk = arbre.indice_noeuds_non_traites.pop()
        
        #Calcul de la borne dual de Pk
        zD, isOptimal, solution  = borne_duale(arbre.noeuds[Pk],instance)
        
        #Disjonction des cas:
        if(zD > arbre.primal_bound):
            #Si zD est plus grand que la borne primale courante, on élague (uniquement pour un problème de minimisation)
            pass
        elif(isOptimal):
            #Si zD est optimale pour Pk, on met à jour la borne primale:
            if zD < arbre.primal_bound:
                #On met à jour la meilleure solution courante:
                Current_best_solution = solution
            arbre.primal_bound = min(arbre.primal_bound,zD)
        else:
            #Sinon branchement et ajout des noeuds fils à l'arbre (en fonction de la méthode d'exploration):
            Branchement(arbre,arbre.noeuds[Pk],instance)
        k+=1
    return arbre.primal_bound, Current_best_solution

#Pour trouver une borne primale, on prend la solution constituée des pièces les unes à la suite des autres
def primale1(instance):
    borne = 0
    for i in range(instance.nb_piece):
        date_fin = 0
        for j in range(i+1):
            date_fin += instance.unite_temps[j]
        if(date_fin >= instance.deadlines[i]):
            borne += (date_fin - instance.deadlines[i])*instance.penalites[i]
    return(borne)

#Pour trouver une borne duale, si on a fixé l'ordre des k pièces, on calcule les pénalités de retard de ces k pièces et on ajoute la pénalité des autres pièces en supposant qu'elles passent en (k+1)-ème position
def borne_duale1(node,instance):
    borne = 0
    temps_utilise = 0
    #Pénalités des pièces déjà usinées
    for i in range(len(node.info)):
        date_fin = 0
        for j in range(i+1):
           date_fin += instance.unite_temps[node.info[j]] 
        borne += max(0,date_fin - instance.deadlines[node.info[i]])*instance.penalites[node.info[i]]
        temps_utilise += instance.unite_temps[node.info[i]]
    #Liste des pièces non-usinées
    pieces_non_usinees = [i for i in range(instance.nb_piece) if i not in node.info]
    #Pénalités des pièces non-usinées
    for i in pieces_non_usinees:
        borne += max(0,temps_utilise + instance.unite_temps[i] - instance.deadlines[i])*instance.penalites[i]
    if(node.position):
        solution = node.info.copy()
        solution += pieces_non_usinees
    else:
        solution = None
    return borne, node.position,solution
        
#Pour la règle de branchement, au niveau k, on crée un noeud pour chaque pièce non usinée et on l'usine en k-ème position
#Méthode d'exploration : parcours en profondeur (on ajoute les nouveaux noeuds au début de la pile)
def Branchement1(arbre,noeud,instance):
    pieces_non_usinees = [i for i in range(instance.nb_piece) if i not in noeud.info]
    if(len(pieces_non_usinees) == 2):
        position = True
    else:
        position = False
    for i in pieces_non_usinees:
        arbre.nombre_noeuds += 1
        new_info = noeud.info.copy()
        new_info.append(i)
        des = "P"
        for piece in noeud.info:
            des += str(piece)
        des += str(i)
        arbre.noeuds.append(Noeud(des,position,new_info,arbre.nombre_noeuds-1))
        arbre.nombre_noeuds_non_traites+=1
        arbre.indice_noeuds_non_traites.append(arbre.nombre_noeuds-1)
        
    
if __name__ == "__main__":
    a = ArbreEnumeration(1000,0)
    probleme1 = order.Ordonnancement()
    #Instance du TD (Exercice 7)
    '''
    P = [4,5,3,5] #Pénalités
    T = [12,8,15,9] #Unités de temps nécessaires
    D = [16,26,25,27] #Deadlines
    probleme1.ajouterPieces(T,D,P)
    '''
    probleme1.problemeAleatoire(10)
    t1_plne = time.time()
    probleme1.resolutionPLNE()
    t2_plne = time.time()
    print("Temps exécution pulp: ",t2_plne-t1_plne,"s")
    
    t1_bb = time.time()
    z,x = branch_and_bound(probleme1,primale1,borne_duale1,Branchement1)
    t2_bb = time.time()
    
    print("\nSOLUTION OBTENUE B&B : \n\nz = ",z,", x = ",x)
    print("Temps exécution B&B: ",t2_bb-t1_bb,"s")