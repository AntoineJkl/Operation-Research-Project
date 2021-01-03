# -*- coding: utf-8 -*-
import pulp
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
        self.nb_piece += len(liste_ut)
        self.unite_temps += liste_ut
        self.deadlines += liste_d
        self.penalites += liste_p
    
    def ajouterContraintePrecedence(self,piece,pieces_precedentes):
        if(piece >= self.nb_piece):
            print("Attention ! La pièce",piece,"n'a pas encore été ajoutée")
        else:
            if piece not in self.contraintesPrecedence:
                self.contraintesPrecedence[piece] = pieces_precedentes
            else:
                for p in pieces_precedentes:
                    self.contraintesPrecedence[piece].append(p)
    
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
    
    def afficherProbleme(self):
        print("\nAFFICHAGE DU PROBLEME:\n")
        for i in range(self.nb_piece):
            print("Piece n°",i,": [Unités de temps nécessaires: ",self.unite_temps[i],"Deadline: ",self.deadlines[i],"Pénalité par unité de temps de retard: ",self.penalites[i],"]")
        
    def problemeAleatoire(self,n = 10):
        self.nb_piece = n
        self.unite_temps = [random.randint(1,20) for i in range(n)]
        self.deadlines = [random.randint(20,40) for i in range(n)]
        self.penalites = [random.randint(1,10) for i in range(n)]
        
        
    def resolutionPLNE(self,afficheTout=0):
        #Création du modèle:
        modele = pulp.LpProblem("Ordonnancement",pulp.LpMinimize)
        J = list(range(self.nb_piece))
        #Variables:
        r = pulp.LpVariable.dicts("r",J,0,None,pulp.LpContinuous) #Retard de chaque piece
        f = pulp.LpVariable.dicts("f",J,0,None,pulp.LpContinuous) #Date de fin d'usinage de chaque piece
        x = pulp.LpVariable.matrix("x",(J,J),0,1,pulp.LpInteger) #Ordre de passage des pieces
        #Objectif:
        modele += pulp.lpSum([self.penalites[j]*r[j] for j in J]) #Minimisation des pénalités de retard
        #Contraintes:
        
        for j in J:
            modele += r[j] >= f[j] - self.deadlines[j] #Calcul du retard
        
        for j in J:
            modele += f[j] == self.unite_temps[j] + pulp.lpSum([self.unite_temps[i]*x[i][j] for i in J if i != j]) #Calcul des dates de fin d'usinage
        
        for j in J:
            modele += x[j][j] == 0
        
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
                modele += x[i][j] == 1 #Impose les contraintes de précédence
                
        print("\nRESOLUTION DU PROBLEME:\n")
        #Résolution du problème:
        print("Solve with CBC")
        modele.solve(pulp.PULP_CBC_CMD())
        #Affichage de la solution
        print("Status:",pulp.LpStatus[modele.status])
        print("Optimal value =",pulp.value(modele.objective))
        if(afficheTout):
            print(modele)
            for v in modele.variables():
                print(v.name,"=",v.varValue)
        print("\nSOLUTION OBTENUE PLNE:\n")
        print("Total des pénalités:",pulp.value(modele.objective))
        Ordre = []
        k = self.nb_piece - 1
        while(k >= 0):
            for i in J:
                if(sum([pulp.value(x[i][j]) for j in J]) == k):
                    Ordre.append(i)
            k -= 1
        print("Ordre d'usinage des pièces:",Ordre)










            
            