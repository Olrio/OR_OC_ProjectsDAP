from models.player import Player

class Controller:
    def __init__(self):
        """Create a controller for the application"""
        self.players = {}

    def add_player(self, lastname, firstname, rank, id):
        self.players[id] = Player(lastname, firstname, rank, id)
