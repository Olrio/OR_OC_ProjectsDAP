"""
Display ranking
Display matchs
Display statistics
...
"""

import os
import time
import curses



class View:
    def __init__(self, name=None):
        self.name = name

    def path_and_historic(self, source):
        result = ""
        for page in source:
            result = result + f"{page.name}/"
        return result

    def menu_headers(self, menu, historic, tournament, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")

    def choose_submenu(self, menu, historic, tournament, player):
        self.menu_headers(menu, historic, tournament, player)
        print("Faites un choix : ")
        for option in menu.submenus.items():
            print(f"{option[1].name:<30} [{option[0]}]")
        return input("-->  ")

    def select_a_loaded_element(self, menu):
        print("Voulez-vous : ")
        for option in menu.submenus.items():
            print(f"{option[1].name:<35} [{option[0]}]")
        return input("-->  ")

    def tournament_ended(self, tournament):
        print(f"Le tournoi {tournament} est terminé.")
        print("Veuillez sélectionner un autre tournoi")
        time.sleep(2)

    def tournament_upcoming(self, tournament):
        print(f"Le tournoi {tournament} n'a pas débuté.")
        print("Veuillez effectuer un autre choix")
        time.sleep(2)

    def tournament_in_progress(self, tournament):
        print(f"Le tournoi {tournament} a déjà débuté.")
        print("Veuillez effectuer un autre choix")
        time.sleep(2)

    def player_already_in_tournament(self, player, tournament):
        print(f"Le joueur {player} participe déjà au tournoi {tournament}")
        print("Ajout annulé")
        time.sleep(5)

    def not_enought_players_in_tournament(self, tournament):
        print(f"Il faut au moins 2 joueurs pour débuter le tournoi {tournament}")
        print("Veuillez effectuer un autre choix")
        time.sleep(2)

    def players_in_tournament(self, menu, historic, tournament, player):
        print("Voulez-vous : ")
        for option in menu.submenus.items():
            print(f"{option[1].name:<35} [{option[0]}]")
        return input("-->  ")

    def no_player_in_tournament(self, tournament):
        print(f"Il n'y a actuellement aucun participant pour le tournoi {tournament}.")
        time.sleep(2)

    def match_result_already_completed(self, match):
        print(f"Vous avez déjà entré le résultat du match {match}")
        print("Confirmez la réinitialisation de ce résultat [Y]")
        print('Ou revenez à la liste des matchs en cours [N]')
        return input("-->  ")

    def some_results_missing(self, tournament):
        print(f"Vous n'avez pas entré tous les résultats du {tournament.rounds[-1].name}")
        print(f"Veuillez compléter vos saisies avant de lancer le tour suivant")
        time.sleep(5)

    def system_of_tournament(self, tournament):
        print(f"Le tournoi {tournament} a été créé comme tournoi de système {tournament.system}")
        print(f"Confirmez-vous le système de tournoi [Y]/[N] : ?")
        print("Revenir au menu précédent [B]")
        print("Quitter                   [Q]")
        return input("--> ")

    def draw(self, match):
        print(f"Match nul entre {match.player1} et {match.player2}")
        print(f"{match.player1} + 0.5 point")
        print(f"{match.player2} + 0.5 point")

    def victory1(self, match):
        print(f"Victoire {match.player1} sur {match.player2}")
        print(f"{match.player1} + 1 point")
        print(f"{match.player2} + 0 point")

    def victory2(self, match):
        print(f"Victoire {match.player2} sur {match.player1}")
        print(f"{match.player2} + 1 point")
        print(f"{match.player1} + 0 point")

    def swiss_sort_players(self, menu, historic, tournament):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi : {tournament}  --- système {tournament.system}")
        print("Score des joueurs du tournoi ", end="")
        if len(tournament.rounds)==0:
            print("avant le premier tour")
        else:
            print(f"à l'issue du {tournament.rounds[-1].name}")
        print(f"{'Nom':<10} {'Prénom':<15} {'Classement':<15} {'Score':<5}")
        for player in tournament.players:
            print(f"{player.lastname:<10} {player.firstname:<15} {player.rank:<15} {tournament.scores[player]:<5}")
        for option in menu.submenus.items():
            print(f"{option[1].name:<35} [{option[0]}]")
        return input("--> ")

    def swiss_final_results(self, menu, historic, tournament):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi : {tournament}  --- système {tournament.system}")
        print("Fin du tournoi")
        print("Score des joueurs du tournoi ")
        print(f"{'Nom':<10} {'Prénom':<15} {'Classement':<15} {'Score':<5}")
        for player in tournament.players:
            print(f"{player.lastname:<10} {player.firstname:<15} {player.rank:<15} {tournament.scores[player]:<5}")
        print(f"\n***** Victoire de {tournament.players[0].firstname} {tournament.players[0].lastname} *****\n")
        print("Pressez une touche pour revenir à l'accueil")
        return input("--> ")


    def swiss_round_matchs(self, menu, historic, tournament):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi : {tournament}  --- système {tournament.system}")
        print(f"Matchs du {tournament.rounds[-1].name} :")
        for match in tournament.rounds[-1].matchs:
            if match in tournament.players:
                print(f"Flotteur : {match.firstname:>15} {match.lastname:<47}{tournament.scores[match]}\n")
            else:
                print(f"{match} {tournament.scores[match.player1]}-{tournament.scores[match.player2]:<10} [{tournament.rounds[-1].matchs.index(match)}]\n")
        for option in menu.submenus.items():
            print(f"{option[1].name:<35} [{option[0]}]")
        return input("--> ")

    def enter_match_result(self, menu, historic, tournament, match):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi : {tournament}  --- système {tournament.system}")
        print(f"Résultat du match {match}\n")
        print(f"Victoire de            : {match.player1.firstname:>15} {match.player1.lastname:<15}  [{match.player1.id}]")
        print(f"Victoire de            : {match.player2.firstname:>15} {match.player2.lastname:<15}  [{match.player2.id}]")
        print(f"Match nul              : {'[N]':>36}")
        print(f"Revenir aux matchs     : {'[C]':>36}")
        return input("--> ")



class Report:
    """Manage reports about players and tournaments"""

    def __init__(self):
        pass

    def path_and_historic(self, source):
        result = ""
        for page in source:
            result = result + f"{page.name}/"
        return result

    def display_selected_player(self, menu, historic, tournament, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")
        for item in menu.choices.items():
            print("{:<25}".format(player.translation[item[1]]), end='')
            print("{:<25}".format(player.__getattribute__(item[1])), end='')
            print("{:<2}".format(f"[{item[0]}]"))

    def display_selected_tournament(self, menu, historic, tournament, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")

        for item in menu.choices.items():
            print("{:<25}".format(tournament.translation[item[1]]), end='')
            print("{:<25}".format(tournament.__getattribute__(item[1])), end='')
            print("{:<2}".format(f"[{item[0]}]"))

        print(f"Participants :      {'Nom':<15}{'Prénom':<15} {'(Classement)':<15} Score")
        for t_player, score in tournament.scores.items():
            print(f"{t_player.lastname:>25} {t_player.firstname:>15}{'(':>15}{t_player.rank}){score:>10}")

    def display_players_by_name(self, menu, historic, players, tournament, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")
        print("Voici la liste des joueurs d'échecs (par ordre alphabétique)")
        print(f"{'Nom':<10} {'Prénom':<15} {'Classement':<15} {'ID':<5}")
        for player in sorted(players.values(), key = lambda x: x.lastname):
            print(f"{player.lastname:<10} {player.firstname:<15} {player.rank:<15} [{player.id}]")

    def display_players_by_rank(self, menu, historic, tournament, players, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")
        print("Voici la liste des joueurs d'échecs (par classement")
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        players.sort(key=lambda x: x[2])
        for player in players:
            print(f"{player[0]:<10} {player[1]:<10} {player[2]:<5}")

    def display_tournament_players_by_name(self, tournament):
        print(
            f"Voici la liste des joueurs du tournoi {tournament.name} (par ordre alphabétique)"
        )
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15} {'Score':<5}")

        tournament.players.sort(key=lambda x: x.firstname)
        tournament.players.sort(key=lambda x: x.lastname)
        for player in tournament.players:
            print(
                f"{player.lastname:<10} {player.firstname:<15} {player.rank:<12} {player.score:<5}"
            )

    def display_tournament_players_by_rank(self, tournament):
        print(
            f"Voici la liste des joueurs du tournoi {tournament.name} (par classement)"
        )
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15} {'ID':<5}")
        tournament.players.sort(key=lambda x: x.rank)
        for player in tournament.players:
            print(
                f"{player.lastname:<10} {player.firstname:<15} {player.rank:<12} [{player.id}]"
            )

    def display_tournaments_detailed(self, tournaments):
        print(f"{'Nom du tournoi':<25} {'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        for tournament in tournaments:
            print(f"{tournament.name:<25}")
            for player in tournament.players:
                print(
                    f"{'*'*25} {player.lastname:<10} {player.firstname:<13} {player.rank:<15}"
                )

    def display_tournaments_global(self, menu, historic, tournaments, tournament, player):
        # display headers from the first tournament of the list
        # names of columns are issued from dict(label_attributes)
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")

        # using the first tournament of the list of tournaments to get the labels
        first_tournament = list(tournaments.values())[0]
        print(
            "{:<25}".format(first_tournament.translation['name']),
            "{:<10}".format(first_tournament.translation["town"]),
            "{:<10}".format(first_tournament.translation["country"]),
            "{:<20}".format(first_tournament.translation["date_start"]),
            "{:<15}".format(first_tournament.translation["date_end"]),
            "{:<15}".format(first_tournament.translation["status"]),
            "{:<10}".format(first_tournament.translation["id"]),
        )
        # display specific data for each tournament
        for tournament in tournaments.values():
            print(
                f"{tournament.name:<25}",
                f"{tournament.town:<10}",
                f"{tournament.country:<10}",
                f"{tournament.date_start:<20}",
                f"{tournament.date_end:<15}",
                f"{tournament.status:<15}",
                f"{tournament.id:<10}",
            )


class EditTournament:
    """Manage modifications of the tournament data by the user"""

    def __init__(self):
        pass

    def path_and_historic(self, source):
        result = ""
        for page in source:
            result = result + f"{page.name}/"
        return result

    def edit_element(self, menu):
        print("Voulez-vous : ")
        for option in menu.submenus.items():
            print(f"{option[1].name:<40} [{option[0]}]")
        return input("-->  ")

    def new_value_for_data(self, menu, historic, tournament, player, param, olddata):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_menu = self.path_and_historic(menu.path)
        historic_menu = self.path_and_historic(historic)
        print(f"{path_menu}")
        print(f"Historique : {historic_menu}")
        print(f"Tournoi sélectionné : {'aucun' if tournament is None else tournament}")
        print(f"Joueur sélectionné : {'aucun' if player is None else player}")
        print(
            f"Saisissez la nouvelle valeur de {param} en remplacement de {olddata} \n"
            f"[B] pour revenir à la liste des paramètres\n"
            f"ou [Q] pour quitter "
        )
        return input("-->  ")

    def value_non_numeric(self, param):
        print(f"ATTENTION ! {param} doit être un nombre !")
        time.sleep(4)

    def confirm_new_value(self, olddata, newdata):
        return input(
            f"Veuillez confirmer que vous remplacez {olddata} par {newdata} : [Y] pour valider la modification : "
        )

    def confirm_add_player_to_tournament(self, player, tournament):
        return input(f"Confirmez-vous l'ajout du joueur {player} au tournoi {tournament} (Y/N) ? ")

    def confirm_create_player(self, player):
        return input(f"Confirmez-vous la création du joueur {player} (Y/N) ? ")

    def confirm_create_tournament(self, tournament):
        return input(f"Confirmez-vous la création du tournoi {tournament} (Y/N) ? ")

    def confirm_remove_player_from_tournament(self, player, tournament):
        return input(f"Confirmez-vous le retrait du joueur {player} du tournoi {tournament} (Y/N) ? ")

    def modification_validated(self):
        print("La modification est validée")
        time.sleep(2)

    def modification_cancelled(self):
        print("La modification est annulée")
        time.sleep(2)

    def save_ok(self):
        print("*****")
        print("Enregistrement des informations")
        print("*****")
        time.sleep(2)

    def no_tournament_to_edit(self):
        print("Aucun tournoi sélectionné")
        print("Veuillez préalablement charger ou créer un tournoi")
        time.sleep(2)

    def no_tournament_in_database(self):
        print("Aucun tournoi dans la base de données")
        print("Veuillez préalablement créer un tournoi")
        time.sleep(2)

    def no_player_to_edit(self):
        print("Aucun joueur sélectionné")
        print("Veuillez préalablement charger ou créer un joueur")
        time.sleep(2)

    def lastname_new_player(self):
        return input("Entrez le nom du nouveau joueur : ")

    def firstname_new_player(self):
        return input("Entrez le prénom du nouveau joueur : ")

    def rank_new_player(self):
        return input("Entrez le classement du nouveau joueur : ")

    def name_new_tournament(self):
        return input("Entrez le nom du nouveau tournoi : ")

    def town_new_tournament(self):
        return input("Entrez la ville du nouveau tournoi : ")

    def country_new_tournament(self):
        return input("Entrez le pays du nouveau tournoi : ")

    def alert_creating_an_existing_player(self, player):
        print(f"ATTENTION ! Il existe déjà un joueur {player.lastname} {player.firstname} dans la base de données")
        print("Veuillez modifier vos saisies pour distinguer les deux joueurs")
        time.sleep(5)

    def alert_creating_an_existing_tournament(self, tournament):
        print(f"ATTENTION ! Il existe déjà un tournoi {tournament.name} {tournament.town} dans la base de données")
        print("Veuillez modifier vos saisies pour distinguer les deux tournois")
        time.sleep(5)




