"""
Programme principal
S'exécute dans un environnement virtuel
"""

from controller.controller import Controller

from models.player import Player
from models.tournament import Tournament
from models.data import Data


def main():
    mycontroller = Controller()
    mycontroller.run()



if __name__ == "__main__":
    main()
