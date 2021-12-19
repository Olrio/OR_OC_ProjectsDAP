import time

from models.data import DataLoader
from models.match import Match
from models.round import Round
from view.view import View

class MainController:
    """Global management of the app"""
    def __init__(self):
        self.tournament = None
        # instance sub controllers
        self.mm = MenuManager()
        self.dm = DataManager()

    def run(self):
        # loading all existing data
        self.mm.run()
        self.dm.get_data()
        # getting current tournament. May be created or chosen in the database
        self.tournament = self.mm.load_or_create_tournament(self.dm.tournaments)
        # running tournament
        if self.tournament.system == "swiss":
            self.run_swiss_first_round(self.tournament)
        else:
            self.run_other_system()

    def run_swiss_first_round(self, tournament):
        # display players participating in the tournament
        # players are sorted by score then by rank
        self.mm.show_players_in_tournament(tournament)
        # first round
        # players are distributed in two halves
        halves = tournament.rounds[0].two_halves(tournament.rounds[0].players, tournament)
        # generating matchs of the first round
        num_match = len(self.dm.matchs) + 1
        for player1, player2 in zip(halves[0], halves[1]):
            self.dm.matchs[str(num_match)] = Match()
            self.dm.matchs[str(num_match)].ident = str(num_match)
            self.dm.matchs[str(num_match)].data = ([player1, 0.0], [player2, 0.0])
            tournament.rounds[0].add_match(self.dm.matchs[str(num_match)])
            num_match += 1
        # manage floating player if number of players is odd
        if len(tournament.rounds[0].players) % 2 != 0:
            self.dm.matchs[str(num_match)] = Match()
            self.dm.matchs[str(num_match)].ident = str(num_match)
            self.dm.matchs[str(num_match)].data = ([tournament.singleton[-1], 0.0], [None, None])
            tournament.rounds[0].add_match(self.dm.matchs[str(num_match)])
            num_match += 1
        # manage matchs of the first round
        self.mm.matchs_of_the_round(tournament)
        # display ranking at the end of the round
        self.mm.show_players_in_tournament(tournament)
        # other rounds
        self.run_swiss_following_rounds(tournament)


    def run_swiss_following_rounds(self, tournament):
        while len(tournament.rounds) != tournament.nb_rounds:
            # each match has a unique identifiant and is stored in self.dm.matchs
            # matchs is a list of the matchs belonging to the next round
            num_match = len(self.dm.matchs) + 1
            matchs = []
            first_players = list(tournament.players)
            second_players = list(tournament.players)
            rev_i = -1
            if len(tournament.players) % 2 != 0:
                # if number of players is odd, a singleton is identified
                while tournament.players[rev_i] in tournament.singleton:
                    rev_i -= 1
                tournament.singleton.append(tournament.players[rev_i])
                first_players.remove(tournament.singleton[-1])
                second_players.remove(tournament.singleton[-1])

            while first_players:
                second_players.remove(second_players[0])
                x = 0
                appairing = 0

                while appairing == 0:  # a player can't play twice against the same opponent
                    flag = 0
                    self.dm.matchs[str(num_match)] = Match()
                    self.dm.matchs[str(num_match)].ident = str(num_match)
                    self.dm.matchs[str(num_match)].data = ([first_players[0], 0.0], [second_players[x], 0.0])
                    for t_round in tournament.rounds:
                        for past_match in t_round.matchs:
                            if (
                                    self.dm.matchs[str(num_match)].data[0][0] == past_match.data[0][0]
                                    and self.dm.matchs[str(num_match)].data[1][0] == past_match.data[1][0]
                                    or self.dm.matchs[str(num_match)].data[0][0] == past_match.data[1][0]
                                    and self.dm.matchs[str(num_match)].data[1][0] == past_match.data[0][0]
                            ):
                                if len(first_players) > 2:  # if no other possibility, player will play twice an opponent
                                    x += 1
                                    flag = 1
                                    break
                    if flag == 0:
                        appairing = 1

                matchs.append(self.dm.matchs[str(num_match)])  # only when appairing is correct
                first_players.remove(first_players[0])
                first_players.remove(second_players[x])
                second_players.remove(second_players[x])
                num_match += 1
            if len(tournament.players) % 2 != 0:  # adding a match with singleton
                self.dm.matchs[str(num_match)] = Match()
                self.dm.matchs[str(num_match)].ident = str(num_match)
                self.dm.matchs[str(num_match)].data = ([tournament.singleton[-1], 0.0], [None, None])
                matchs.append(self.dm.matchs[str(num_match)])

            num_round = len(self.dm.rounds) + 1
            self.dm.rounds[str(num_round)] = Round()  # create the new round
            self.dm.rounds[str(num_round)].ident = str(num_round)
            self.dm.rounds[str(num_round)].name = "Round "+str(num_round)
            self.dm.rounds[str(num_round)].players = tournament.players
            self.dm.rounds[str(num_round)].scores = dict()
            for player in self.dm.rounds[str(num_round)].players:
                self.dm.rounds[str(num_round)].scores[player.ident] = tournament.rounds[-1].scores[player.ident]
            self.dm.rounds[str(num_round)].matchs = matchs
            self.dm.rounds[str(num_round)].get_start_time()
            tournament.add_round(self.dm.rounds[str(num_round)])  # the new round is added to the tournament
            self.mm.matchs_of_the_round(tournament)
            self.mm.show_players_in_tournament(tournament)


def run_other_system(self):
        print("A implémenter ...")
        exit()


class MenuManager:
    """Management of the choices of the user"""
    def __init__(self):
        pass

    def run(self):
        self.ui = View()
        self.ui.home()

    def load_or_create_tournament(self, tournaments):
        choice = ""
        while choice.upper() not in ["L", "C"]:
            choice = self.ui.load_or_create_tournament()
        if choice.upper() == "L":
            print(f"OK, on charge la liste des tournois. Il n'y a actuellement que {tournaments['1'].name}")
        else:
            print(f"Création pas prête, on va prendre un tournoi existant : {tournaments['1'].name}")
        input()
        # so whatever the choice is, we suppose user chose to load the tournament Europe Grand Masters which ident is '1'
        return tournaments['1']

    def show_players_in_tournament(self, tournament):
        text = f"au {tournament.rounds[-1].name}"
        for match in tournament.rounds[-1].matchs:
            if match.data[0][1] == 0 and match.data[1][1] == 0: # round not ended
                break
            text = f"à l'issue du {tournament.rounds[-1].name} - Fin de la ronde :{tournament.rounds[-1].end}"
        tournament.rounds[-1].players = tournament.rounds[0].sort_players(tournament.rounds[-1].players)
        tournament.players = tournament.rounds[-1].sort_players(tournament.players)
        self.ui.show_players_in_tournament(tournament, text)

    def matchs_of_the_round(self, tournament):
        choice = ""
        valid_choice = ["N"]
        for match in tournament.rounds[-1].matchs:
            if match.data[1][0]:
                valid_choice.append(match.ident)
        while choice.upper() not in valid_choice:
            choice =self.ui.show_matchs_of_the_round(tournament)
        if choice.upper() == "N":
            # check if a result for every match exists
            for match in tournament.rounds[-1].matchs:
                if match.data[0][1] == 0.0 and match.data[1][1] == None:
                    match.data[0][1] = 1.0  # singleton marks 1 point
                    tournament.rounds[-1].scores[match.data[0][0].ident] += 1
                if match.data[0][1] == 0.0 and match.data[1][1] == 0.0:
                    self.ui.some_results_missing(tournament)
                    self.matchs_of_the_round(tournament)
            tournament.rounds[-1].get_end_time()
        for match in tournament.rounds[-1].matchs:
            if match.ident == choice:
                self.result_of_a_match(match, tournament)

    def result_of_a_match(self, match, tournament):
        choice = ""
        while choice.upper() not in ["C", "N", match.data[0][0].ident, match.data[1][0].ident]:
            choice = self.ui.result_of_a_match(match)
        if choice.upper() == "C":
            self.matchs_of_the_round(tournament)
        # check if a result has already been enterd for this match. If yes, reset scores
        if match.data[0][1] != 0 or match.data[1][1] != 0:
            tournament.rounds[-1].scores_reset(match)
        if choice.upper() == "N":
            match.set_draw()
        elif choice.upper() == match.data[0][0].ident:
            match.set_victory_1()
        elif choice.upper() == match.data[1][0].ident:
            match.set_victory_2()
        tournament.rounds[-1].scores_update(match)
        self.matchs_of_the_round(tournament)


class DataManager:
    """Management of all data in the app"""
    def __init__(self):
        self.players = None
        self.matchs = None
        self.rounds = None
        self.tournaments = None

    def get_data(self):
        '''loading players, matchs, rounds, tournaments from database'''
        self.players = DataLoader().get_players(dict())
        self.matchs = DataLoader().get_matchs(dict(), self.players)
        self.rounds = DataLoader().get_rounds(dict(), self.matchs, self.players)
        self.tournaments = DataLoader().get_tournaments(dict(), self.rounds, self.players)
