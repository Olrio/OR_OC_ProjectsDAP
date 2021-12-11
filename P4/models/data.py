"""
Management of the database for the application
"""

import pickle


class Data:
    """database"""

    def __init__(self):
        self.players = {}
        self.tournaments = {}

    def save_program(self, historic, tournaments, tournament, player):
        """save the state of the program"""
        with open("data/state", "wb") as file_program:
            if tournament:
                id = tournament.id
            else:
                id = None
            pickle.dump((historic, player, id), file_program)
        with open("data/tournaments", "wb") as file_program:
            pickle.dump(tournaments, file_program)

    def load_program(self):
        """save the state of the program"""
        with open("data/state", "rb") as file_program:
            self.data_state = pickle.load(file_program)
        with open("data/tournaments", "rb") as file_program:
            self.tournaments = pickle.load(file_program)
            if self.data_state[2]:
                self.tournament = self.tournaments[self.data_state[2]]
            else:
                self.tournament = None
        self.state_program = (self.data_state[0], self.tournaments, self.tournament, self.data_state[1])
        return self.state_program

    def add_tournament(self, tournament):
        """add a new tournament to the list of tournaments"""
        if tournament not in self.tournaments.values():
            self.tournaments[tournament.id] = tournament

    def save_tournaments(self, tournaments):
        """save the list of tournaments in a file"""
        try:
            with open("data/tournaments", "rb") as file_tournaments:
                self.already_saved_files = pickle.load(file_tournaments)
            if self.already_saved_files:
                self.already_saved_files.update(tournaments)
            else:
                self.already_saved_files = tournaments
        except FileNotFoundError:
            self.already_saved_files = tournaments
        with open("data/tournaments", "wb") as file_tournaments:
            pickle.dump(self.already_saved_files, file_tournaments)

    def load_tournaments(self):
        """load the dict of tournaments from a file"""
        try:
            with open("data/tournaments", "rb") as file_tournaments:
                self.tournaments = pickle.load(file_tournaments)
            return self.tournaments
        except FileNotFoundError :
            return FileNotFoundError

    def list_of_saved_tournaments_id(self):
        self.id_list = []
        try:
            with open("data/tournaments", "rb") as file_tournaments:
                self.saved_tournaments = pickle.load(file_tournaments)
            if self.saved_tournaments:
                for tournament in self.saved_tournaments.values():
                    self.id_list.append(tournament.id)
        except FileNotFoundError:
            pass
        return self.id_list

    def list_of_saved_players_id(self):
        self.id_list = []
        with open("data/players", "rb") as file_players:
            self.saved_players = pickle.load(file_players)
        for player in self.saved_players.values():
            self.id_list.append(player.id)
        return self.id_list

    def add_players(self, player):
        """add a new player to the whole list of players"""
        self.players[player.id] = player

    def get_players(self):
        """get the whole list of players"""
        return self.players

    def save_players(self, players):
        with open("data/players", "rb") as file_players:
            self.already_saved_files = pickle.load(file_players)
        self.already_saved_files.update(players)
        with open("data/players", "wb") as file_players:
            pickle.dump(self.already_saved_files, file_players)

    def load_players(self):
        with open("data/players", "rb") as file_players:
            self.players = pickle.load(file_players)
        return self.players
