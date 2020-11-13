# -*- coding: utf-8 -*-
class Ordonnancement:
    
    def __init__(self):
        self.nb_piece=0
        self.unite_temps=[]
        self.deadlines=[]
        self.penalites=[]
        
    def ajouterPieces(self,liste_ut,liste_d,liste_p):
        self.nb_piece += len(liste_ut)
        self.unite_temps += liste_ut
        self.deadlines += liste_d
        self.penalites += liste_p

