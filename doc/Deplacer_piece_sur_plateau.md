# Déplacement d'une pièce sur un plateau

Partons d'une version modifiée du jeu de Tic Tac Toe monoposte  où 2 pièces sont déjà disposées aux cellules (0,0) et (0,1) :

<svg width="150" height="150" style="border: 1px solid black;">
    <path stroke="black" d="M 50 0 V 150 M 100 0 V 150 M 0 50 H 150 M 0 100 H 150" />
    <path stroke="black" stroke-width="3" d="M 0 0 m 12 12 l 24 24 m 0 -24 l -24 24" />
    <circle stroke="black" stroke-width="3" cx="75" cy="25" r="15" fill="None"/>
</svg>

## I. Fonctionnement interne

(*classe `Jeu` dans le module `engine.py`*)

En POO (*Programmation Orientée Objet*), le jeu doit modifier lui-même ses valeurs et non pas le module graphique. La classe `Jeu` doit donc fournir 2 nouveaux services (= 2 nouvelles méthodes):

- `occupation` pour vérifier si une case donnée est libre et, si non, indiquer la pièce qui l'occupe

  ```python
  def occupant(self, colonne, ligne):
      if self.plateau[ligne][colonne]==0: # case vide
          return None
      else: # case occupée
          return self.plateau[ligne][colonne]
  ```

- `deplacer` pour changer l'emplacement d'une pièce (suite à un déplacement graphique). Ses paramètres sont les emplacements de départ (colonne, ligne) et d'arrivée (colonne, ligne)

  ```python
  def deplacer(self, dep, arr):
      if self.plateau[arr[1]][arr[0]]==0: # case arrivée libre
          # recopier le type de pièce
          self.plateau[arr[1]][arr[0]] = self.plateau[dep[1]][dep[0]]
          # vider la case de départ
          self.plateau[dep[1]][dep[0]] = 0
  ```

> Remarque: d'autres critères que case d'arrivée libre pourraient être ajoutés dans la méthode `deplacer` (par exemple, n'autoriser qu'un déplacement vertical, ou horizontal, ou que d'une seule case...)

## II. Partie graphique

(*module `gui.py`*)

On utilise :

- `case_dep` (*tuple*) pour mémoriser (colonne, ligne) de la case de départ:
  - pour ne plus dessiner la pièce déplacée dans sa case de départ (même si elle s'y trouve toujours dans le tableau `jeu.plateau`)
  - pour y revenir si le déplacement n'est finalement pas valide.
- `position` (tuple) pour mémoriser (x,y) de la position courante de la souris.
- `piece_deplacee` (`None` si pas de déplacement en cours) pour mémoriser le type de pièce à déplacer (pour dessiner la pièce en cours de déplacement).

Le déplacement via la souris fait intervenir 3 événements (instructions à placer dans la boucle de gestion des événements):

> Rappel: les indices de colonne et de lignes s'obtiennent en divisant les coordonnées de la souris par la taille d'une case (et on ne garde que la partie entière).


1. `pygame.MOUSEBUTTONDOWN`: sélection de la pièce.

   ```python
   elif e.type == pygame.MOUSEBUTTONDOWN: # Début
       # colonne et ligne de départ
       position = e.pos
       colonne = int(position[0]//(WIDTH/3))
       ligne = int(position[1]//(HEIGHT/3))
       
       # Vérifier s'il y a une pièce
       piece_deplacee = jeu.occupant(colonne, ligne)
       if piece_deplacee != None: # pièce sélectionnée
           deplacement = True 
           case_dep = (colonne, ligne)
   ```

2. `pygame.MOUSEMOTION`: déplacement de la pièce.

   ```python
   elif e.type == pygame.MOUSEMOTION: # suivre le déplacement
       if piece_deplacee != None:
           position = e.pos
   ```

3. `pygame.MOUSEBUTTONUP`: dépose de la pièce.

   ```python
   elif e.type == pygame.MOUSEBUTTONUP: # Fin
       if piece_deplacee != None:
           position = e.pos
           colonne = int(position[0]//(WIDTH/3))
           ligne = int(position[1]//(HEIGHT/3))
           
   		case_arrivee = (colonne, ligne)
           jeu.deplacer(case_dep, case_arrivee)
           piece_deplacee = None
   ```

Dans la partie *Dessin du contenu*, il faut:

- Arrêter de dessiner la pièce dans sa case départ lors d'un déplacement (dans la double boucle de dessin du plateau):

  ```python
  # Ne pas dessiner la pièce qui se déplace
  if piece_deplacee!=None and (j,i)==case_dep:
    continue
  ```

- Dessiner la pièce qui se déplace à la bonne position:

  ```python
  # Dessin de la pièce qui bouge
  if piece_deplacee == 1: # une croix
      screen.blit(croix, position)
  elif piece_deplacee == 2: # un cercle
      screen.blit(cercle, position)
  ```

  