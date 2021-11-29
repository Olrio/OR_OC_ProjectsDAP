"""
Accepter les données de l'utilisateur
Produire les résultats des matchs
Lancer de nouveaux tournois
...
"""

import re
from models.data import Data
from models.round import Round
from models.player import Player
from models.tournament import Tournament
from view.view import View, Report, EditTournament
from view.createplayer import get_players
from view.createtournament import get_info_tournament, choose_players


class Controller:
    def __init__(self):
        """Create a controller for the application"""
        self.db = Data()
        self.view = View()
        self.report = Report()
        self.edit = EditTournament()

    def load_or_create_tournament(self):
        """Interact with Views and Models
        and returns tournament data to the Controller"""
        # Asks user to choose between loading an existing
        # or creating a new tournament
        self.tournament_user_choice = ""
        # Entry must be [1] (load), [2] (create)
        # or [Q] to quit the program
        while self.tournament_user_choice.upper() not in ["1", "2", "Q"]:
            self.tournament_user_choice = (
                self.view.load_or_create_tournament()
            )  # 1 = load, 2 = create, Q = Quit
        if self.tournament_user_choice.upper() == "Q":
            exit()
        elif self.tournament_user_choice == "1":  # loading list of tournaments
            # loading all tournaments -> dict of tournaments
            self.load_all_tournaments()
            # display all tournaments
            self.display_all_tournaments()
            # user chooses one of the displayed tournaments from its id
            # returns selected_tournament
            self.select_a_tournament()
            # ask if user wants to edit the tournament
            self.ask_for_edit_a_tournament()
            return self.selected_tournament


    def ask_for_edit_a_tournament(self):
        """
        Ask if the user wants to edit the selected tournament
        """
        self.edit_tournament = ""
        while self.edit_tournament.upper() not in ["Y", "N"]:
            self.edit_tournament = self.view.choose_to_edit_tournament(
                self.selected_tournament.name
            )
        if self.edit_tournament.upper() == "Y":
            self.edit_a_tournament()

    def edit_a_tournament(self):
        self.edit.edit_all(self.selected_tournament)
        self.data_to_change = None
        while self.data_to_change not in [
            str(x) for x in (range(1, len(self.selected_tournament.label_attributes)))
        ]:
            self.data_to_change = self.edit.ask_for_data_to_change()
        # Determination of the attribute to modify
        self.parameter = self.selected_tournament.dict_attributes[self.data_to_change]
        self.old_value = self.selected_tournament.__getattribute__(self.parameter)
        self.new_value = self.edit.new_value_for_data(
            self.selected_tournament.label_attributes[self.parameter], self.old_value
        )
        if self.edit.confirm_new_value(self.old_value, self.new_value).upper() == "Y":
            self.edit.modification_validated()
            self.selected_tournament.set_new_value(self.parameter, self.new_value)
        else:
            self.edit.modification_cancelled()
        self.edit.edit_all(self.selected_tournament)
        # ask if the user wishes to proceed to more modifications
        # or wants to save the updated tournament
        self.choice_between_change_and_save = ""
        while self.choice_between_change_and_save.upper() not in ["S", "M"]:
            self.choice_between_change_and_save = (
                self.edit.ask_for_other_changes_or_save()
            )
        if self.choice_between_change_and_save.upper() == "S":
            self.db.save_tournaments(self.tournaments_to_choose)
            self.edit.save_ok()
            self.load_all_tournaments()
            self.ask_for_edit_a_tournament()
        else:
            self.edit_a_tournament()

    def load_all_tournaments(self):
        """
        Data gets the dict of saved tournaments
        """
        self.tournaments_to_choose = self.db.load_tournaments()

    def display_all_tournaments(self):
        """
        View displays the list of tournaments (ended/ in progress / upcoming)
        """
        self.report.display_tournaments_global(self.tournaments_to_choose)

    def select_a_tournament(self):
        # View asks the user to enter tournament id until it's a valid id
        self.selected_tournament_id = ""
        self.selected_tournament = None
        while (
            self.selected_tournament_id.upper() not in self.tournaments_to_choose.keys()
            and self.selected_tournament_id.upper() != "Q"
        ):
            self.selected_tournament_id = self.view.select_a_loaded_tournament()
        # Back to precedent menu if user enters [M]
        if self.selected_tournament_id.upper() == "M":
            self.load_or_create_tournament()
        # Determination of the tournament corresponding to the entered id
        else:
            self.selected_tournament = self.tournaments_to_choose[
                self.selected_tournament_id
            ]
            print(self.selected_tournament)

    def run(self):
        """loading or creation of the tournament"""
        self.mytournament = self.load_or_create_tournament()
        if not self.mytournament.players:
            self.choice_add_player = ""
            while self.choice_add_player.upper() not in ["A", "Q", "L"]:
                self.choice_add_player = self.view.ask_to_add_players(self.mytournament)
            if self.choice_add_player.upper() == "Q":
                exit()
            elif self.choice_add_player.upper() == "L":
                self.display_all_tournaments()
                self.select_a_tournament()
            else:
                print("ajout des joueurs")

        else:
            self.report.display_tournament_players_by_rank()

        exit()
        # récupération des infos sur les 8 joueurs du tournoi
        self.data_players = get_players()
        for data_player in self.data_players:
            player = Player(data_player)  # création de chaque joueur
            # ajout de chaque joueur à la liste globale des joueurs
            self.db.add_players(player)
        # enregistrement de la liste des joueurs dans un fichier
        self.db.save_players()

        self.players = choose_players(self.db.get_players())
        for player in self.players:
            self.mytournament.add_player(player)

        # ajout du tournoi à la liste des tournois
        self.db.add_tournament(self.mytournament)
        # enregistrement de la liste des tournois dans un fichier
        self.db.save_tournaments()

        for num_round in range(1, self.mytournament.nb_rounds + 1):
            if num_round == 1:
                self.mytournament.sort_players()
                self.mytournament.first_round_sort_players()
                self.matchs = self.mytournament.first_matchs()
                self.mytournament.generate_round(Round("Round 1", self.matchs))
                self.mytournament.generate_results(self.mytournament.rounds[0])
                self.mytournament.sort_players()
                self.mytournament.display_scores()
            else:
                self.matchs = self.mytournament.other_matchs()
                self.mytournament.generate_round(
                    Round(f"Round {num_round}", self.matchs)
                )
                self.mytournament.generate_results(
                    self.mytournament.rounds[num_round - 1]
                )
                self.mytournament.sort_players()
                self.mytournament.display_scores()
