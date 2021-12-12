"""
Management of the database for the application
"""

import pickle


class Data:
    """database"""

    def __init__(self):
        self.players = {}
        self.tournaments = {}

    @staticmethod
    def save_program(historic, tournaments, tournament, player):
        """save the state of the program"""
        with open("data/state", "wb") as file_program:
            if tournament:
                t_id = tournament.id
            else:
                t_id = None
            pickle.dump((historic, player, t_id), file_program)
        with open("data/tournaments", "wb") as file_program:
            pickle.dump(tournaments, file_program)

    @staticmethod
    def load_program():
        """save the state of the program"""
        with open("data/state", "rb") as file_program:
            data_state = pickle.load(file_program)
        with open("data/tournaments", "rb") as file_program:
            tournaments = pickle.load(file_program)
            if data_state[2]:
                tournament = tournaments[data_state[2]]
            else:
                tournament = None
        state_program = (data_state[0], tournaments, tournament, data_state[1])
        return state_program

    def add_tournament(self, tournament):
        """add a new tournament to the list of tournaments"""
        if tournament not in self.tournaments.values():
            self.tournaments[tournament.id] = tournament

    @staticmethod
    def save_tournaments(tournaments):
        """save the list of tournaments in a file"""
        try:
            with open("data/tournaments", "rb") as file_tournaments:
                already_saved_files = pickle.load(file_tournaments)
            if already_saved_files:
                already_saved_files.update(tournaments)
            else:
                already_saved_files = tournaments
        except FileNotFoundError:
            already_saved_files = tournaments
        with open("data/tournaments", "wb") as file_tournaments:
            pickle.dump(already_saved_files, file_tournaments)

    def load_tournaments(self):
        """load the dict of tournaments from a file"""
        try:
            with open("data/tournaments", "rb") as file_tournaments:
                self.tournaments = pickle.load(file_tournaments)
            return self.tournaments
        except FileNotFoundError:
            return FileNotFoundError

    @staticmethod
    def list_of_saved_tournaments_id():
        id_list = []
        try:
            with open("data/tournaments", "rb") as file_tournaments:
                saved_tournaments = pickle.load(file_tournaments)
            if saved_tournaments:
                for tournament in saved_tournaments.values():
                    id_list.append(tournament.id)
        except FileNotFoundError:
            pass
        return id_list

    @staticmethod
    def list_of_saved_players_id():
        id_list = []
        with open("data/players", "rb") as file_players:
            saved_players = pickle.load(file_players)
        for player in saved_players.values():
            id_list.append(player.id)
        return id_list

    def add_players(self, player):
        """add a new player to the whole list of players"""
        self.players[player.id] = player

    def get_players(self):
        """get the whole list of players"""
        return self.players

    @staticmethod
    def save_players(players):
        with open("data/players", "rb") as file_players:
            already_saved_files = pickle.load(file_players)
        already_saved_files.update(players)
        with open("data/players", "wb") as file_players:
            pickle.dump(already_saved_files, file_players)

    def load_players(self):
        with open("data/players", "rb") as file_players:
            self.players = pickle.load(file_players)
        return self.players
