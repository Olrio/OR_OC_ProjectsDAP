"""
Gestion de la classe Round
correspondant à un tour dans un tournoi d'échecs
Un round comprend plusieurs matchs opposant tous les joueurs deux à deux
"""
import datetime


class Round:
    def __init__(self):
        """ensemble des parties jouées durant une ronde"""
        self.name = str()
        self.scores = dict()  # dict of identifiants of the players participating in the round and their score in the round
        self.players = list()
        self.matchs = list()  # list of identifiants of the matchs in the round
        self.ident = str()
        self.start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end = None

    def get_translation(self, lang):
        if lang == "fr":
            return {
                "name": "Nom",
                "scores": "Scores des joueurs",
                "sorted_players": "Liste triée des joueurs",
                "matchs": "Liste des matchs",
                "ident": "Identifiant",
            }

    def add_player_score(self, player):
        if player not in self.scores:
            self.scores[player] = 0

    def add_match(self, match):
        if match not in self.matchs:
            self.matchs.append(match)

    def sort_players(self, players):
        self.players = sorted(self.scores, key=lambda x: players[x].rank)  # by rank
        self.players = sorted(self.players, key=lambda x: self.scores[x], reverse=True)

    def two_halves(self, players, tournament):
        # distribute players in best half and lowest half
        first_half = self.players.copy()
        second_half = []

        # verify if number of players is odd number
        # player with the lowest score/rank is singleton for this round
        # player can be singleton only once
        rev_i = -1
        if len(self.players) % 2 != 0:
            while self.players[rev_i] in tournament.singleton:
                rev_i -= 1
            tournament.singleton.append(self.players[rev_i])
            first_half.remove(self.players[rev_i])

        while len(first_half) > len(second_half):
            second_half.append(first_half.pop())
        # players of the latest group are sorted by rank
        second_half.sort(key=lambda x: players[x].rank)
        return first_half, second_half

    def scores_update(self, match):
        self.scores[match.data[0][0]] += match.data[0][1]
        if match.data[1][0]:
            self.scores[match.data[1][0]] += match.data[1][1]

    def get_end_time(self):
        self.end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
