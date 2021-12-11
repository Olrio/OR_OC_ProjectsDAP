"""
Management of a tournament
"""

import random
from models.match import Match
from models.data import Data


class Tournament:
    def __init__(
        self,
        name,
        town,
        country,
        date_start="N/A",
        date_end="N/A",
        status="upcoming",
        control_time="N/A",
        description="N/A",
        system="swiss",
            lang="fr"
    ):
        """initialization of a new tournament"""
        self.name = name
        self.town = town  # town location of the tournament
        self.country = country  # country location of the tournament
        self.id = self.get_id()  # unique identifiant of the tournament
        self.date_start = date_start  # starting date of the tournament.
        self.date_end = date_end  # ending date of the tournament (duration usually equals to one day)
        self.status = status  # 'upcoming' is default, options are 'in progress' and 'ended'
        self.nb_rounds = 4  # number of rounds in the tournament
        self.control_time = control_time  # bullet, blitz or rapid
        self.description = description  # tournament director's comments
        self.system = system # "swiss" by default
        self.translation = self.get_translation(lang)
        # the following attributes shouldn't be modified by editing the tournament
        # modifications are enable by specific interactions or by the script itself
        self.rounds = []  # list of round instances
        self.players = []  # list of player instances
        self.scores = {}
        self.first_half = []
        self.second_half = []

    def get_id(self):
        """
        consulting the list of saved tournaments
        create a list of id of all saved tournaments
        """
        list_id = Data().list_of_saved_tournaments_id()
        return str(len(list_id))

    def get_translation(self, lang):
        if lang == "fr":
            return {
            "name": "Nom du tournoi",
            "town": "Ville",
            "country": "Pays",
            "id": "ID",
            "date_start": "Date de début",
            "date_end": "Date de fin",
            "status": "Statut",
            "nb_rounds": "Nombre de rounds",
            "control_time": "Type de partie",
            "description": "Commentaires",
            "system" : "Système",
                "scores": "Scores"
        }

    def set_new_value(self, param, value):
        self.__setattr__(param, value)

    def __str__(self):
        return str(f"{self.name}")

    def add_player(self, player):
        self.players.append(player)
        self.scores[player] = 0

    def remove_player(self, player):
        self.players.remove(player)
        del(self.scores[player])

    def sort_players(self):
        self.players.sort(key=lambda x: x.rank)  # players sorted by rank
        self.players.sort(
            key=lambda x: x.score, reverse=True
        )  # players sorted by score
        return self.players

    def generate_round(self, newround):
        for round in self.rounds:
            if newround.name == round.name:
                return
        self.rounds.append(newround)

    @staticmethod
    def generate_results(currentround):
        print(f"{currentround.name} : résultats")
        for match in currentround.matchs:
            print(f"Match opposant {match.player1} et {match.player2}")
            ecart = match.player2.rank - match.player1.rank
            maxrank = 30
            chance_draw = 0.33 - 0.66 * (ecart / (2 * maxrank))
            chance_win = 0.33 + 0.66 * (ecart / maxrank)
            seuil1 = int(1000 * chance_win)
            seuil2 = 1000 - int(1000 * chance_draw)
            result = random.randrange(1, 1000)
            if result <= seuil1:
                print(f"Victoire de {match.player1} \n")
                match.score1 += 1
                match.player1.score += 1
            elif result >= seuil2:
                print(f"Victoire de {match.player2} \n")
                match.score2 += 1
                match.player2.score += 1
            else:
                print(f"Match nul entre {match.player1} et {match.player2} \n")
                match.score1 += 0.5
                match.score2 += 0.5
                match.player1.score += 0.5
                match.player2.score += 0.5

    def display_scores(self):
        for player in self.players:
            print(player, player.score)
        print("________\n")

    def other_matchs(self):
        matchs = []
        first_players = list(self.players)
        second_players = list(self.players)

        while first_players:
            second_players.remove(second_players[0])
            x = 0
            appairing = 0
            match = None

            while appairing == 0:
                flag = 0
                match = Match(first_players[0], second_players[x])
                for myround in self.rounds:
                    for past_match in myround.matchs:
                        if (
                            match.player1 == past_match.player1
                            and match.player2 == past_match.player2
                            or match.player1 == past_match.player2
                            and match.player2 == past_match.player1
                        ):
                            if len(first_players) > 2:
                                x += 1
                                flag = 1
                                break
                if flag == 0:
                    appairing = 1

            matchs.append(match)
            first_players.remove(first_players[0])
            first_players.remove(second_players[x])
            second_players.remove(second_players[x])
        return matchs
