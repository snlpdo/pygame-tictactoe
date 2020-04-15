"""
Ce module s'occupe du fonction interne du jeu.
Il ne doit surtout pas supposer qu'il existe une interface
graphique.
"""

class Jeu:

  def __init__(self):
    # Contenu des cellules:
    # 0: case vide
    # 1: croix
    # 2: cercle
    self.plateau = [
      [1,2,0],
      [0,0,0],
      [0,0,0],
    ]


  def occupant(self,colonne,ligne):
    if self.plateau[ligne][colonne]==0: # case vide
      return None
    else: 
      return self.plateau[ligne][colonne]

  def deplacer(self, dep, arr):
    if self.plateau[arr[1]][arr[0]]==0: # arrivée libre
        # recopier le type de pièce
        self.plateau[arr[1]][arr[0]] = self.plateau[dep[1]][dep[0]]
        # vider la case de départ
        self.plateau[dep[1]][dep[0]] = 0
