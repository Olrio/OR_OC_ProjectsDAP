"""
Gestion de la classe Match
correspondant à une partie entre deux joueurs
"""


class Match:
    def __init__(self, player1, player2, tournament):
        """Partie entre deux joueurs"""
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0  # score du joueur 1 à l'issue de la partie  = 0/+1/+0.5
        self.score2 = 0  # score du joueur 2 à l'issue de la partie  = +1/0/+0.5
        self.match = (
            [self.player1, tournament.scores[self.player1]],
            [self.player2, tournament.scores[self.player2]],
        )

    def __str__(self):
        match_str = (
            f"Match : {self.player1.firstname:>15} {self.player1.lastname:<15} -"
            f"{self.player2.firstname:>15} {self.player2.lastname:<15}"
        )
        return match_str
