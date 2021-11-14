"""
Gestion de la classe Round
correspondant à un tour dans un tournoi d'échecs
Un round comprend plusieurs matchs opposant tous les joueurs deux à deux
"""

import datetime

class Round:
    def __init__(self, name, matchs):
        """ensemble des parties jouées durant une ronde"""
        self.matchs = matchs
        self.name = name
        self.debut = None
        self.fin = None
        self.get_start_time()

    def get_start_time(self):
        """ Enregistre le début de la partie """
        self.jour_debut = datetime.date.today().strftime("%Y/%m/%d")
        self.heure_debut = datetime.datetime.now().strftime("%H:%M")
        self.debut = (self.jour_debut, self.heure_debut)
        return self.debut

    def get_end_time(self):
        """ Enregistre la fin de la partie """
        self.jour_fin = datetime.date.today().strftime("%Y/%m/%d")
        self.heure_fin = datetime.datetime.now().strftime("%H:%M")
        self.fin = (self.jour_fin, self.heure_fin)
        return self.fin

    def __str__(self):
        round_str = str([f"{match.player1.firstname} vs {match.player2.firstname}" for match in self.matchs])
        return round_str