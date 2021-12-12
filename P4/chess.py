"""
Programme principal
S'exécute dans un environnement virtuel
"""

"""
1- Créer un tournoi
2- Ajouter 8 joueurs
3- Générer des paires de joueurs pour le premier tour
4- Entrer les résultats à la fin du tour
5- Répéter les étapes 3 et 4 jusqu'à ce que tous les tours soient joués
"""

from controller.controller import Controller
from models.data import Data
from models.tournament import Tournament
from models.player import Player
import pickle

def main():
    # mydb = Data()
    # tournaments = mydb.load_tournaments()
    # print(tournaments['2'].rounds)
    # print(tournaments['2'].singleton)
    # print(tournaments['2'].status)
    # tournaments['2'].status = "upcoming"
    # tournaments['2'].rounds = []
    # tournaments['2'].singleton = []
    # mydb.save_tournaments(tournaments)
    # exit()

    mycontroller = Controller()
    mycontroller.run()


if __name__ == "__main__":
    main()
