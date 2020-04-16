import pygame
from engine import Jeu

"""
Ce module ne s'occupe que de la partie graphique (dessiner le plateau, les pièce) 
et de l'interaction avec l'utilisateur (gestion de la souris et/ou du clavier)
"""

# Constantes utiles
WIDTH = 150
HEIGHT = 150
BLANC = (255,255,255)
NOIR = (0,0,0)

# Démarrer la bibliothèque
pygame.init()

# Création du jeu
jeu = Jeu()

# Définir la taille de la fenêtre en pixels
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

##################################################
# Préparer les images d'arrière plan et les pièces
bg = pygame.Surface((WIDTH,HEIGHT))
bg.fill(BLANC)
pygame.draw.line(bg, NOIR, (0,HEIGHT/3), (WIDTH,HEIGHT/3), 3)
pygame.draw.line(bg, NOIR, (0,2*HEIGHT/3), (WIDTH,2*HEIGHT/3), 3)
pygame.draw.line(bg, NOIR, (WIDTH/3,0), (WIDTH/3,HEIGHT), 3)
pygame.draw.line(bg, NOIR, (2*WIDTH/3,0), (2*WIDTH/3,HEIGHT), 3)

w = WIDTH/3-4
h = HEIGHT/3-4
croix = pygame.Surface((w,h))
croix.fill(BLANC)
pygame.draw.line(croix, NOIR, (w/4, h/4), (3*w/4, 3*h/4), 3)
pygame.draw.line(croix, NOIR, (w/4, 3*h/4), (3*w/4, h/4), 3)

cercle = pygame.Surface((w,h))
cercle.fill(BLANC)
pygame.draw.circle(cercle, NOIR, (int(w//2), int(h//2)), int(3*w//8), 3)
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

    elif e.type == pygame.MOUSEBUTTONDOWN: # Début
        # colonne et ligne de départ
        position = e.pos
        colonne = int(position[0]//(WIDTH/3))
        ligne = int(position[1]//(HEIGHT/3))
        delta = ( position[0]%int(WIDTH/3), position[1]%int(HEIGHT/3) )
        
        # Vérifier s'il y a une pièce
        piece_deplacee = jeu.occupant(colonne, ligne)
        if piece_deplacee != None: # pièce sélectionnée
            deplacement = True 
            case_dep = (colonne, ligne)

    elif e.type == pygame.MOUSEMOTION: # suivre le déplacement
        if piece_deplacee != None:
            position = e.pos

    elif e.type == pygame.MOUSEBUTTONUP: # Fin
        if piece_deplacee != None:
            position = e.pos
            colonne = int(position[0]//(WIDTH/3))
            ligne = int(position[1]//(HEIGHT/3))
            
            case_arrivee = (colonne, ligne)
            jeu.deplacer(case_dep, case_arrivee)
            piece_deplacee = None

  ##############################
  # Mises à jour des propriétés
  # du contenu
  
  
  #########################
  # Dessin du contenu
  screen.blit(bg, (0,0))
  for i in range(len(jeu.plateau)):
    for j in range(len(jeu.plateau[i])):
      # Ne pas dessiner la pièce qui se déplace
      if piece_deplacee!=None and (j,i)==case_dep:
          continue 

      if jeu.plateau[i][j]==1: # une croix
          screen.blit(croix, (j*WIDTH/3+2, i*HEIGHT/3+2))
      elif jeu.plateau[i][j]==2: # un cercle
          screen.blit(cercle, (j*WIDTH/3+2, i*HEIGHT/3+2))

  # Dessin de la pièce qui bouge
  if piece_deplacee == 1: # une croix
      screen.blit(croix, (position[0]-delta[0], position[1]-delta[1]) )
  elif piece_deplacee == 2: # un cercle
      screen.blit(cercle, (position[0]-delta[0], position[1]-delta[1]) )
  
  #########################  
  # raffraichir l'affichage
  pygame.display.flip()

  # fps: ici 30 image par seconde
  clock.tick(30)

# Terminer l'application
pygame.quit()
quit()
