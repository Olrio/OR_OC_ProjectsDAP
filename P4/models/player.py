"""
Manage all
"""

from models.data import Data


class Player:
    def __init__(self, lastname=None, firstname=None, rank=None):
        """initialise un nouveau joueur"""
        self.lastname = lastname  # nom de famille
        self.firstname = firstname
        self.birthdate = None
        self.gender = None
        self.rank = rank
        self.id = get_id() if self.lastname else None
        self.translation = None

    def set_new_value(self, param, value):
        self.__setattr__(param, value)

    def modify_rank(self, rank):
        """possibilité de modifier manuellement le rang d'un joueur"""
        self.rank = rank

    def __str__(self):
        return f"{self.lastname}, {self.firstname} ({self.rank})"


def get_translation(lang):
    if lang == "fr":
        return {
            "lastname": "Nom",
            "firstname": "Prénom",
            "birthdate": "Date de naissance",
            "gender": "Sexe",
            "rank": "Classement",
        }


def get_id():
    """Getting a unique identifiant consulting existing ones"""
    list_id = Data().list_of_saved_players_id()
    return str(len(list_id))
