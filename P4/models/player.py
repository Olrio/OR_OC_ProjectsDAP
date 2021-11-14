"""
Gestion de la classe Joueur
"""

class Player:
    def __init__(self, data_player):
        """initialise un nouveau joueur"""
        self.lastname = data_player[0]  # nom de famille
        self.firstname = data_player[1]
        self.birthdate = None
        self.gender = None
        self.rank = data_player[2]
        self.score = 0

    def modify_rank(self, rank):
        """possibilité de modifier manuellement le rang d'un joueur"""
        self.rank = rank

    def __str__(self):
        return (f"{self.lastname}, {self.firstname} ({self.rank})")