# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 12:53:16 2020

@author: antoi
"""

import Ordonnancement as order

if __name__ == "__main__":
    probleme1 = order.Ordonnancement()
    #Instance du TD (Exercice 7)
    P = [4,5,3,5] #Pénalités
    T = [12,8,15,9] #Unités de temps nécessaires
    D = [16,26,25,27] #Deadlines
    probleme1.ajouterPieces(T,D,P)
    probleme1.afficherProbleme()
    probleme1.resolutionPLNE()
    #Instance aléatoire
    probleme2 = order.Ordonnancement()
    probleme2.problemeAleatoire()
    probleme2.afficherProbleme()
    probleme2.resolutionPLNE()