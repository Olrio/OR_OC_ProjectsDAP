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
        status="N/A",
        control_time="N/A",
        description="N/A",
    ):
        """initialization of a new tournament"""
        self.name = name
        self.town = town  # town location of the tournament
        self.country = country  # country location of the tournament
        self.id = self.get_id()  # unique identifiant of the tournament
        self.date_start = date_start  # starting date of the tournament.
        self.date_end = date_end  # ending date of the tournament (duration usually equals to one day)
        self.status = status  # ended / in progress / upcoming
        self.nb_rounds = 4  # number of rounds in the tournament
        self.control_time = control_time  # bullet, blitz or rapid
        self.description = description  # tournament director's comments
        # the following attributes shouldn't be modified by editing the tournament
        # modifications are enable by specific interactions or by the script itself
        self.rounds = []  # list of round instances
        self.players = []  # list of player instances
        self.first_half = []
        self.second_half = []
        self.dict_attributes = {
            "1": "name",
            "2": "town",
            "3": "country",
            "4": "id",
            "5": "date_start",
            "6": "date_end",
            "7": "status",
            "8": "nb_rounds",
            "9": "control_time",
            "10": "description",
        }
        self.label_attributes = {
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
        }
        self.number_attributes = {
            "Nom du tournoi": "1",
            "Ville": "2",
            "Pays": "3",
            "ID": "4",
            "Date de début": "5",
            "Date de fin": "6",
            "Statut": "7",
            "Nombre de rounds": "8",
            "Type de partie": "9",
            "Commentaires": "10",
        }

    def get_id(self):
        """
        consulting the list of saved tournaments
        create a list of id of all saved tournaments
        """
        self.list_id = Data().list_of_saved_tournaments_id()
        self.random_id = random.randint(1, 1000)
        while str(self.random_id) in self.list_id:
            self.random_id = random.randint(1, 1000)
        print(self.list_id)
        print(self.random_id)
        return str(self.random_id)

    def set_new_value(self, param, value):
        self.__setattr__(param, value)

    def __str__(self):
        return str(f"{self.name}")

    def add_date(self, date):
        self.date = date

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def sort_players(self):
        self.players.sort(key=lambda x: x.rank)  # players sorted by rank
        self.players.sort(
            key=lambda x: x.score, reverse=True
        )  # players sorted by score
        return self.players

    def first_round_sort_players(self):
        # players are divided in two equal groups : the x best players and the x latest players
        self.first_half = self.players.copy()
        while len(self.first_half) > len(self.second_half):
            self.second_half.append(self.first_half.pop())

        # players of the latest group are sorted by rank
        self.second_half.sort(key=lambda x: x.rank)

    def first_matchs(self):
        matchs = []
        for player1, player2 in zip(self.first_half, self.second_half):
            match = Match(player1, player2)
            matchs.append(match)
        return matchs

    def generate_round(self, newround):
        self.rounds.append(newround)
        print(f"{newround.name} : prochains matchs")
        for match in newround.matchs:
            print(match, match.player1.score, "-", match.player2.score, "\n")

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
