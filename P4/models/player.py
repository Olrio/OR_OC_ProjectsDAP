import datetime

class Player:
    def __init__(self):
        """initialize a new player"""
        self.lastname: str = None
        self.firstname: str = None
        self.birthdate: datetime.date = None
        self.gender: str = None
        self.rank: int = None
        self.ident: str = None  # unique identifiant of the player

    def __str__(self):
        return f"{self.lastname:<12}{self.firstname:<15}{self.rank:<10}"

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
