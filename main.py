# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 12:53:16 2020

@author: antoi
"""

import Ordonnancement as order
import ArbreEnumeration as ar
import time

if __name__ == "__main__":
    """
    probleme1 = order.Ordonnancement()
    #Instance du TD (Exercice 7)
    P = [4,5,3,5] #Pénalités
    T = [12,8,15,9] #Unités de temps nécessaires
    D = [16,26,25,27] #Deadlines
    probleme1.ajouterPieces(T,D,P)
    probleme1.ajouterContraintePrecedence(3,[0,1,2])
    probleme1.afficherProbleme()
    probleme1.resolutionPLNE()
    #Instance aléatoire
    probleme2 = order.Ordonnancement()
    probleme2.problemeAleatoire(10)
    probleme2.afficherProbleme()
    t1 = time.time()
    probleme2.resolutionPLNE()
    t2 = time.time()
    print("Temps écoulé : ", t2 - t1,"s")
    """
    probleme2 = order.Ordonnancement()
    probleme2.problemeAleatoire(10)
    #probleme2.ajouterContraintePrecedence(3,[0,1,2])
    #probleme2.ajouterContraintePrecedence(0,[9,8,1])
    
    t1_plne2 = time.time()
    probleme2.resolutionPLNE()
    t2_plne2 = time.time()
    print("Temps exécution pulp: ",t2_plne2-t1_plne2,"s")
    print("\n")
    
        #Méthode 2 avec meilleur d'abord:
    t1_bb7 = time.time()
    z7,x7,k7 = ar.branch_and_bound(probleme2,ar.primale3,ar.borne_duale1,ar.Branchement1,ar.best_first_method)
    t2_bb7 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (Meilleur d'abord) : \n\nz = ",z7,", x = ",x7)
    print("Temps exécution B&B: ",t2_bb7-t1_bb7,"s")
    print("Nombre d'itérations: ",k7)
    
    print("======================\n")
    
            #Méthode 2 avec meilleur d'abord:
    t1_bb7 = time.time()
    z7,x7,k7 = ar.branch_and_bound(probleme2,ar.primale3,ar.borne_duale1,ar.Branchement1,ar.mixed_method)
    t2_bb7 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (Meilleur d'abord) : \n\nz = ",z7,", x = ",x7)
    print("Temps exécution B&B: ",t2_bb7-t1_bb7,"s")
    print("Nombre d'itérations: ",k7)
    
    print("======================\n")
    
    
        #Méthode 2 avec meilleur d'abord:
    t1_bb7 = time.time()
    z7,x7,k7 = ar.branch_and_bound(probleme2,ar.primale3,ar.borne_duale1,ar.Branchement1,ar.depth_first_method)
    t2_bb7 = time.time()
    
    print("\n\nSOLUTION OBTENUE B&B METHODE 2 (Meilleur d'abord) : \n\nz = ",z7,", x = ",x7)
    print("Temps exécution B&B: ",t2_bb7-t1_bb7,"s")
    print("Nombre d'itérations: ",k7)