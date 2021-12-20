"""
manage CRUD operations for following objects
Tournament
"""

import datetime

from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match

class Crud:
    def __init__(self):
        pass

    def create_tournament(self, data, tournaments):
        """create a new tournament from data"""
        t_ident = str(len(tournaments)+1)
        tournaments[t_ident] = Tournament()
        tournaments[t_ident].ident = t_ident
        tournaments[t_ident].name = data["Nom"]
        tournaments[t_ident].town = data["Ville"]
        tournaments[t_ident].country = data["Pays"]
        tournaments[t_ident].date_start = data["Date de début"]
        tournaments[t_ident].date_end = data["Date de fin"]
        tournaments[t_ident].nb_rounds = int(data["Nombre de rondes"])
        tournaments[t_ident].control_time = data["Type de partie"]
        tournaments[t_ident].system = data["Système"]
        tournaments[t_ident].description = data["Commentaires"]
        tournaments[t_ident].status = "upcoming"
        tournaments[t_ident].rounds = list()
        tournaments[t_ident].players = list()
        tournaments[t_ident].singleton = list()
        return tournaments[t_ident]

    def create_player(self, data, players):
        """create a new player from data"""
        p_ident = str(len(players)+1)
        players[p_ident] = Player()
        players[p_ident].ident = p_ident
        players[p_ident].lastname = data["Nom"]
        players[p_ident].firstname = data["Prénom"]
        players[p_ident].rank = int(data["Classement"])
        players[p_ident].birthdate = data["Date de naissance"]
        players[p_ident].gender = data["Sexe"]
        return players[p_ident]

    def create_round(self, tournament, rounds):
        """create a new round from tournament given as an argument"""
        r_ident = str(len(rounds)+1)
        rounds[r_ident] = Round()
        rounds[r_ident].ident = r_ident
        rounds[r_ident].name = "Round " + r_ident
        rounds[r_ident].players = tournament.players
        rounds[r_ident].scores = dict()
        if len(tournament.rounds) == 0:
            for player in rounds[r_ident].players:
                rounds[r_ident].add_player_score(player.ident)
        else:
            for player in rounds[r_ident].players:
                rounds[r_ident].scores[player.ident] = tournament.rounds[-1].scores[player.ident]
        rounds[r_ident].matchs = list()
        rounds[r_ident].get_start_time()
        return rounds[r_ident]

    def create_match(self, matchs, player1, player2, score1=0.0,  score2=0.0):
        m_ident = str(len(matchs)+1)
        matchs[m_ident] = Match()
        matchs[m_ident].ident = m_ident
        matchs[m_ident].data = ([player1, score1], [player2, score2])
        return matchs[m_ident]
