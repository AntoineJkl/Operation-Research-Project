# -*- coding: utf-8 -*-

#Classe représentant le concept d'arbre d'énumération

import Ordonnancement as order
import time
from heapq import *
import numpy as np
import matplotlib.pyplot as plt

class ArbreEnumeration:
    
    def __init__(self,d1,p1):
            self.nombre_noeuds=1
            self.nombre_noeuds_non_traites = 1
            self.noeuds = [Noeud("Problème initiale",False)]
            self.indice_noeuds_non_traites= [0]
            self.first_update_primal = False
            self.dual_bound=d1
            self.primal_bound=p1
            
class Noeud:
    
    def __init__(self,description,pos,info =[],indice=-1):
        self.description=description
        self.position = pos #branche : 0 ou une feuille : 1
        self.indice_pere = indice #-1 si noeud racine
        self.info = info
    

    
def depth_first_method(arbre,list_nodes): 
    n=len(list_nodes)
    arbre.nombre_noeuds+=n
    arbre.nombre_noeuds_non_traites+=n
    arbre.noeuds+= list_nodes
    arbre.indice_noeuds_non_traites+= [i for i in range(arbre.nombre_noeuds-n,arbre.nombre_noeuds)]
    
def breadth_first_method(arbre,list_nodes):
    n=len(list_nodes)
    arbre.nombre_noeuds+=n
    arbre.nombre_noeuds_non_traites+=n
    arbre.noeuds += list_nodes
    arbre.indice_noeuds_non_traites = [i for i in range(arbre.nombre_noeuds-n,arbre.nombre_noeuds)] + arbre.indice_noeuds_non_traites
    
def best_first_method(arbre,list_nodes,borne_duale,instance):
    n=len(list_nodes)
    arbre.nombre_noeuds+=n
    arbre.nombre_noeuds_non_traites+=n
    arbre.noeuds += list_nodes
    for i in range(arbre.nombre_noeuds-n,arbre.nombre_noeuds):
        zD, isOptimal, solution  = borne_duale(arbre.noeuds[i],instance)
        heappush(arbre.indice_noeuds_non_traites,(zD,isOptimal,solution,i))

def mixed_method(arbre,list_nodes,borne_duale,instance):
    if(not arbre.first_update_primal):
        n=len(list_nodes)
        arbre.nombre_noeuds+=n
        arbre.nombre_noeuds_non_traites+=n
        arbre.noeuds += list_nodes
        for i in range(arbre.nombre_noeuds-n,arbre.nombre_noeuds):
            zD, isOptimal, solution  = borne_duale(arbre.noeuds[i],instance)
            arbre.indice_noeuds_non_traites.append((zD,isOptimal,solution,i))
    else:
        n=len(list_nodes)
        arbre.nombre_noeuds+=n
        arbre.nombre_noeuds_non_traites+=n
        arbre.noeuds += list_nodes
        for i in range(arbre.nombre_noeuds-n,arbre.nombre_noeuds):
            zD, isOptimal, solution  = borne_duale(arbre.noeuds[i],instance)
            heappush(arbre.indice_noeuds_non_traites,(zD,isOptimal,solution,i))
            
def recuperationNoeud(arbre,explo,k,borne_duale,instance):
    if(explo == best_first_method):
            Pk = heappop(arbre.indice_noeuds_non_traites)
            if(k!=1):
                zD=Pk[0]
                isOptimal=Pk[1]
                solution=Pk[2]
                Pk=Pk[3]
    elif(explo == mixed_method):
        if(arbre.first_update_primal):
            Pk = heappop(arbre.indice_noeuds_non_traites)
            if(k!=1):
                zD=Pk[0]
                isOptimal=Pk[1]
                solution=Pk[2]
                Pk=Pk[3]
        else:
          Pk = arbre.indice_noeuds_non_traites.pop() 
          if(k!=1):
                zD=Pk[0]
                isOptimal=Pk[1]
                solution=Pk[2]
                Pk=Pk[3]
    else:
        Pk = arbre.indice_noeuds_non_traites.pop()

    #Ou alors .drop() pour retier au début : NON
    arbre.nombre_noeuds_non_traites-=1
    
    #Calcul de la borne dual de Pk
    if(explo not in [best_first_method,mixed_method] or k==1):
        zD, isOptimal, solution  = borne_duale(arbre.noeuds[Pk],instance)
    #isOptimal == pos du noeud
    #Zd c'est le premier element de heapop
    return Pk, zD, isOptimal, solution
            
def exploration(explo,arbre,list_nodes,borne_duale,instance):
    if(explo not in [best_first_method,mixed_method]):
        explo(arbre,list_nodes)
    else:
        explo(arbre,list_nodes,borne_duale,instance)
        
#Algorithme générique du branch-and-bound:
def branch_and_bound(instance,primale,borne_duale,Branchement,explo):
    #Calcul de la borne primale initiale et itialisation de la meilleure solution courante:
    p, Current_best_solution = primale(instance)
    #Création de l'arrbre d'énumération:
    arbre=ArbreEnumeration(0,p) 
    #Variable comptant le nombre d'itérations
    k = 1
    #Boucle principale
    while(arbre.indice_noeuds_non_traites != []):
        #Récupération du premier noeud Pk dans Q et de la borne duale du problème associé
        Pk, zD, isOptimal, solution = recuperationNoeud(arbre,explo,k,borne_duale,instance)
        #Disjonction des cas:
        if(zD >= arbre.primal_bound):
            #Si zD est plus grand que la borne primale courante, on élague (uniquement pour un problème de minimisation)
            pass
        elif(isOptimal):
            #Si zD est optimale pour Pk, on met à jour la borne primale:
            if zD < arbre.primal_bound:
                #On met à jour la meilleure solution courante:
                Current_best_solution = solution
                if(not arbre.first_update_primal):
                    arbre.first_update_primal = True
                    if(explo == mixed_method):
                        arbre.indice_noeuds_non_traites.sort()
            arbre.primal_bound = min(arbre.primal_bound,zD)
        else:
            #Sinon branchement et ajout des noeuds fils à l'arbre (en fonction de la méthode d'exploration):
            list_nodes=Branchement(arbre,instance,Pk)
            exploration(explo,arbre,list_nodes,borne_duale,instance)
        k+=1
    return arbre.primal_bound, Current_best_solution, k

#Pour trouver une borne primale, on prend la solution constituée des pièces les unes à la suite des autres
def primale1(instance):
    borne = 0
    solution = []
    for i in range(instance.nb_piece):
        date_fin = 0
        for j in range(i+1):
            date_fin += instance.unite_temps[j]
        if(date_fin >= instance.deadlines[i]):
            borne += max(0,date_fin - instance.deadlines[i])*instance.penalites[i]
        solution.append(i)
    return(borne,solution)

#Pour trouver une borne primale, on peut mettre successivement à la dernière position disponible l'élément non traité donnant lieu à la plus petite pénalité de retard
def primale3(instance):
    borne = 0
    piece_non_ajoute = list(range(instance.nb_piece))
    solution = []
    date_fin = sum(instance.unite_temps)
    while(len(piece_non_ajoute) != 0):
        pire_cas = [ max(0,(date_fin - instance.deadlines[i]))*instance.penalites[i] for i in piece_non_ajoute ]
        index = np.argmin(pire_cas)
        borne += min(pire_cas)
        prochaine_piece = piece_non_ajoute.pop(index)
        #print("min : ", min(pire_cas),"arg: ",prochaine_piece)
        date_fin -= instance.unite_temps[prochaine_piece]
        solution.insert(0,prochaine_piece)
    return(borne,solution)

#Pour trouver une borne primale (en particulier lorsque l'on impose des contraintes de précédence), on considère que chaque pièce engendre le maximum de pénalité possible
def primale2(instance):
    borne = 0
    date_fin = sum(instance.unite_temps)
    for i in range(instance.nb_piece):
        borne += max(0,date_fin - instance.deadlines[i])*instance.penalites[i]
    return(borne,[])

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

#Pour trouver une borne duale, si on a fixé l'ordre des dernières pièces, on calcule les pénalités des pièces dont l'ordre est fixé
def borne_duale2(node,instance):
    borne = 0
    for i in range(len(node.info)-1,-1,-1):
        date_fin = sum(instance.unite_temps)
        for j in range(len(node.info)-1,i,-1):
            date_fin -= instance.unite_temps[node.info[j]]
        borne += max(0,date_fin - instance.deadlines[node.info[i]])*instance.penalites[node.info[i]]
    if(node.position):
        solution = node.info.copy()
        noeuds_manquants = [x for x in range(instance.nb_piece) if x not in solution ]
        solution = noeuds_manquants + solution
        for i in range(len(noeuds_manquants)):
            borne += max(0,instance.unite_temps[noeuds_manquants[i]] - instance.deadlines[noeuds_manquants[i]])*instance.penalites[noeuds_manquants[i]]
    else:
        solution = None
    return borne, node.position,solution
        
#Pour la règle de branchement, au niveau k, on crée un noeud pour chaque pièce non usinée et on l'usine en k-ème position
def Branchement1(arbre,instance,indice_pere):
    noeud=arbre.noeuds[indice_pere]
    new_node=[]
    pieces_non_usinees = [i for i in range(instance.nb_piece) if i not in noeud.info]
    if(len(pieces_non_usinees) == 2):
        position = True
    else:
        position = False
    for i in pieces_non_usinees:
        if(i in instance.contraintesPrecedence):
            if(not all(piece in noeud.info for piece in instance.contraintesPrecedence[i])):
                continue
        #arbre.nombre_noeuds += 1
        new_info = noeud.info.copy()
        new_info.append(i)
        des = "P"
        for piece in noeud.info:
            des += str(piece)
        des += str(i)
        #arbre.noeuds.append(Noeud(des,position,new_info,arbre.nombre_noeuds-1))
        #arbre.nombre_noeuds_non_traites+=1
        #arbre.indice_noeuds_non_traites.append(arbre.nombre_noeuds-1)
        new_node.append(Noeud(des,position,new_info,indice_pere))
    return new_node
        
#Pour la règle de branchement, au niveau k de l'arbre, on crée un noeud pour chaque pièce non traitée et on la fixe à la (n-k+1)-ème position
def Branchement2(arbre,instance,indice_pere):
    noeud=arbre.noeuds[indice_pere]
    new_node=[]
    pieces_non_usinees = [i for i in range(instance.nb_piece) if i not in noeud.info]
    if(len(pieces_non_usinees) == 2):
        position = True
    else:
        position = False
    for i in pieces_non_usinees:
        if(i in instance.contraintesPrecedence):
            if(any(piece in noeud.info for piece in instance.contraintesPrecedence[i])):
                continue
        #arbre.nombre_noeuds += 1
        new_info = noeud.info.copy()
        new_info.insert(0,i)
        if(position):
            derniere_piece = [x for x in range(instance.nb_piece) if x not in new_info]
            if(derniere_piece[0] in instance.contraintesPrecedence):
                if(any(piece in noeud.info for piece in instance.contraintesPrecedence[derniere_piece[0]])):
                    continue
        des = "P"
        for piece in pieces_non_usinees:
            des += "."
        for piece in noeud.info:
            des += str(piece)
        des += str(i)
        new_node.append(Noeud(des,position,new_info,indice_pere))
        #arbre.noeuds.append(Noeud(des,position,new_info,arbre.nombre_noeuds-1))
        #arbre.nombre_noeuds_non_traites+=1
        #arbre.indice_noeuds_non_traites.append(arbre.nombre_noeuds-1)
    return new_node
                
    
if __name__ == "__main__":

    probleme1 = order.Ordonnancement()
    #Instance du TD (Exercice 7)

    #P = [4,5,3,5] #Pénalités
    #T = [12,8,15,9] #Unités de temps nécessaires
    #D = [16,26,25,27] #Deadlines
    #probleme1.ajouterPieces(T,D,P)
    #probleme1.ajouterContraintePrecedence(0,[2,1])
    #probleme1.ajouterContraintePrecedence(1,[2,3])
    probleme1.problemeAleatoire(8)
    #probleme1.ajouterContraintePrecedence(0,[1,2,3])
    #probleme1.ajouterContraintePrecedence(4,[1,3])
    #probleme1.ajouterContraintePrecedence(5,[1,2,3,4])
    t1_plne = time.time()
    probleme1.resolutionPLNE()
    t2_plne = time.time()
    print("Temps exécution pulp: ",t2_plne-t1_plne,"s")
    
    #Méthode 1 : On fixe l'ordre d'usinage des pièces en commençant par le début
    #Méthode 2 : On fixe l'ordre d'usinage des pièces en commençant par la fin
    #Méthode 1 avec un parcours en profondeur (DFS):
    t1_bb1 = time.time()
    z1,x1,k1 = branch_and_bound(probleme1,primale1,borne_duale1,Branchement1,depth_first_method)
    t2_bb1 = time.time()
   
    print("\n\nSOLUTION OBTENUE B&B METHODE 1 (DFS) : \n\nz = ",z1,", x = ",x1)
    print("Temps exécution B&B: ",t2_bb1-t1_bb1,"s")
    print("Nombre d'itérations: ",k1)


    #Méthode 1 avec un parcours en largeur (BFS):
    t1_bb2 = time.time()
    z2,x2,k2 = branch_and_bound(probleme1,primale1,borne_duale1,Branchement1,breadth_first_method)
    t2_bb2 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 1 (BFS) : \n\nz = ",z2,", x = ",x2)
    print("Temps exécution B&B: ",t2_bb2-t1_bb2,"s")
    print("Nombre d'itérations: ",k2)
    
    
    #Méthode 1 avec meilleur d'abord:
    t1_bb5 = time.time()
    z5,x5,k5 = branch_and_bound(probleme1,primale1,borne_duale1,Branchement1,best_first_method)
    t2_bb5 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 1 (Meilleur d'abord) : \n\nz = ",z5,", x = ",x5)
    print("Temps exécution B&B: ",t2_bb5-t1_bb5,"s")
    print("Nombre d'itérations: ",k5)
  
    #Méthode 2 avec un parcours en profondeur (DFS):
    t1_bb3 = time.time()
    z3,x3,k3 = branch_and_bound(probleme1,primale1,borne_duale2,Branchement2,depth_first_method)
    t2_bb3 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (DFS) : \n\nz = ",z3,", x = ",x3)
    print("Temps exécution B&B: ",t2_bb3-t1_bb3,"s")
    print("Nombre d'itérations: ",k3)

 
    #Méthode 2 avec un parcours en largeur (BFS):
    t1_bb4 = time.time()
    z4,x4,k4 = branch_and_bound(probleme1,primale1,borne_duale2,Branchement2,breadth_first_method)
    t2_bb4 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (BFS) : \n\nz = ",z4,", x = ",x4)
    print("Temps exécution B&B: ",t2_bb4-t1_bb4,"s")
    print("Nombre d'itérations: ",k4)
    
    
    #Méthode 2 avec meilleur d'abord:
    t1_bb6 = time.time()
    z6,x6,k6 = branch_and_bound(probleme1,primale1,borne_duale2,Branchement2,best_first_method)
    t2_bb6 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (Meilleur d'abord) : \n\nz = ",z6,", x = ",x6)
    print("Temps exécution B&B: ",t2_bb6-t1_bb6,"s")
    print("Nombre d'itérations: ",k6)
    
    #Ajout de contraintes de précédences
    
    print("\n\n ---- PROBLEME UTILISANT DES CONTRAINTES DE PRECEDENCE ----")
    
    probleme2 = order.Ordonnancement()
    P = [4,5,3,5,6,7,9,1,2] #Pénalités
    T = [12,8,15,9,13,15,7,10,9] #Unités de temps nécessaires
    D = [16,26,25,27,23,12,26,17,23] #Deadlines
    probleme2.ajouterPieces(T,D,P)
    probleme2.ajouterContraintePrecedence(0,[2,1])
    probleme2.ajouterContraintePrecedence(1,[2,3])
    probleme2.ajouterContraintePrecedence(6,[1,2,3,4,5])
    
    t1_plne2 = time.time()
    probleme2.resolutionPLNE()
    t2_plne2 = time.time()
    print("Temps exécution pulp: ",t2_plne2-t1_plne2,"s")
    
        #Méthode 2 avec meilleur d'abord:
    t1_bb7 = time.time()
    z7,x7,k7 = branch_and_bound(probleme2,primale2,borne_duale2,Branchement2,best_first_method)
    t2_bb7 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (Meilleur d'abord) : \n\nz = ",z7,", x = ",x7)
    print("Temps exécution B&B: ",t2_bb7-t1_bb7,"s")
    print("Nombre d'itérations: ",k7)
    
    
    
    