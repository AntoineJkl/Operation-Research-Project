# -*- coding: utf-8 -*-
from pulp import*
import numpy as np
import random as random

class Ordonnancement:
    
    def __init__(self):
        self.nb_piece=0 #Nombre de pièces
        self.unite_temps=[] #Unités de temps nécessaires pour les pièces
        self.deadlines=[] #Deadlines pour chaque pièce
        self.penalites=[] #Pénalités pour les retards de chaque pièce
        self.contraintesPrecedence = {} #Contraintes de précédence entre les pièces
        
    def ajouterPieces(self,liste_ut,liste_d,liste_p):
        #On vérifie qu'il ne manque pas d'informations
        if(len(liste_ut) == len(liste_d) == len(liste_p)):
            self.nb_piece += len(liste_ut) #Augmentation du nombre de pièces
            self.unite_temps += liste_ut #Ajout des unités de temps des nouvelles pièces
            self.deadlines += liste_d #Ajout des deadlies des nouvelles pièces
            self.penalites += liste_p #Ajout des penalites des nouvelles pièces
        else:
            print("Attention les listes doivent être de même longueur")
    
    #Fonction permettant d'imposer que les pices de la liste 'pieces_precedentes' passent avant 'piece'
    def ajouterContraintePrecedence(self,piece,pieces_precedentes):
        if(piece >= self.nb_piece):
            #La pièce doit être dans la liste pour lui imposer des contraintes de précédence
            print("Attention ! La pièce",piece,"n'a pas encore été ajoutée")
        else:
            #On ajoute les contraintes de précédence
            if piece not in self.contraintesPrecedence:
                self.contraintesPrecedence[piece] = pieces_precedentes
            else:
                for p in pieces_precedentes:
                    self.contraintesPrecedence[piece].append(p)
    
    #A enlever
    def coutSolution(self,ordre):
        if(len(ordre) == self.nb_piece) and (all(i in list(range(self.nb_piece)) for i in ordre)):
            date_fin = 0
            cout = 0
            for piece in ordre:
                date_fin += self.unite_temps[piece]
                cout += max(0,date_fin - self.deadlines[piece])*self.penalites[piece]
            return(cout)
        else:
            print("Erreur")
    
    #Fonction permettant d'afficher les données du problèmes créé
    def afficherProbleme(self):
        print("\nAFFICHAGE DU PROBLEME:\n")
        print("############### PIECES ##############")
        for i in range(self.nb_piece):
            print("Piece n°",i,": [Unités de temps nécessaires: ",self.unite_temps[i],"Deadline: ",self.deadlines[i],"Pénalité par unité de temps de retard: ",self.penalites[i],"]")
        print("###### CONTRAINTES PRECEDENCES ######")
        if(len(self.contraintesPrecedence) ==  0):
            print("Pas de contraintes de précédence")
        else:
            for i in self.contraintesPrecedence:
                for j in self.contraintesPrecedence[i]:
                    print("La pièce",j,"doit passer avant la pièce",i)
    
    #Fonction permettant de créer une instance de n pièces aux valeurs aléatoire 
    def problemeAleatoire(self,n = 10):
        self.nb_piece = n #Nombre de pièces
        self.unite_temps = [random.randint(1,20) for i in range(n)] #Unités de temps
        self.deadlines = [random.randint(20,40) for i in range(n)] #Deadlines
        self.penalites = [random.randint(1,10) for i in range(n)] #Pénalités
        
        
    def resolutionPLNE(self,afficheTout=0):
        #Création du modèle:
        modele = LpProblem("Ordonnancement",LpMinimize)
        #Ensembles des pièces
        J = list(range(self.nb_piece))
        #Variables:
        r = LpVariable.dicts("r",J,0,None,LpContinuous) #Retard de chaque piece
        f = LpVariable.dicts("f",J,0,None,LpContinuous) #Date de fin d'usinage de chaque piece
        x = LpVariable.matrix("x",(J,J),0,1,LpInteger) #Ordre de passage des pieces
        #Objectif:
        modele += pulp.lpSum([self.penalites[j]*r[j] for j in J]) #Minimisation des pénalités de retard
        #Contraintes:
        
        for j in J:
            modele += r[j] >= f[j] - self.deadlines[j] #Calcul du retard
        
        for j in J:
            modele += f[j] == self.unite_temps[j] + lpSum([self.unite_temps[i]*x[i][j] for i in J if i != j]) #Calcul des dates de fin d'usinage
        
        for j in J:
            modele += x[j][j] == 0 #Une pièce ne peut pas passer avant elle-même
        
        for j in J:
            for i in range(j):
                modele += x[i][j] + x[j][i] == 1 #Impose l'ordre total sur la relation d'ordre
        
        for j in J:
            for i in J:
                for k in J:
                    if(i<j and i<k and j != k):
                        modele += x[i][k] >= x[i][j] + x[j][k]- 1 #Impose la transitivité sur la relation d'ordre
        
        for j in self.contraintesPrecedence:
            for i in self.contraintesPrecedence[j]:
                modele += x[i][j] == 1 #Impose la contrainte de précédence : i doit passer avant j
                
        print("\nRESOLUTION DU PROBLEME:\n")
        #Résolution du problème:
        print("Solve with CBC")
        modele.solve(pulp.PULP_CBC_CMD())
        #Affichage de la solution
        print("Status:",LpStatus[modele.status])
        print("Optimal value =",value(modele.objective))
        #Si option selectionnée, on affiche toutes variables
        if(afficheTout):
            print(modele)
            for v in modele.variables():
                print(v.name,"=",v.varValue)
        #Si la solution est optimale, on affiche le résultat
        if(LpStatus[modele.status] == "Optimal"):
            print("\nSOLUTION OBTENUE PLNE:\n")
            print("Total des pénalités:",value(modele.objective))
            #Reconstruction de l'ordre des pièces
            Ordre = []
            k = self.nb_piece - 1
            while(k >= 0):
                for i in J:
                    if(sum([value(x[i][j]) for j in J]) == k):
                        Ordre.append(i)
                k -= 1
            print("Ordre d'usinage des pièces:",Ordre)
        else:
            print("Erreur lors de la résolution")











            
            