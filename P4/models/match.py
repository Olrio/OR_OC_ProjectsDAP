"""
Gestion de la classe Match
correspondant à une partie entre deux joueurs
"""


class Match:
    def __init__(self, player1, player2):
        """Partie entre deux joueurs"""
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0  # score du joueur 1 à l'issue de la partie  = 0/+1/+0.5
        self.score2 = 0  # score du joueur 2 à l'issue de la partie  = +1/0/+0.5
        self.match = (
            [self.player1, self.player1.score],
            [self.player2, self.player2.score],
        )

    def __str__(self):
        match_str = (
            f"Match opposant {self.player1.firstname} {self.player1.lastname} et "
            f"{self.player2.firstname} {self.player2.lastname}"
        )
        return match_str
