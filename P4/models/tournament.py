"""
Management of a tournament
"""
import datetime


class Tournament:
    def __init__(self):
        self.name = str()
        self.town = str()
        self.country = str()
        self.ident = str()
        self.date_start = datetime.date.today()
        self.date_end = datetime.date.today()
        self.status = "upcoming"  #upcoming, in progress, ended
        self.control_time = str()  # bullet, blitz or rapid
        self.description = str()  # tournament director's comments
        self.system = "swiss"  # "swiss" by default
        self.nb_rounds = 4  # number of rounds in the tournament 4 by default
        self.rounds = list()  # list of round identifiants. To get Round instances
        self.players = list()  # list of players identifiants. To get Player instances
        self.singleton = list()  # list of floating players when number of players is odd

    def get_translation(self, lang):
        if lang == "fr":
            return {
                "name": "Nom du tournoi",
                "town": "Ville",
                "country": "Pays",
                "ident": "ID",
                "date_start": "Date de début",
                "date_end": "Date de fin",
                "status": "Statut",
                "nb_rounds": "Nombre de rounds",
                "control_time": "Type de partie",
                "description": "Commentaires",
                "system": "Système",
                "scores": "Scores",
            }

    def add_round(self, newround):
        for t_round in self.rounds:
            if newround.name == t_round.name:
                return
        self.rounds.append(newround)