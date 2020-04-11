"""
Ce module s'occupe du fonction interne du jeu.
Il ne doit surtout pas supposer qu'il existe une interface
graphique.
"""
import sys
import socket
import random
import threading

class Jeu:

  def __init__(self):
    # Version simplifiée
    if len(sys.argv)==2 and sys.argv[1]=="client":
      self.serveur = False
      print("Mode client")
    else:
      self.serveur = True
      print("Mode serveur")

    # Création des sockets
    if self.serveur: # Mode serveur
      listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      listen_socket.bind( ('', 7175) ) # 7175: valeur arbitraire
      listen_socket.listen(1) # Attendre 1 seul client
      print("Attente du client...")

      self.local_socket, remote_socket = listen_socket.accept()
      print("Connecté avec", remote_socket)
    else: # Mode client
      self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.local_socket.connect(('127.0.0.1', 7175))
      remote_socket = self.local_socket.getpeername()
      print("Connecté avec", remote_socket)

    # 1ère communication (détermination 1er joueur)
    if self.serveur: # Le serveur choisit et envoit le résultat
      if random.random()>0.5: # valeur entre 0 et 1
        self.joueur = 1
        adversaire = '2'
      else:
        self.joueur = 2
        adversaire = '1'
      # Envoi d'un octet
      message = bytes(adversaire, 'ascii') # conversion en octet
      self.local_socket.sendall(message)
    else: # le client reçoit son numéro de joueur
      # Réception d'1 octet
      message = self.local_socket.recv(1)
      self.joueur = int(message.decode('ascii')) # conversion ascii puis int

    # Après la 1ère communication
    self.reception = Reception(self) # envoi du jeu au Thread
    self.reception.start() # démarrer le thread

    # Contenu des cellules:
    # 0: case vide
    # 1: croix
    # 2: cercle
    self.plateau = [
      [0,0,0],
      [0,0,0],
      [0,0,0],
    ]

    # 2 joueurs 1 (croix) et 2 (cercle)
    self.fin = (False, 0)

    # Prochain joueur
    if self.joueur==1:
      self.mon_tour = True
    else:
      self.mon_tour = False
    print('Joueur', self.joueur)

  def maj(self, c, l):
    if self.plateau[l][c]!=0: # case non libre
      return
    else: # case libre
      if self.mon_tour: # joueur local
        self.plateau[l][c] = self.joueur
        # envoyer à l'adversaire
        message = str(c) + str(l)
        self.local_socket.sendall(bytes(message, 'ascii'))
      else: # joueur distant
        self.plateau[l][c] = 2 - (self.joueur-1)

    # Victoire ?
    self.fin = self.victoire()

    if self.fin[0]: # Victoire
      self.mon_tour = False # enlever la main
      self.reception.stop() # arrêter la réception
    else: # Passer au joueur suivant
      self.mon_tour = not self.mon_tour

  def victoire(self):
        """
        Vérifier si un joueur a gagné
        """
        
        # variable locale (plus rapide)
        p  = self.plateau 
        
        # Vérification des lignes et colonnes
        for i in range(3):
            if p[i][0]!=0 and p[i][0]==p[i][1]==p[i][2]:
                return (True, p[i][0])
            if p[0][i]!=0 and p[0][i]==p[1][i]==p[2][i]:
                return (True, p[0][i])
        # Vérifier les diagonales
        if p[0][0]!=0 and p[0][0]==p[1][1]==p[2][2]:
            return (True, p[0][0])
        if p[2][0]!=0 and p[2][0]==p[1][1]==p[0][2]:
            return (True, p[2][0])
        return (False, 0)

class Reception(threading.Thread):
  def __init__(self, j): # j correspond au jeu
    threading.Thread.__init__(self)
    self.jeu = j # mémorisation
    self.continuer = True # pour la boucle sans fin

  def stop(self): # méthode pour arrêter la boucle sans fin
    self.continuer = False

  def run(self): # instructions à exécuter dans le thread
    while self.continuer:
      # Attendre de recevoir 2 caractères (colonne + ligne du coup)
      message = self.jeu.local_socket.recv(2)
      recu = message.decode('ascii') # convertir en chaîne
      self.jeu.maj(int(recu[0]), int(recu[1])) # colonne, ligne (entiers)