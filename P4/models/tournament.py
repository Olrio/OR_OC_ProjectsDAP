"""
Management of a tournament
"""
import datetime


class Tournament:
    def __init__(self):
        self.name: str = None
        self.town: str = None
        self.country: str = None
        self.ident: str = None
        self.date_start: datetime.date = None
        self.date_end: datetime.date = None
        self.status: str = None  #upcoming, in progress, ended
        self.control_time: str = None  # bullet, blitz or rapid
        self.description: str = None  # tournament director's comments
        self.system: str = None  # "swiss" by default
        self.nb_rounds: int = None  # number of rounds in the tournament  = 4 by default
        self.rounds: list = None  # list of round identifiants. To get Round instances
        self.players: list = None  # list of players identifiants. To get Player instances
        self.singleton: list = None  # list of floating players when number of players is odd

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

    def add_round(self, round):
        for t_round in self.rounds:
            if round.name == t_round.name:
                return
        self.rounds.append(round)