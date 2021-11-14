"""
Création de 8 joueurs pour un tournoi
"""


def get_players():
    player_list = []
    prof = ("Prof", "Albert", 1)
    grincheux = ("Grincheux", "Patrick", 17)
    simplet = ("Simplet", "Victor", 25)
    timide = ("Timide", "Jean-Pierre", 51)
    distrait = ("Distrait", "Marc", 65)
    joyeux = ("Joyeux", "Anatole", 83)
    dormeur = ("Dormeur", "Casimir", 99)
    neige = ("Neige", "Blanche", 2)

    player_list.extend([prof, grincheux, simplet, timide, distrait, joyeux, dormeur, neige])

    return player_list



