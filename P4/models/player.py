import datetime

class Player:
    def __init__(self):
        """initialize a new player"""
        self.lastname = str()
        self.firstname = str()
        self.birthdate = datetime.date.today()
        self.gender = str()
        self.rank = int()
        self.ident = str()  # unique identifiant of the player

    def __str__(self):
        return f"{self.lastname}, {self.firstname} ({self.rank})"

    def get_translation(self, lang):
        if lang == "fr":
            return {
                "lastname": "Nom",
                "firstname": "Prénom",
                "rank": "Classement",
                "ident": "Identifiant",
                "birthdate": "Date de naissance",
                "gender": "Sexe"
            }
