"""
Management of the database for the application
"""

import pickle


class Data:
    """database"""

    def __init__(self):
        self.players = []
        self.tournaments = {}

    def add_tournament(self, tournament):
        """add a new tournament to the list of tournaments"""
        if tournament not in self.tournaments.values():
            self.tournaments[tournament.id] = tournament

    def save_tournaments(self, tournaments):
        """save the list of tournaments in a file"""
        with open("data/tournaments2", "rb") as file_tournaments:
            self.already_saved_files = pickle.load(file_tournaments)
        self.already_saved_files.update(self.tournaments)
        with open("data/tournaments2", "wb") as file_tournaments:
            pickle.dump(self.already_saved_files, file_tournaments)

    def load_tournaments(self):
        """load the list of tournaments from a file"""
        with open("data/tournaments2", "rb") as file_tournaments:
            self.loaded_tournaments = pickle.load(file_tournaments)
        """ test if pickle data are stored as a list or as a dict"""
        for tournament in self.loaded_tournaments.values():
            self.tournaments[tournament.id] = tournament
        return self.tournaments

    def list_of_saved_tournaments_id(self):
        self.id_list = []
        with open("data/tournaments", "rb") as file_tournaments:
            self.saved_tournaments = pickle.load(file_tournaments)
        for tournament in self.saved_tournaments.values():
            self.id_list.append(tournament.id)
        return self.id_list

    def add_players(self, player):
        """add a new player to the whole list of players"""
        if player not in self.players:
            self.players.append(player)

    def get_players(self):
        """get the whole list of players"""
        return self.players

    def save_players(self):
        with open("models/players", "wb") as file_players:
            pickle.dump(self.players, file_players)

    def load_players(self):
        self.players = []
        with open("models/players", "rb") as file_players:
            self.players = pickle.load(file_players)
