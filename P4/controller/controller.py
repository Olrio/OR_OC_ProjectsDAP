import time

from models.data import Data
from models.round import Round
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from view.view import View, Report, EditTournament
from models.menu import Menu


class Controller:
    def __init__(self):
        """Create a controller for the application"""
        self.db = Data()
        self.view = View()
        self.report = Report()
        self.edit = EditTournament()
        self.tournaments = dict()
        # menus creation
        self.path = []
        self.historic = []
        self.current_menu = None
        # Level 1
        self.menu_home = Menu("Accueil", "H")
        self.menu_home.path = [self.menu_home]
        # Level 2
        self.menu_management = Menu("Gestion du tournoi", "M")
        self.menu_management.path = [self.menu_home, self.menu_management]
        self.menu_tournament = Menu("Tournoi", "T")
        self.menu_tournament.path = [self.menu_home, self.menu_tournament]
        self.menu_player = Menu("Joueur", "P")
        self.menu_player.path = [self.menu_home, self.menu_player]
        self.menu_reports = Menu("Rapports", "R")
        self.menu_reports.path = [self.menu_home, self.menu_reports]
        self.menu_back = Menu("Revenir au menu précédent", "B")
        self.menu_quit = Menu("Quitter", "Q")
        self.menu_save = Menu("Sauvegarder le programme", "S")
        self.menu_load = Menu("Charger une sauvegarde", "L")
        # Level 3 - management
        self.menu_start_tournament = Menu("Démarrer le tournoi", "G")
        self.menu_start_tournament.path = [
            self.menu_home,
            self.menu_management,
            self.menu_start_tournament,
        ]
        self.menu_resume_tournament = Menu("Poursuivre le tournoi", "R")
        self.menu_resume_tournament.path = [
            self.menu_home,
            self.menu_management,
            self.menu_resume_tournament,
        ]
        # Level 4 - management/resume tournament
        self.menu_swiss = Menu("Système suisse", "CH")
        self.menu_swiss.path = [
            self.menu_home,
            self.menu_management,
            self.menu_resume_tournament,
            self.menu_swiss,
        ]

        # Level 5 management/resume tournament/swiss
        self.menu_swiss_first_round = Menu("Premier Round", "R")
        self.menu_swiss_first_round.path = [
            self.menu_home,
            self.menu_management,
            self.menu_resume_tournament,
            self.menu_swiss,
            self.menu_swiss_first_round,
        ]

        # Level 6 management/resume tournament/swiss/first round
        self.menu_swiss_match_result = Menu("Entrer le résultat du match", "x")
        self.menu_swiss_match_result.path = [
            self.menu_home,
            self.menu_management,
            self.menu_resume_tournament,
            self.menu_swiss,
            self.menu_swiss_first_round,
            self.menu_swiss_match_result,
        ]
        self.menu_swiss_following_round = Menu("Round suivant", "F")
        self.menu_swiss_following_round.path = [
            self.menu_home,
            self.menu_management,
            self.menu_resume_tournament,
            self.menu_swiss,
            self.menu_swiss_first_round,
            self.menu_swiss_following_round,
        ]

        # Level 3 - tournament
        self.menu_load_a_tournament = Menu("Charger un tournoi existant", "1")
        self.menu_load_a_tournament.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_load_a_tournament,
        ]
        self.menu_create_a_tournament = Menu("Créer un nouveau tournoi", "2")
        self.menu_create_a_tournament.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_create_a_tournament,
        ]
        self.menu_edit_tournament = Menu("Editer le tournoi", "3")
        self.menu_edit_tournament.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_edit_tournament,
        ]
        # Level 3 - player
        self.menu_load_a_player = Menu("Charger un joueur existant", "1")
        self.menu_load_a_player.path = [
            self.menu_home,
            self.menu_player,
            self.menu_load_a_player,
        ]
        self.menu_create_a_player = Menu("Créer un nouveau joueur", "2")
        self.menu_create_a_player.path = [
            self.menu_home,
            self.menu_player,
            self.menu_create_a_player,
        ]
        self.menu_edit_player = Menu("Editer le joueur", "3")
        self.menu_edit_player.path = [
            self.menu_home,
            self.menu_player,
            self.menu_edit_player,
        ]
        # Level 3 - reports
        self.menu_database_players_alpha = Menu(
            "Afficher tous les joueurs par ordre alphabétique", "A"
        )
        self.menu_database_players_alpha.path = [
            self.menu_home,
            self.menu_reports,
            self.menu_database_players_alpha,
        ]

        # Level 4 - tournament/load tournament
        self.menu_select_tournament_id = Menu("Saisir l'identifiant du tournoi", "ID")
        self.menu_select_tournament_id.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_load_a_tournament,
            self.menu_select_tournament_id,
        ]
        # Level 4 - tournament/edit tournament
        self.menu_select_tournament_parameter_to_change = Menu(
            "Sélectionner le paramètre à modifier", "x"
        )
        self.menu_select_tournament_parameter_to_change.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_edit_tournament,
            self.menu_select_tournament_parameter_to_change,
        ]
        self.menu_players_in_tournament = Menu("Editer les joueurs du tournoi", "P")
        self.menu_players_in_tournament.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_edit_tournament,
            self.menu_players_in_tournament,
        ]

        # Level 5 - tournament/edit tournament/players in tournament

        self.menu_add_player_from_edit_tournament = Menu(
            "Ajouter un joueur à ce tournoi", "A"
        )
        self.menu_add_player_from_edit_tournament.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_edit_tournament,
            self.menu_players_in_tournament,
            self.menu_add_player_from_edit_tournament,
        ]
        self.menu_remove_player_from_edit_tournament = Menu(
            "Retirer un joueur de ce tournoi", "x"
        )
        self.menu_remove_player_from_edit_tournament.path = [
            self.menu_home,
            self.menu_tournament,
            self.menu_edit_tournament,
            self.menu_players_in_tournament,
            self.menu_remove_player_from_edit_tournament,
        ]

        # Level 4 - player/load player
        self.menu_select_player_id = Menu("Saisir l'identifiant du joueur", "ID")
        self.menu_select_player_id.path = [
            self.menu_home,
            self.menu_player,
            self.menu_load_a_player,
            self.menu_select_player_id,
        ]

        # Level 4 - player/edit player

        self.menu_select_player_parameter_to_change = Menu(
            "Sélectionner le paramètre à modifier", "x"
        )

        self.menu_select_player_parameter_to_change.path = [
            self.menu_home,
            self.menu_player,
            self.menu_edit_player,
            self.menu_select_player_parameter_to_change,
        ]

        self.menu_add_player_to_tournament = Menu("Ajouter le joueur au tournoi", "A")
        self.menu_add_player_to_tournament.path = [
            self.menu_home,
            self.menu_player,
            self.menu_edit_player,
            self.menu_add_player_to_tournament,
        ]

        #
        # submenus for home
        self.menu_home.submenus[self.menu_management.id] = self.menu_management
        self.menu_home.submenus[self.menu_tournament.id] = self.menu_tournament
        self.menu_home.submenus[self.menu_player.id] = self.menu_player
        self.menu_home.submenus[self.menu_reports.id] = self.menu_reports
        self.menu_home.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_home.submenus[self.menu_save.id] = self.menu_save
        self.menu_home.submenus[self.menu_load.id] = self.menu_load
        # submenus for management
        self.menu_management.submenus[
            self.menu_start_tournament.id
        ] = self.menu_start_tournament
        self.menu_management.submenus[
            self.menu_resume_tournament.id
        ] = self.menu_resume_tournament
        self.menu_management.submenus[self.menu_back.id] = self.menu_back
        self.menu_management.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_management.submenus[self.menu_save.id] = self.menu_save
        self.menu_management.submenus[self.menu_load.id] = self.menu_load
        # submenus for resume tournament
        self.menu_resume_tournament.submenus[self.menu_swiss.id] = self.menu_swiss
        self.menu_resume_tournament.submenus[self.menu_back.id] = self.menu_back
        self.menu_resume_tournament.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_resume_tournament.submenus[self.menu_save.id] = self.menu_save
        self.menu_resume_tournament.submenus[self.menu_load.id] = self.menu_load
        # submenus for swiss
        self.menu_swiss.submenus[
            self.menu_swiss_first_round.id
        ] = self.menu_swiss_first_round
        self.menu_swiss.submenus[self.menu_back.id] = self.menu_back
        self.menu_swiss.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_swiss.submenus[self.menu_save.id] = self.menu_save
        self.menu_swiss.submenus[self.menu_load.id] = self.menu_load
        # submenus for swiss first round
        self.menu_swiss_first_round.submenus[
            self.menu_swiss_match_result.id
        ] = self.menu_swiss_match_result
        self.menu_swiss_first_round.submenus[
            self.menu_swiss_following_round.id
        ] = self.menu_swiss_following_round
        self.menu_swiss_first_round.submenus[self.menu_home.id] = self.menu_home
        self.menu_swiss_first_round.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_swiss_first_round.submenus[self.menu_save.id] = self.menu_save
        self.menu_swiss_first_round.submenus[self.menu_load.id] = self.menu_load

        # submenus for swiss following round
        self.menu_swiss_following_round.submenus[
            self.menu_swiss_following_round.id
        ] = self.menu_swiss_following_round
        self.menu_swiss_following_round.submenus[self.menu_home.id] = self.menu_home
        self.menu_swiss_following_round.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_swiss_following_round.submenus[self.menu_save.id] = self.menu_save
        self.menu_swiss_following_round.submenus[self.menu_load.id] = self.menu_load

        # submenus for tournament
        self.menu_tournament.submenus[
            self.menu_load_a_tournament.id
        ] = self.menu_load_a_tournament
        self.menu_tournament.submenus[
            self.menu_create_a_tournament.id
        ] = self.menu_create_a_tournament
        self.menu_tournament.submenus[
            self.menu_edit_tournament.id
        ] = self.menu_edit_tournament
        self.menu_tournament.submenus[self.menu_home.id] = self.menu_home
        self.menu_tournament.submenus[self.menu_back.id] = self.menu_back
        self.menu_tournament.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_tournament.submenus[self.menu_save.id] = self.menu_save
        self.menu_tournament.submenus[self.menu_load.id] = self.menu_load
        # submenus for load_a_tournament
        self.menu_load_a_tournament.submenus[
            self.menu_select_tournament_id.id
        ] = self.menu_select_tournament_id
        self.menu_load_a_tournament.submenus[self.menu_back.id] = self.menu_back
        self.menu_load_a_tournament.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_load_a_tournament.submenus[self.menu_save.id] = self.menu_save
        self.menu_load_a_tournament.submenus[self.menu_load.id] = self.menu_load
        # submenus for edit a tournament
        self.menu_edit_tournament.submenus[
            self.menu_select_tournament_parameter_to_change.id
        ] = self.menu_select_tournament_parameter_to_change
        self.menu_edit_tournament.submenus[
            self.menu_players_in_tournament.id
        ] = self.menu_players_in_tournament
        self.menu_edit_tournament.submenus[self.menu_back.id] = self.menu_back
        self.menu_edit_tournament.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_edit_tournament.submenus[self.menu_save.id] = self.menu_save
        self.menu_edit_tournament.submenus[self.menu_load.id] = self.menu_load
        # submenus for players in tournament
        self.menu_players_in_tournament.submenus[
            self.menu_add_player_from_edit_tournament.id
        ] = self.menu_add_player_from_edit_tournament
        self.menu_players_in_tournament.submenus[
            self.menu_remove_player_from_edit_tournament.id
        ] = self.menu_remove_player_from_edit_tournament
        self.menu_players_in_tournament.submenus[self.menu_back.id] = self.menu_back
        self.menu_players_in_tournament.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_players_in_tournament.submenus[self.menu_save.id] = self.menu_save
        self.menu_players_in_tournament.submenus[self.menu_load.id] = self.menu_load
        # submenus for player
        self.menu_player.submenus[self.menu_load_a_player.id] = self.menu_load_a_player
        self.menu_player.submenus[
            self.menu_create_a_player.id
        ] = self.menu_create_a_player
        self.menu_player.submenus[self.menu_edit_player.id] = self.menu_edit_player
        self.menu_player.submenus[self.menu_back.id] = self.menu_back
        self.menu_player.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_player.submenus[self.menu_save.id] = self.menu_save
        self.menu_player.submenus[self.menu_load.id] = self.menu_load
        # submenus for load_a_player
        self.menu_load_a_player.submenus[
            self.menu_select_player_id.id
        ] = self.menu_select_player_id
        self.menu_load_a_player.submenus[self.menu_back.id] = self.menu_back
        self.menu_load_a_player.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_load_a_player.submenus[self.menu_save.id] = self.menu_save
        self.menu_load_a_player.submenus[self.menu_load.id] = self.menu_load
        # submenus for edit a player
        self.menu_edit_player.submenus[
            self.menu_select_player_parameter_to_change.id
        ] = self.menu_select_player_parameter_to_change
        self.menu_edit_player.submenus[
            self.menu_add_player_to_tournament.id
        ] = self.menu_add_player_to_tournament
        self.menu_edit_player.submenus[self.menu_back.id] = self.menu_back
        self.menu_edit_player.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_edit_player.submenus[self.menu_save.id] = self.menu_save
        self.menu_edit_player.submenus[self.menu_load.id] = self.menu_load
        # submenus for reports
        self.menu_reports.submenus[
            self.menu_database_players_alpha.id
        ] = self.menu_database_players_alpha
        self.menu_reports.submenus[self.menu_back.id] = self.menu_back
        self.menu_reports.submenus[self.menu_quit.id] = self.menu_quit
        self.menu_reports.submenus[self.menu_save.id] = self.menu_save
        self.menu_reports.submenus[self.menu_load.id] = self.menu_load

    def save_program(self, historic, tournaments, tournament, player):
        self.db.save_program(historic, tournaments, tournament, player)
        self.edit.save_ok()

    def load_program(self):
        data_program = self.db.load_program()
        historic = data_program[0]
        historic.append("Load")
        tournaments = data_program[1]
        tournament = data_program[2]
        player = data_program[3]
        self.run_back(historic, tournaments, tournament, player)

    def run_back(self, historic, tournaments, tournament, player):
        pop = historic.pop()
        if pop == "Load":
            menu = historic[-1]
        else:
            menu = historic.pop()
            historic.append(menu)
        if menu.name == self.menu_home.name:
            self.run_home(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_tournament.name:
            self.run_tournament(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_player.name:
            self.run_player(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_load_a_tournament.name:
            self.run_load_a_tournament(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_edit_tournament.name:
            self.run_edit_a_tournament(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_players_in_tournament.name:
            self.run_players_in_tournament(
                menu, historic, tournaments, tournament, player
            )
        elif menu.name == self.menu_load_a_player.name:
            self.run_load_a_player(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_edit_player.name:
            self.run_edit_a_player(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_management.name:
            self.run_management(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_start_tournament.name:
            self.run_start_tournament(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_resume_tournament.name:
            self.run_resume_tournament(historic, tournaments, tournament, player)
        elif menu.name == self.menu_create_a_player.name:
            self.run_create_a_player(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_create_a_tournament.name:
            self.run_create_a_tournament(
                menu, historic, tournaments, tournament, player
            )
        elif menu.name == self.menu_swiss.name:
            self.run_swiss(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_swiss_first_round.name:
            self.run_swiss_first_round(menu, historic, tournaments, tournament, player)
        elif menu.name == self.menu_swiss_following_round.name:
            self.run_swiss_following_round(
                menu, historic, tournaments, tournament, player
            )

    def run_home(self, menu, historic, tournaments, tournament=None, player=None):
        # Choosing between tournaments management, players management, reports editing, save, load  or quit
        choice = ""
        while choice.upper() not in [key for key in menu.submenus.keys()]:
            choice = self.view.choose_submenu(menu, historic, tournament, player)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_tournament.id:
            historic.append(self.menu_tournament)
            self.run_tournament(
                self.menu_tournament, historic, tournaments, tournament, player
            )
        elif choice.upper() == self.menu_player.id:
            historic.append(self.menu_player)
            self.run_player(self.menu_player, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_reports.id:
            # menu reports
            print("Menu Rapports --> à implémenter")
            exit()
        elif choice.upper() == self.menu_management.id:
            historic.append(self.menu_management)
            self.run_management(
                self.menu_management, historic, tournaments, tournament, player
            )
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_home(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()

    def run_management(self, menu, historic, tournaments, tournament, player):
        choice = ""
        while choice.upper() not in [key for key in menu.submenus.keys()]:
            choice = self.view.choose_submenu(menu, historic, tournament, player)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_management(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_start_tournament.id:
            if tournament is None:
                self.edit.no_tournament_to_edit()
                self.run_management(menu, historic, tournaments, tournament, player)
            else:
                historic.append(self.menu_start_tournament)
                self.run_start_tournament(
                    self.menu_start_tournament,
                    historic,
                    tournaments,
                    tournament,
                    player,
                )
        elif choice.upper() == self.menu_resume_tournament.id:
            if tournament is None:
                self.edit.no_tournament_to_edit()
                self.run_management(menu, historic, tournaments, tournament, player)
            else:
                if len(tournament.rounds) == 0:
                    historic.append(self.menu_resume_tournament)
                    self.run_resume_tournament(
                        historic,
                        tournaments,
                        tournament,
                        player,
                    )
                elif len(tournament.rounds) == 1:
                    historic.append(self.menu_swiss_first_round)
                    self.run_swiss_first_round(
                        self.menu_swiss_first_round,
                        historic,
                        tournaments,
                        tournament,
                        player,
                    )
                else:
                    historic.append(self.menu_swiss_following_round)
                    self.run_swiss_following_round(
                        self.menu_swiss_following_round,
                        historic,
                        tournaments,
                        tournament,
                        player,
                    )

    def run_tournament(self, menu, historic, tournaments, tournament, player):
        """Interact with Views and Models
        and manage tournament menu"""
        # Asks user to choose between
        # loading an existing tournament
        # creating a new tournament
        # editing a tournament
        choice = ""
        while choice.upper() not in [key for key in menu.submenus.keys()]:
            choice = self.view.choose_submenu(menu, historic, tournament, player)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_home.id:
            historic.append(self.menu_home)
            self.run_home(self.menu_home, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_tournament(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice == self.menu_load_a_tournament.id:
            historic.append(self.menu_load_a_tournament)
            self.run_load_a_tournament(
                self.menu_load_a_tournament,
                historic,
                tournaments,
                tournament,
                player,
            )
        elif choice == self.menu_create_a_tournament.id:
            historic.append(self.menu_create_a_tournament)
            self.run_create_a_tournament(
                self.menu_create_a_tournament,
                historic,
                tournaments,
                tournament,
                player,
            )
        else:
            if tournament is None:
                self.edit.no_tournament_to_edit()
                self.run_tournament(menu, historic, tournaments, tournament, player)
            else:
                historic.append(self.menu_edit_tournament)
                self.run_edit_a_tournament(
                    self.menu_edit_tournament,
                    historic,
                    tournaments,
                    tournament,
                    player,
                )

    def run_player(self, menu, historic, tournaments, tournament, player):
        """Interact with Views and Models
        and manage player menu"""
        # Asks user to choose between
        # loading an existing player
        # creating a new player
        # editing a player
        choice = ""
        while choice.upper() not in [key for key in menu.submenus.keys()]:
            choice = self.view.choose_submenu(menu, historic, tournament, player)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_player(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_load_a_player.id:
            historic.append(self.menu_load_a_player)
            self.run_load_a_player(
                self.menu_load_a_player, historic, tournaments, tournament, player
            )
        elif choice == self.menu_create_a_player.id:
            historic.append(self.menu_create_a_player)
            self.run_create_a_player(
                self.menu_create_a_player,
                historic,
                tournaments,
                tournament,
                player,
            )
        else:
            # edit a player
            if player is None:
                self.edit.no_player_to_edit()
                self.run_player(menu, historic, tournaments, tournament, player)
            else:
                historic.append(self.menu_edit_player)
                self.run_edit_a_player(
                    self.menu_edit_player,
                    historic,
                    tournaments,
                    tournament,
                    player,
                )

    def run_start_tournament(self, menu, historic, tournaments, tournament, player):
        if len(tournament.players) < 2:
            self.view.not_enought_players_in_tournament(tournament)
            self.run_back(historic, tournaments, tournament, player)
        if tournament.status == "in progress":
            self.view.tournament_in_progress(tournament)
            self.run_back(historic, tournaments, tournament, player)
        if tournament.status == "ended":
            self.view.tournament_ended(tournament)
            historic.append(self.menu_tournament)
            self.run_tournament(
                self.menu_tournament, historic, tournaments, tournament, player
            )
        self.view.menu_headers(menu, historic, tournament, player)
        self.report.display_tournament_players_by_rank(tournament)
        choice = ""
        while choice.upper() not in [
            "Y",
            "N",
            self.menu_back.id,
            self.menu_quit.id,
            self.menu_load.id,
            self.menu_save.id,
        ]:
            self.view.menu_headers(menu, historic, tournament, player)
            choice = self.view.system_of_tournament(tournament)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_start_tournament(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif (choice.upper() == "N" and tournament.system == "swiss") or (
            choice.upper() == "Y" and tournament.system != "swiss"
        ):
            print("Autre système de tournoi --> à implémenter")
            time.sleep(4)
            self.run_start_tournament(menu, historic, tournaments, tournament, player)
        elif choice.upper() == "Y" and tournament.system == "swiss":
            tournament.set_new_value("status", "in progress")
            self.db.save_tournaments(tournaments)
            historic.append(self.menu_resume_tournament)
            self.run_resume_tournament(
                historic,
                tournaments,
                tournament,
                player,
            )

    def run_swiss(self, menu, historic, tournaments, tournament, player):
        # players are sorted
        s1 = sorted(tournament.scores.items(), key=lambda item: item[0].rank)  # by rank
        s2 = sorted(s1, key=lambda item: item[1])  # then by score
        tournament.players = []
        for t_player in s2:
            tournament.players.append(t_player[0])
        choice = ""
        while choice.upper() not in [key for key in menu.submenus.keys()]:
            choice = self.view.swiss_sort_players(menu, historic, tournament)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.historic.pop()
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_swiss(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_swiss_first_round.id:
            historic.append(self.menu_swiss_first_round)
            self.run_swiss_first_round(
                self.menu_swiss_first_round,
                historic,
                tournaments,
                tournament,
                player,
            )

    def run_swiss_first_round(self, menu, historic, tournaments, tournament, player):
        if not tournament.rounds:
            self.swiss_generate_first_round(tournament)

        valid_choices = []
        for match in tournament.rounds[-1].matchs:
            if match not in tournament.players:
                valid_choices.extend(str(tournament.rounds[-1].matchs.index(match)))
        valid_choices.extend(key for key in menu.submenus.keys())
        valid_choices.remove(self.menu_swiss_match_result.id)
        choice = ""
        while choice.upper() not in valid_choices:
            choice = self.view.swiss_round_matchs(menu, historic, tournament)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_home.id:
            self.run_home(self.menu_home, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_swiss_first_round(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_swiss_following_round.id:
            for match in tournament.rounds[-1].matchs:
                if (
                    match not in tournament.players
                    and match.score1 == 0
                    and match.score2 == 0
                ):
                    self.view.some_results_missing(tournament)
                    self.run_swiss_first_round(
                        menu, historic, tournaments, tournament, player
                    )
            for match in tournament.rounds[-1].matchs:
                if match in tournament.players:
                    tournament.scores[match] += 1  # victory for the singleton player
            tournament.rounds[-1].get_end_time()
            self.swiss_generate_following_round(
                menu, historic, tournaments, tournament, player
            )
        else:
            result = ""
            if (
                tournament.rounds[-1].matchs[int(choice)].score1 != 0
                or tournament.rounds[-1].matchs[int(choice)].score2 != 0
            ):
                result_reset = ""
                while result_reset.upper() not in ["Y", "N"]:
                    result_reset = self.view.match_result_already_completed(
                        tournament.rounds[-1].matchs[int(choice)]
                    )
                if result_reset.upper() == "Y":
                    tournament.scores[
                        tournament.rounds[-1].matchs[int(choice)].player1
                    ] -= tournament.rounds[-1].matchs[int(choice)].score1
                    tournament.scores[
                        tournament.rounds[-1].matchs[int(choice)].player2
                    ] -= tournament.rounds[-1].matchs[int(choice)].score2
                    tournament.rounds[-1].matchs[int(choice)].score1 = 0
                    tournament.rounds[-1].matchs[int(choice)].score2 = 0
                    self.run_swiss_first_round(
                        menu, historic, tournaments, tournament, player
                    )
                else:
                    self.run_swiss_first_round(
                        menu, historic, tournaments, tournament, player
                    )
            while result.upper() not in [
                "N",
                "C",
                str(tournament.rounds[-1].matchs[int(choice)].player1.id),
                str(tournament.rounds[-1].matchs[int(choice)].player2.id),
            ]:
                result = self.view.enter_match_result(
                    menu,
                    historic,
                    tournament,
                    tournament.rounds[-1].matchs[int(choice)],
                )
            if result.upper() == "C":
                self.run_swiss_first_round(
                    menu, historic, tournaments, tournament, player
                )
            elif result.upper() == "N":
                self.view.draw(tournament.rounds[-1].matchs[int(choice)])
                # update match scores
                tournament.rounds[-1].matchs[int(choice)].score1 += 0.5
                tournament.rounds[-1].matchs[int(choice)].score2 += 0.5
                # update players score in tournament
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player1
                ] += 0.5
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player2
                ] += 0.5
            elif result == str(tournament.rounds[-1].matchs[int(choice)].player1.id):
                self.view.victory1(tournament.rounds[-1].matchs[int(choice)])
                tournament.rounds[-1].matchs[int(choice)].score1 += 1
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player1
                ] += 1
            else:
                self.view.victory2(tournament.rounds[-1].matchs[int(choice)])
                tournament.rounds[-1].matchs[int(choice)].score2 += 1
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player2
                ] += 1
            self.db.save_tournaments(tournaments)
            self.edit.save_ok()
            self.run_swiss_first_round(menu, historic, tournaments, tournament, player)

    def swiss_generate_first_round(self, tournament):
        # distribute players in best half and lowest half
        first_half = tournament.players.copy()
        second_half = []
        # verify if number of players is odd number
        # player with the lowest score/rank is singleton for this round
        # player can be singleton only once
        rev_i = -1
        if len(tournament.players) % 2 != 0:
            while tournament.players[rev_i] in tournament.singleton:
                rev_i -= 1
            tournament.singleton.append(tournament.players[rev_i])
            first_half.remove(tournament.players[rev_i])
        # generation of the two halves of players
        while len(first_half) > len(second_half):
            second_half.append(first_half.pop())
        # players of the latest group are sorted by rank
        second_half.sort(key=lambda x: x.rank)
        # first matchs
        matchs = []
        for player1, player2 in zip(first_half, second_half):
            match = Match(player1, player2, tournament)
            matchs.append(match)
        if len(tournament.players) % 2 != 0:
            matchs.append(tournament.singleton[-1])
        tournament.generate_round(Round("Round 1", matchs))
        tournament.rounds[-1].get_start_time()
        self.db.save_tournaments({tournament.id: tournament})
        self.edit.save_ok()
        return tournament

    def run_swiss_following_round(
        self, menu, historic, tournaments, tournament, player
    ):
        valid_choices = []
        for match in tournament.rounds[-1].matchs:
            if match not in tournament.players:
                valid_choices.extend(str(tournament.rounds[-1].matchs.index(match)))
        menu.submenus[self.menu_swiss_match_result.id] = self.menu_swiss_match_result
        valid_choices.extend(key for key in menu.submenus.keys())
        valid_choices.remove(self.menu_swiss_match_result.id)
        choice = ""
        while choice.upper() not in valid_choices:
            choice = self.view.swiss_round_matchs(menu, historic, tournament)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_home.id:
            self.run_home(self.menu_home, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_swiss_following_round(
                menu, historic, tournaments, tournament, player
            )
        elif choice.upper() == self.menu_swiss_following_round.id:
            for match in tournament.rounds[-1].matchs:
                if (
                    match not in tournament.players
                    and match.score1 == 0
                    and match.score2 == 0
                ):
                    self.view.some_results_missing(tournament)
                    self.run_swiss_following_round(
                        menu, historic, tournaments, tournament, player
                    )
            for match in tournament.rounds[-1].matchs:
                if match in tournament.players:
                    tournament.scores[match] += 1
            if len(tournament.rounds) == tournament.nb_rounds:
                s1 = sorted(
                    tournament.scores.items(), key=lambda item: item[0].rank
                )  # by rank
                s2 = sorted(s1, key=lambda item: item[1], reverse=True)  # by score
                tournament.players = []
                for t_player in s2:
                    tournament.players.append(t_player[0])
                self.view.swiss_final_results(menu, historic, tournament)
                tournament.set_new_value("status", "ended")
                tournament.rounds[-1].get_end_time()
                self.db.save_tournaments({tournament.id: tournament})
                historic.append(self.menu_home)
                self.run_home(self.menu_home, historic, tournaments, tournament, player)
            else:
                tournament.rounds[-1].get_end_time()
                self.swiss_generate_following_round(
                    menu, historic, tournaments, tournament, player
                )
        else:
            result = ""
            if (
                tournament.rounds[-1].matchs[int(choice)].score1 != 0
                or tournament.rounds[-1].matchs[int(choice)].score2 != 0
            ):
                result_reset = ""
                while result_reset.upper() not in ["Y", "N"]:
                    result_reset = self.view.match_result_already_completed(
                        tournament.rounds[-1].matchs[int(choice)]
                    )
                if result_reset.upper() == "Y":
                    tournament.scores[
                        tournament.rounds[-1].matchs[int(choice)].player1
                    ] -= tournament.rounds[-1].matchs[int(choice)].score1
                    tournament.scores[
                        tournament.rounds[-1].matchs[int(choice)].player2
                    ] -= tournament.rounds[-1].matchs[int(choice)].score2
                    tournament.rounds[-1].matchs[int(choice)].score1 = 0
                    tournament.rounds[-1].matchs[int(choice)].score2 = 0
                    self.run_swiss_following_round(
                        menu, historic, tournaments, tournament, player
                    )
                else:
                    self.run_swiss_following_round(
                        menu, historic, tournaments, tournament, player
                    )
            while result.upper() not in [
                "N",
                "C",
                str(tournament.rounds[-1].matchs[int(choice)].player1.id),
                str(tournament.rounds[-1].matchs[int(choice)].player2.id),
            ]:
                result = self.view.enter_match_result(
                    menu,
                    historic,
                    tournament,
                    tournament.rounds[-1].matchs[int(choice)],
                )
            if result.upper() == "C":
                self.run_swiss_first_round(
                    menu, historic, tournaments, tournament, player
                )
            elif result.upper() == "N":
                self.view.draw(tournament.rounds[-1].matchs[int(choice)])
                # update match scores
                tournament.rounds[-1].matchs[int(choice)].score1 += 0.5
                tournament.rounds[-1].matchs[int(choice)].score2 += 0.5
                # update players score in tournament
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player1
                ] += 0.5
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player2
                ] += 0.5
            elif result == str(tournament.rounds[-1].matchs[int(choice)].player1.id):
                self.view.victory1(tournament.rounds[-1].matchs[int(choice)])
                tournament.rounds[-1].matchs[int(choice)].score1 += 1
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player1
                ] += 1
            else:
                self.view.victory2(tournament.rounds[-1].matchs[int(choice)])
                tournament.rounds[-1].matchs[int(choice)].score2 += 1
                tournament.scores[
                    tournament.rounds[-1].matchs[int(choice)].player2
                ] += 1
            self.db.save_tournaments({tournament.id: tournament})
            self.edit.save_ok()
            self.run_swiss_following_round(
                menu, historic, tournaments, tournament, player
            )

    def swiss_generate_following_round(
        self, menu, historic, tournaments, tournament, player
    ):
        historic.append(self.menu_swiss_following_round)
        s1 = sorted(tournament.scores.items(), key=lambda item: item[0].rank)  # by rank
        s2 = sorted(s1, key=lambda item: item[1], reverse=True)  # by score
        tournament.players = []
        for t_player in s2:
            tournament.players.append(t_player[0])
        choice = ""
        while choice.upper() not in [key for key in menu.submenus.keys()]:
            choice = self.view.swiss_sort_players(
                self.menu_swiss_following_round, historic, tournament
            )
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_home.id:
            self.run_home(self.menu_home, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.swiss_generate_following_round(
                menu, historic, tournaments, tournament, player
            )
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        else:
            # generating matchs for this round
            matchs = []
            first_players = list(tournament.players)
            second_players = list(tournament.players)
            rev_i = -1
            if len(tournament.players) % 2 != 0:
                while tournament.players[rev_i] in tournament.singleton:
                    rev_i -= 1
                tournament.singleton.append(tournament.players[rev_i])
                first_players.remove(tournament.singleton[-1])
                second_players.remove(tournament.singleton[-1])

            while first_players:
                second_players.remove(second_players[0])
                x = 0
                appairing = 0
                match = None

                while appairing == 0:
                    flag = 0
                    match = Match(first_players[0], second_players[x], tournament)
                    for t_round in tournament.rounds:
                        for past_match in t_round.matchs:
                            if past_match in tournament.players:
                                break
                            if (
                                match.player1 == past_match.player1
                                and match.player2 == past_match.player2
                                or match.player1 == past_match.player2
                                and match.player2 == past_match.player1
                            ):
                                if len(first_players) > 2:
                                    x += 1
                                    flag = 1
                                    break
                    if flag == 0:
                        appairing = 1

                matchs.append(match)
                first_players.remove(first_players[0])
                first_players.remove(second_players[x])
                second_players.remove(second_players[x])
            if len(tournament.players) % 2 != 0:
                matchs.append(tournament.singleton[-1])
            tournament.generate_round(
                Round("Round " + str(len(tournament.rounds) + 1), matchs)
            )
            tournament.rounds[-1].get_start_time()
            self.db.save_tournaments({tournament.id: tournament})
            self.edit.save_ok()
            self.run_swiss_following_round(
                menu, historic, tournaments, tournament, player
            )

    def run_resume_tournament(self, historic, tournaments, tournament, player):
        if tournament.status == "ended":
            self.view.tournament_ended(tournament)
            historic.append(self.menu_tournament)
            self.run_tournament(
                self.menu_tournament, historic, tournaments, tournament, player
            )
        elif tournament.status == "upcoming":
            self.view.tournament_upcoming(tournament)
            self.run_back(historic, tournaments, tournament, player)
        elif tournament.status == "in progress" and tournament.system == "swiss":
            historic.append(self.menu_swiss)
            self.run_swiss(self.menu_swiss, historic, tournaments, tournament, player)
        else:
            exit()

    def run_load_a_tournament(self, menu, historic, tournaments, tournament, player):
        # loading all tournaments -> dict of tournament
        loc_tournaments = self.db.load_tournaments()
        if loc_tournaments == FileNotFoundError:
            self.edit.no_tournament_in_database()
            self.run_back(historic, tournaments, tournament, player)
        # display all tournaments
        choice = ""
        tournaments_id = []
        for t_id in loc_tournaments.keys():
            tournaments_id.append(t_id)
        self.menu_select_tournament_id.id = tournaments_id
        valid_choices = tournaments_id
        valid_choices.extend(
            [self.menu_quit.id, self.menu_back.id, self.menu_save.id, self.menu_load.id]
        )
        while choice.upper() not in valid_choices:
            self.display_all_tournaments(
                menu, historic, loc_tournaments, tournament, player
            )
            choice = self.view.select_a_loaded_element(menu)
        # Quit [Q]
        if choice.upper() == self.menu_quit.id:
            exit()
        # Back to precedent menu [B]
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, loc_tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, loc_tournaments, tournament, player)
            self.run_load_a_tournament(
                menu, historic, loc_tournaments, tournament, player
            )
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        # Determination of the tournament corresponding to the entered id
        else:
            tournament = loc_tournaments[choice]
            historic.append(self.menu_edit_tournament)
            self.run_edit_a_tournament(
                self.menu_edit_tournament,
                historic,
                loc_tournaments,
                tournament,
                player,
            )

    def run_load_a_player(self, menu, historic, tournaments, tournament, player):
        # loading all players -> dict of players
        players = self.db.load_players()
        # display all players
        choice = ""
        player = player
        players_id = []
        for t_id in players.keys():
            players_id.append(t_id)
        self.menu_select_player_id.id = players_id
        valid_choices = players_id
        valid_choices.extend(
            [self.menu_quit.id, self.menu_back.id, self.menu_save.id, self.menu_load.id]
        )
        while choice.upper() not in valid_choices:
            self.display_all_players(menu, historic, players, tournament, player)
            choice = self.view.select_a_loaded_element(menu)
        # Quit [Q]
        if choice.upper() == self.menu_quit.id:
            exit()
        # Back to precedent menu [B]
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_load_a_player(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        # Determination of the player corresponding to the entered id
        else:
            player = players[choice]
            historic.append(self.menu_edit_player)
            self.run_edit_a_player(
                self.menu_edit_player,
                historic,
                tournaments,
                tournament,
                player,
            )

    def run_create_a_player(self, menu, historic, tournaments, tournament, player):
        self.view.menu_headers(menu, historic, tournament, player)
        new_lastname = self.edit.lastname_new_player()
        new_firstname = self.edit.firstname_new_player()
        new_rank = self.edit.rank_new_player()
        while not new_rank.isdecimal():
            self.edit.value_non_numeric("Le classement")
            new_rank = self.edit.rank_new_player()
        new_rank = int(new_rank)
        for existing_player in self.db.load_players().values():
            if (
                new_lastname == existing_player.lastname
                and new_firstname == existing_player.firstname
            ):
                self.edit.alert_creating_an_existing_player(existing_player)
                self.run_create_a_player(
                    menu, historic, tournaments, tournament, player
                )
        choice = ""
        while choice.upper() not in ["Y", "N"]:
            choice = self.edit.confirm_create_player(new_lastname + " " + new_firstname)
        if choice.upper() == "Y":
            self.edit.modification_validated()
            new_player = Player(new_lastname, new_firstname, new_rank)
            new_player_saver = {new_player.id: new_player}
            self.db.save_players(new_player_saver)
            self.edit.save_ok()
        else:
            self.edit.modification_cancelled()
        self.run_back(historic, tournaments, tournament, player)

    def run_create_a_tournament(self, menu, historic, tournaments, tournament, player):
        self.view.menu_headers(menu, historic, tournament, player)
        new_name = self.edit.name_new_tournament()
        new_town = self.edit.town_new_tournament()
        new_country = self.edit.country_new_tournament()
        if self.db.load_tournaments() == FileNotFoundError:
            tournaments = {}
        else:
            try:
                for existing_tournament in self.db.load_tournaments().values():
                    if (
                        new_name == existing_tournament.name
                        and new_town == existing_tournament.town
                    ):
                        self.edit.alert_creating_an_existing_tournament(
                            existing_tournament
                        )
                        self.run_create_a_tournament(
                            menu, historic, tournaments, tournament, player
                        )
            except Exception as error:
                log = list()
                log.append(error)
                pass
        choice = ""
        while choice.upper() not in ["Y", "N"]:
            choice = self.edit.confirm_create_tournament(new_name + " " + new_town)
        if choice.upper() == "Y":
            self.edit.modification_validated()
            new_tournament = Tournament(new_name, new_town, new_country)
            tournaments[new_tournament.id] = new_tournament
            self.db.save_tournaments({new_tournament.id: new_tournament})
            self.edit.save_ok()
        else:
            self.edit.modification_cancelled()
        self.run_back(historic, self.tournaments, tournament, player)

    def run_edit_a_tournament(self, menu, historic, tournaments, tournament, player):
        choice = ""
        menu.choices = {}
        for param, index in zip(tournament.__dict__, range(len(tournament.__dict__))):
            if param in [
                "scores",
                "rounds",
                "players",
                "first_half",
                "second_half",
                "translation",
                "singleton",
            ]:
                pass
            else:
                menu.choices[str(index)] = param
        valid_choices = [param for param in menu.choices.keys()]
        valid_choices.extend(menu.submenus.keys())
        self.report.display_selected_tournament(menu, historic, tournament, player)

        while choice.upper() not in valid_choices:
            self.report.display_selected_tournament(menu, historic, tournament, player)
            choice = self.edit.edit_element(menu)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_edit_a_tournament(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == "P":
            historic.append(self.menu_players_in_tournament)
            self.run_players_in_tournament(
                self.menu_players_in_tournament,
                historic,
                tournaments,
                tournament,
                player,
            )
        else:
            # Determination of the attribute to modify
            parameter = menu.choices[choice]
            old_value = tournament.__getattribute__(parameter)
            new_value = self.edit.new_value_for_data(
                menu,
                historic,
                tournament,
                player,
                tournament.translation[parameter],
                old_value,
            )
            if new_value.upper() == "B":
                self.run_back(historic, tournaments, tournament, player)
            elif new_value.upper() == "Q":
                exit()
            if self.edit.confirm_new_value(old_value, new_value).upper() == "Y":
                self.edit.modification_validated()
                tournament.set_new_value(parameter, new_value)
                self.report.display_selected_tournament(
                    menu, historic, tournament, player
                )
                self.db.save_tournaments(tournaments)
                self.edit.save_ok()
                self.run_edit_a_tournament(
                    menu, historic, tournaments, tournament, player
                )
            else:
                self.edit.modification_cancelled()
            self.run_edit_a_tournament(menu, historic, tournaments, tournament, player)

    def run_edit_a_player(self, menu, historic, tournaments, tournament, player):
        choice = ""
        menu.choices = {}
        for param, index in zip(player.__dict__, range(len(player.__dict__))):
            if param == "id" or param == "translation":
                pass
            else:
                menu.choices[str(index)] = param
        valid_choices = [param for param in menu.choices.keys()]
        valid_choices.extend(menu.submenus.keys())
        self.report.display_selected_player(menu, historic, tournament, player)
        while choice.upper() not in valid_choices:
            choice = self.edit.edit_element(menu)
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_edit_a_player(menu, historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_add_player_to_tournament.id:
            if tournament is None:
                self.edit.no_tournament_to_edit()
            elif tournament.status == "ended":
                self.view.tournament_ended(tournament)
                self.run_edit_a_player(menu, historic, tournaments, tournament, player)
            else:
                choice = ""
                while choice.upper() not in ["Y", "N"]:
                    choice = self.edit.confirm_add_player_to_tournament(
                        player, tournament
                    )
                if choice.upper() == "Y":
                    if player.id in [
                        existing_player.id for existing_player in tournament.players
                    ]:
                        self.view.player_already_in_tournament(player, tournament)
                    else:
                        tournament.add_player(player)
                        self.edit.modification_validated()
                        self.db.save_tournaments({tournaments})
                        self.edit.save_ok()
                else:
                    self.edit.modification_cancelled()
            self.run_edit_a_player(menu, historic, tournaments, tournament, player)

        else:
            # Determination of the attribute to modify
            parameter = menu.choices[choice]
            old_value = player.__getattribute__(parameter)
            new_value = self.edit.new_value_for_data(
                menu,
                historic,
                tournament,
                player,
                player.translation[parameter],
                old_value,
            )
            if parameter == "score":
                if not isinstance(eval(new_value), float) and not isinstance(
                    eval(new_value), int
                ):
                    self.edit.value_non_numeric(player.translation[parameter])
                    self.run_edit_a_player(
                        menu, historic, tournaments, tournament, player
                    )
            if parameter == "rank":
                if not new_value.isdecimal():
                    self.edit.value_non_numeric(player.translation[parameter])
                    self.run_edit_a_player(
                        menu, historic, tournaments, tournament, player
                    )
            if new_value.upper() == "B":
                self.run_back(historic, tournaments, tournament, player)
            elif new_value.upper() == "Q":
                exit()
            elif self.edit.confirm_new_value(old_value, new_value).upper() == "Y":
                self.edit.modification_validated()
                if parameter in ["rank", "score"]:
                    new_value = eval(new_value)
                player.set_new_value(parameter, new_value)
                self.report.display_selected_player(menu, historic, tournament, player)
                self.db.save_players({player.id: player})
                self.edit.save_ok()
                self.run_edit_a_player(menu, historic, tournaments, tournament, player)
            else:
                self.edit.modification_cancelled()
            self.run_edit_a_player(menu, historic, tournaments, tournament, player)

    def display_all_tournaments(self, menu, historic, tournaments, tournament, player):
        """
        View displays the list of tournaments (ended/ in progress / upcoming)
        """
        if not tournaments:
            self.edit.no_tournament_in_database()
            self.run_back(historic, tournaments, tournament, player)
        else:
            self.report.display_tournaments_global(
                menu, historic, tournaments, tournament, player
            )

    def display_all_players(self, menu, historic, players, tournament, player):
        """
        View displays the list of players
        """
        self.report.display_players_by_name(menu, historic, players, tournament, player)

    def run_players_in_tournament(
        self, menu, historic, tournaments, tournament, player
    ):
        choice = ""
        valid_choices = [
            str(tournament_player.id) for tournament_player in tournament.players
        ]
        valid_choices.extend(
            [
                self.menu_add_player_from_edit_tournament.id,
                self.menu_remove_player_from_edit_tournament.id,
                self.menu_back.id,
                self.menu_quit.id,
                self.menu_save.id,
                self.menu_load.id,
            ]
        )
        while choice.upper() not in valid_choices:
            self.view.menu_headers(
                self.menu_players_in_tournament, historic, tournament, player
            )
            if not tournament.players:
                self.view.no_player_in_tournament(tournament)
            else:
                self.report.display_tournament_players_by_rank(tournament)
            choice = self.view.players_in_tournament(
                self.menu_players_in_tournament, historic, tournament, player
            )
        if choice.upper() == self.menu_quit.id:
            exit()
        elif choice.upper() == self.menu_back.id:
            self.run_back(historic, tournaments, tournament, player)
        elif choice.upper() == self.menu_save.id:
            self.save_program(historic, tournaments, tournament, player)
            self.run_players_in_tournament(
                menu, historic, tournaments, tournament, player
            )
        elif choice.upper() == self.menu_load.id:
            self.load_program()
        elif choice.upper() == self.menu_add_player_from_edit_tournament.id:
            historic.append(self.menu_player)
            self.run_player(self.menu_player, historic, tournaments, tournament, player)
        else:
            if not tournament.players:
                self.view.no_player_in_tournament(tournament)
                self.run_players_in_tournament(
                    menu, historic, tournaments, tournament, player
                )

            player_to_remove = ""
            for tournament_player in tournament.players:
                if tournament_player.id == choice:
                    player_to_remove = tournament_player
            if (
                self.edit.confirm_remove_player_from_tournament(
                    player_to_remove, tournament
                ).upper()
                == "Y"
            ):
                tournament.remove_player(player_to_remove)
                self.edit.modification_validated()
                self.db.save_tournaments(tournaments)
                self.edit.save_ok()
                self.run_players_in_tournament(
                    menu, historic, tournaments, tournament, player
                )
            else:
                self.edit.modification_cancelled()

    def run(self):
        """choose main menu"""
        self.historic.append(self.menu_home)
        self.run_home(self.menu_home, self.historic, self.tournaments)
        exit()
