import pygame
import pygame.freetype
import os
from engine import Jeu

"""
Ce module ne s'occupe que de la partie graphique (dessiner le plateau, les pièce) 
et de l'interaction avec l'utilisateur (gestion de la souris et/ou du clavier)
"""

# Constantes utiles
CZ = 50
WIDTH, HEIGHT = CZ * 10, CZ * 10
BGCOLOR = (213, 166, 49)
BLANC = (255, 255, 255)
MARRON = (97, 82, 74)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Démarrer la bibliothèque
pygame.init()

# Création du jeu
jeu = Jeu()

# Définir la taille de la fenêtre en pixels
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Échecs")

##################################################
# Préparer l'arrière plan
police = pygame.freetype.SysFont('overpass', 30, True, False)
police_petite = pygame.freetype.SysFont('overpass', 20, True, False)
police_mini = pygame.freetype.SysFont('overpass', 14, True, False)

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(BGCOLOR)
toggle = True
for i in range(8):
    text, r = police.render(str(8 - i), NOIR)
    background.blit(text, (CZ / 2 - r.width / 2, (i + 1) * CZ + CZ / 2 - r.height / 2))

    for j in range(8):
        if i == 0:
            text, r = police.render(chr(j + ord('A')), NOIR)
            background.blit(text, ((j + 1) * CZ + CZ / 2 - r.width / 2, CZ / 2 - r.height / 2))

        if toggle:
            pygame.draw.rect(background, BLANC, ((j + 1) * CZ, (i + 1) * CZ, CZ, CZ), 0)
        else:
            pygame.draw.rect(background, MARRON, ((j + 1) * CZ, (i + 1) * CZ, CZ, CZ), 0)
        toggle = not (toggle)
    toggle = not (toggle)

background.convert()


##################################################
# Préparer les pièces


def charger(filename):
    img = pygame.image.load(os.path.join(curdir, 'img', filename)).convert_alpha()
    return pygame.transform.scale(img, (CZ, CZ))


def get_image(piece):
    if piece == 'tn':
        return image_tn
    elif piece == 'cn':
        return image_cn
    elif piece == 'fn':
        return image_fn
    elif piece == 'dn':
        return image_dn
    elif piece == 'rn':
        return image_rn
    elif piece == 'pn':
        return image_pn
    elif piece == 'pb':
        return image_pb
    elif piece == 'rb':
        return image_rb
    elif piece == 'db':
        return image_db
    elif piece == 'fb':
        return image_fb
    elif piece == 'cb':
        return image_cb
    elif piece == 'tb':
        return image_tb


curdir = os.getcwd()
image_tn = charger('tour_noire.png')
image_cn = charger('cavalier_noir.png')
image_dn = charger('dame_noire.png')
image_rn = charger('roi_noir.png')
image_fn = charger('fou_noir.png')
image_pn = charger('pion_noir.png')
image_tb = charger('tour_blanche.png')
image_cb = charger('cavalier_blanc.png')
image_db = charger('dame_blanche.png')
image_rb = charger('roi_blanc.png')
image_fb = charger('fou_blanc.png')
image_pb = charger('pion_blanc.png')
####################################################

# Horloge pour contrôler le fps
clock = pygame.time.Clock()

# Gestion du déplacement
case_dep = ()
position = ()
piece_deplacee = None

# Boucle principale
continuer = True
while continuer:
    # Gestion des évènements
    # (comme la fermeture de la fenêtre)
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            continuer = False

        elif e.type == pygame.MOUSEBUTTONDOWN:  # Début
            # colonne et ligne de départ
            position = e.pos
            colonne = int(position[0] // CZ) - 1
            ligne = int(position[1] // CZ) - 1
            delta = (position[0] % CZ, position[1] % CZ)
            if not (0 <= ligne <= 7 and 0 <= colonne <= 7):
                continue

            # Vérifier s'il y a une pièce
            piece_deplacee = jeu.occupant(colonne, ligne)
            if piece_deplacee:  # pièce sélectionnée
                deplacement = True
                case_dep = (colonne, ligne)

        elif e.type == pygame.MOUSEMOTION:  # suivre le déplacement
            if piece_deplacee:
                position = e.pos

        elif e.type == pygame.MOUSEBUTTONUP:  # Fin
            if piece_deplacee:
                position = e.pos
                colonne = int(position[0] // CZ) - 1
                ligne = int(position[1] // CZ) - 1
                if not (0 <= ligne <= 7 and 0 <= colonne <= 7):
                    continue

                case_arrivee = (colonne, ligne)
                jeu.deplacer(case_dep, case_arrivee)
                piece_deplacee = None

    ##############################
    # Mises à jour des propriétés
    # du contenu

    #########################
    # Arrière-plan
    screen.blit(background, (0, 0))

    # Pièces statiques sur l'échiquier
    for i in range(len(jeu.plateau)):
        for j in range(len(jeu.plateau[i])):
            # ne pas dessiner la pièce déplacée
            if piece_deplacee and case_dep == (j, i):
                continue

            image = get_image(jeu.plateau[i][j])
            if image:
                screen.blit(image, ((j + 1) * CZ, (i + 1) * CZ))

    # Dessiner la pièce qui bouge
    if piece_deplacee:
        colonne, ligne = case_dep
        image = get_image(jeu.plateau[ligne][colonne])
        screen.blit(image, (position[0] - delta[0], position[1] - delta[1]))

    #########################
    # raffraichir l'affichage
    pygame.display.flip()

    # fps: ici 30 image par seconde
    clock.tick(30)

# Terminer l'application
pygame.quit()
quit()
