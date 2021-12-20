
from models.data import DataLoader
from view.view import View
from models.crud import Crud

class MainController:
    """
    Global management of the app
    MainController interacts with MenuManager
    and MenuManager interacts with DataManager
    """
    def __init__(self):
        # instance sub controller
        self.mm = MenuManager()

    def run(self):
        # launching program
        self.mm.run()
        #self.mm.run_home()
        self.run_tournament()

    def run_tournament(self):
        # MainController needs a tournament. It may be created or chosen in the database
        # This tournament must have players
        tournament = self.mm.load_or_create_tournament()
        # running tournament
        if tournament.system == "swiss":
            self.run_swiss_first_round(tournament)
        else:
            self.run_other_system()

    def run_player(self):
        print("Menu Joueur")
        exit()

    def run_reports(self):
        print("Menu Rapports")
        exit()

    def run_swiss_first_round(self, tournament):
        # create a first round if needed
        if len(tournament.rounds) == 0:
            self.mm.dm.create_round(tournament, self.mm.dm.rounds)
        # display players participating in the tournament
        # players are sorted by score then by rank
        self.mm.show_players_in_tournament(tournament)
        # creating matchs for the first round
        self.mm.dm.create_matchs_swiss_first_round(tournament)
        # manage matchs of the first round
        self.mm.matchs_of_the_round(tournament)
        # display ranking at the end of the round
        self.mm.show_players_in_tournament(tournament)
        # other rounds
        self.run_swiss_following_rounds(tournament)


    def run_swiss_following_rounds(self, tournament):
        while len(tournament.rounds) != tournament.nb_rounds:
            self.mm.dm.create_matchs_swiss_following_round(tournament)
            self.mm.matchs_of_the_round(tournament)
            self.mm.show_players_in_tournament(tournament)


def run_other_system(self):
        print("Coming soon ...")
        exit()


class MenuManager:
    """
    Management of the choices of the user
    i.e. views and menus
    """
    def __init__(self):
        pass

    def run(self):
        self.ui = View()
        self.ui.home()
        self.dm = DataManager()
        self.dm.get_database()

    def run_home(self):
        valid_choice = ["T", "P", "R", "Q"]
        choice = ""
        while choice.upper() not in valid_choice:
            choice = self.ui.menu_home()
        if choice.upper() == "Q":
            exit()
        elif choice.upper() == "T":
            pass
        elif choice.upper() == "P":
            pass
        elif choice.upper() == "R":
            pass


    def load_or_create_tournament(self):
        choice = ""
        while choice.upper() not in ["L", "C", "Q", "H"]:
            choice = self.ui.load_or_create_tournament()
        if choice.upper() == "Q":
            exit()
        if choice.upper() == "H":
            exit()
        if choice.upper() == "L":
            tournament = self.load_tournament()
        else:
            data = self.ui.get_data_new_tournament()
            tournament = self.dm.create_tournament(data, self.dm.tournaments)
        # if no player in tournament, add some
        if not tournament.players:
            self.ui.no_player_in_tournament(tournament)
            self.how_add_players_to_tournament(tournament)
        return tournament

    def how_add_players_to_tournament(self, tournament):
        choice = ""
        while choice.upper() not in ["L", "C", "H", "Q"]:
            choice = self.ui.load_or_create_player()
        if choice.upper() == "Q":
            exit()
        if choice.upper() == "H":
            exit()
        if choice.upper() == "L":
            self.load_player_for_tournament(tournament)
        else:
            data = self.ui.get_data_new_player()
            player = self.dm.create_player(data, self.dm.players)
            self.dm.add_or_remove_a_player_to_tournament(player.ident, tournament)
        choice = ""
        while choice.upper() not in ["Y", "N"]:
            choice = self.ui.add_another_player()
        if choice.upper() == "Y":
            self.how_add_players_to_tournament(tournament)
        else:
            if len(tournament.players) >= 2:
                return tournament
            else:
                self.ui.not_enought_players_in_tournament(tournament)
                self.how_add_players_to_tournament(tournament)

    def load_tournament(self):
        valid_choice = ["C"]
        t_choice = ""
        for tournament in self.dm.tournaments.values():
            valid_choice.append(tournament.ident)
        while t_choice.upper() not in valid_choice:
            t_choice = self.ui.display_all_tournaments(self.dm.tournaments)
        if t_choice.upper() == "C":
            self.load_or_create_tournament()
        else:
            return self.dm.load_tournament(t_choice)


    def load_player_for_tournament(self, tournament):
        valid_choice = ["C", "N"]
        p_choice = ""
        for player in self.dm.players.values():
            valid_choice.append(player.ident)
        while p_choice.upper() not in valid_choice:
            p_choice = self.ui.display_all_players(self.dm.players, tournament)
        if p_choice.upper() == "C":
            while tournament.players:
                self.dm.add_or_remove_a_player_to_tournament(tournament.players[-1].ident, tournament)
            self.how_add_players_to_tournament(tournament)
        elif p_choice.upper() == "N":
            return
        else:
            self.dm.add_or_remove_a_player_to_tournament(p_choice, tournament)
            self.load_player_for_tournament(tournament)


    def show_players_in_tournament(self, tournament):
        text = f"pour la ronde {len(tournament.rounds)}"
        for match in tournament.rounds[-1].matchs:
            if match.data[0][1] == 0 and match.data[1][1] == 0: # round not ended
                break
            text = f"à l'issue de la ronde {len(tournament.rounds)} - Fin de la ronde :{tournament.rounds[-1].end}"
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
        self.crud = Crud()

    def get_database(self):
        '''loading players, matchs, rounds, tournaments from database'''
        self.players = DataLoader().get_players(dict())
        self.matchs = DataLoader().get_matchs(dict(), self.players)
        self.rounds = DataLoader().get_rounds(dict(), self.matchs, self.players)
        self.tournaments = DataLoader().get_tournaments(dict(), self.rounds, self.players)

    def create_tournament(self, data, tournaments):
        tournament = self.crud.create_tournament(data, tournaments)
        return tournament

    def create_player(self, data, players):
        player = self.crud.create_player(data, players)
        return player

    def create_round(self, tournament, rounds):
        round = self.crud.create_round(tournament, rounds)
        # a round has to be added to a tournament
        tournament.add_round(round)
        return tournament

    def create_matchs_swiss_first_round(self, tournament):
        # players are distributed in two halves
        halves = tournament.rounds[0].two_halves(tournament.rounds[0].players, tournament)
        # generating matchs of the first round
        num_match = len(self.matchs) + 1
        for player1, player2 in zip(halves[0], halves[1]):
            match = self.crud.create_match(self.matchs, player1, player2)
            tournament.rounds[0].add_match(match)
        # manage floating player if number of players is odd
        if len(tournament.rounds[0].players) % 2 != 0:
            match = self.crud.create_match(self.matchs, tournament.singleton[-1], None, score2=None)
            tournament.rounds[0].add_match(match)

    def create_matchs_swiss_following_round(self, tournament):
        # each match has a unique identifiant and is stored in self.matchs
        # matchs is a list of the matchs belonging to the next round
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
                match = self.crud.create_match(self.matchs, first_players[0], second_players[x])
                for t_round in tournament.rounds:
                    for past_match in t_round.matchs:
                        if (
                                match.data[0][0] == past_match.data[0][0]
                                and match.data[1][0] == past_match.data[1][0]
                                or match.data[0][0] == past_match.data[1][0]
                                and match.data[1][0] == past_match.data[0][0]
                        ):
                            if len(first_players) > 2:  # if no other possibility, player will play twice an opponent
                                x += 1
                                flag = 1
                                break
                if flag == 0:
                    appairing = 1

            matchs.append(match)  # only when appairing is correct
            first_players.remove(first_players[0])
            first_players.remove(second_players[x])
            second_players.remove(second_players[x])
        if len(tournament.players) % 2 != 0:  # adding a match with singleton
            match = self.crud.create_match(self.matchs, tournament.singleton[-1], None, score2=None)
            matchs.append(match)

        round = self.crud.create_round(tournament, self.rounds)
        round.matchs = matchs
        tournament.add_round(round)  # the new round is added to the tournament

    def add_or_remove_a_player_to_tournament(self, player_ident, tournament):
        if self.players[player_ident] in tournament.players:
            tournament.remove_player(self.players[player_ident])
        else:
            tournament.add_player(self.players[player_ident])

    def load_tournament(self, tournament_id):
        return self.tournaments[tournament_id]
