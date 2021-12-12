"""
Gestion de la classe Joueur
"""

from models.data import Data


class Player:
    def __init__(self, lastname, firstname, rank=0, lang="fr"):
        """initialise un nouveau joueur"""
        self.lastname = lastname  # nom de famille
        self.firstname = firstname
        self.birthdate = ""
        self.gender = ""
        self.rank = rank
        self.id = get_id()
        self.translation = get_translation(lang)

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
    list_id = Data().list_of_saved_players_id()
    return str(len(list_id))
