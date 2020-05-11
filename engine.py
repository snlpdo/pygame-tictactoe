"""
Ce module s'occupe du fonction interne du jeu.
Il ne doit surtout pas supposer qu'il existe une interface
graphique.
"""


def pion_blanc(depart, arrivee):
    # Récupérer les indices de lignes et colonnes
    col_dep, ligne_dep = depart
    col_arr, ligne_arr = arrivee

    # Règle 1: case d'arrivée sur la ligne supérieure
    # ou 2 cases pour le premier déplacement
    if not ((ligne_arr == ligne_dep - 2 and ligne_dep == 6) or ligne_arr == ligne_dep - 1):
        return False

    # Règle 2: cases dans la même colonne
    if not (col_arr == col_dep):
        return False

    return True


class Jeu:

    def __init__(self):
        # Contenu des cellules:
        # 0: case vide
        # 1: croix
        # 2: cercle
        self.plateau = [
            ['tn', 'cn', 'fn', 'dn', 'rn', 'fn', 'cn', 'tn'],
            ['pn', 'pn', 'pn', 'pn', 'pn', 'pn', 'pn', 'pn'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
            ['tb', 'cb', 'fb', 'db', 'rb', 'fb', 'cb', 'tb']
        ]

    def occupant(self, colonne, ligne):
        if self.plateau[ligne][colonne] == '':  # case vide
            return None
        else:
            return self.plateau[ligne][colonne]

    def deplacer(self, dep, arr):
        # 1. Identifier la pièce à déplacer (=celle sur la case de départ)
        # dep est un couple au format: (, )
        colonne, ligne = dep
        piece = self.plateau[ligne][colonne]

        # 2. Vérifier la validité du déplacement
        deplacement_valide = True  # valeur par défaut
        if piece == 'pb':  # Pion blanc
            deplacement_valide = pion_blanc(dep, arr)

        if deplacement_valide:
            # recopier le type de pièce
            self.plateau[arr[1]][arr[0]] = self.plateau[dep[1]][dep[0]]
            # vider la case de départ
            self.plateau[dep[1]][dep[0]] = ''
