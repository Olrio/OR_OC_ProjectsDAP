"""
Programme principal
S'exécute dans un environnement virtuel
"""

from controller.controller import Controller


def main():
    mycontroller = Controller()
    mycontroller.run()


if __name__ == "__main__":
    main()
