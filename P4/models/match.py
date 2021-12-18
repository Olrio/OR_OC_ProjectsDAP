"""
Gestion de la classe Match
correspondant à une partie entre deux joueurs
"""

import random

class Match:
    def __init__(self):
        """Partie entre deux joueurs"""
        self.data = tuple()  # format = ([player1, score1], [player2, score2])
        self.ident = str()

    def get_translation(self, lang):
        if lang == "fr":
            return {
                "data": "Informations sur le match",
                "ident": "Identifiant du match"
            }

    def random_result(self, players):
        if not self.data[1][0]:
            print(f"Match N° {self.ident} : Le joueur flottant {players[self.data[0][0]]} marque 1 point")
            self.data[0][1] += 1
        else:
            print(f"Match N° {self.ident} : {players[self.data[0][0]]} vs {players[self.data[1][0]]}")
            ecart = abs(players[self.data[0][0]].rank - players[self.data[1][0]].rank)
            maxrank = 1000
            chance_draw = 0.33 - 0.66 * (ecart / (2 * maxrank))
            chance_win = 0.33 + 0.66 * (ecart / maxrank)
            seuil1 = int(1000 * chance_win)
            seuil2 = 1000 - int(1000 * chance_draw)
            result = random.randrange(1, 1000)
            if result <= seuil1:
                print(f"Victoire de {players[self.data[0][0]]} \n")
                self.data[0][1] += 1
            elif result >= seuil2:
                print(f"Victoire de {players[self.data[1][0]]} \n")
                self.data[1][1] += 1
            else:
                print(f"Match nul entre {players[self.data[0][0]]} et {players[self.data[1][0]]} \n")
                self.data[0][1] += 0.5
                self.data[1][1] += 0.5
