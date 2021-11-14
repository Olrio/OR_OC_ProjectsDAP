"""
Management of the database for the application
"""

import pickle


class Data:
    """database"""
    def __init__(self):
        self.players = []
        self.tournaments = []

    def add_tournament(self, tournament):
        """ add a new tournament to the list of tournaments"""
        if tournament not in self.tournaments:
            self.tournaments.append(tournament)

    def save_tournaments(self):
        """ save the list of tournaments in a file"""
        with open("models/tournaments", "wb") as file_tournaments:
            pickle.dump(self.tournaments, file_tournaments)

    def load_tournaments(self):
        """ load the list of tournaments from a file"""
        self.tournaments = []
        with open("models/tournaments", "rb") as file_tournaments:
            self.tournaments = pickle.load(file_tournaments)

    def add_players(self, player):
        """ add a new player to the whole list of players """
        if player not in self.players:
            self.players.append(player)

    def get_players(self):
        """ get the whole list of players """
        return self.players

    def save_players(self):
        with open("models/players", "wb") as file_players:
            pickle.dump(self.players, file_players)

    def load_players(self):
        self.players = []
        with open("models/players", "rb") as file_players:
            self.players = pickle.load(file_players)
