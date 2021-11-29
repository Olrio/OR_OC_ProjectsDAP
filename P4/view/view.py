"""
Display ranking
Display matchs
Display statistics
...
"""


class View:
    def __init__(self, name=None):
        self.name = name

    def load_or_create_tournament(self):
        return input(
            "Voulez-vous : \n"
            "Charger un tournoi existant [1] ?\n"
            "Créer un nouveau tournoi [2] ? \n"
            "Quitter le programme [Q] ?\n"
            "-->  "
        )

    def select_a_loaded_tournament(self):
        self.selected_tournament_id = input(
            "Veuillez entrer l'ID du tournoi à gérer "
            "ou taper [M] pour revenir au menu précédent : "
        )
        return self.selected_tournament_id

    def choose_to_edit_tournament(self, tournament):
        print(f"Vous avez sélectionné le tournoi {tournament} ")
        return input(
            f"Souhaitez-vous éditer le tournoi {tournament} ? \n "
            f"Tapez [Y] pour éditer le tournoi {tournament} "
            " ou [N] pour poursuivre : "
        )

    def ask_to_add_players(self, tournament):
        print(f"Aucun joueur dans le tournoi {tournament}")
        return input("Tapez [A] pour ajouter un joueur\n"
                     "Tapez [Q] pour quitter le programme\n"
                     "Tapez [L] pour revenir à la liste des tournois\n")


class Report:
    """Manage reports about players and tournaments"""

    def __init__(self):
        pass

    def display_players_by_name(self, players):
        print("Voici la liste des joueurs d'échecs (par ordre alphabétique")
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        players.sort(key=lambda x: x[1])
        players.sort(key=lambda x: x[0])
        for player in players:
            print(f"{player[0]:<10} {player[1]:<10} {player[2]:<5}")

    def display_players_by_rank(self, players):
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
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15} {'Score':<5}")
        tournament.players.sort(key=lambda x: x.rank)
        for player in tournament.players:
            print(
                f"{player.lastname:<10} {player.firstname:<15} {player.rank:<12} {player.score:<5}"
            )

    def display_tournaments_detailed(self, tournaments):
        print(f"{'Nom du tournoi':<25} {'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        for tournament in tournaments:
            print(f"{tournament.name:<25}")
            for player in tournament.players:
                print(
                    f"{'*'*25} {player.lastname:<10} {player.firstname:<13} {player.rank:<15}"
                )

    def display_tournaments_global(self, tournaments):
        # display headers from the first tournament of the list
        # names of columns are issued from dict(label_attributes)
        header_key = list(tournaments.keys())[0]
        print(
            "{:<25}".format(tournaments[header_key].label_attributes["name"]),
            "{:<10}".format(tournaments[header_key].label_attributes["town"]),
            "{:<10}".format(tournaments[header_key].label_attributes["country"]),
            "{:<20}".format(tournaments[header_key].label_attributes["date_start"]),
            "{:<15}".format(tournaments[header_key].label_attributes["date_end"]),
            "{:<15}".format(tournaments[header_key].label_attributes["status"]),
            "{:<10}".format(tournaments[header_key].label_attributes["id"]),
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

    def edit_all(self, tournament):
        for attribute in sorted(
            tournament.dict_attributes.items(), key=lambda t: int(t[0])
        ):
            print(
                f"{tournament.label_attributes[attribute[1]]:<25}"
                f"{tournament.__getattribute__(attribute[1]):<25}"
                f"[{tournament.number_attributes[tournament.label_attributes[attribute[1]]]}]"
            )

    def ask_for_data_to_change(self):
        return input(f"Entrez le nombre correspondant à l'information à modifier : ")

    def new_value_for_data(self, param, olddata):
        return input(
            f"Saisissez la nouvelle valeur de {param} en remplacement de {olddata} : "
        )

    def confirm_new_value(self, olddata, newdata):
        return input(
            f"Veuillez confirmer que vous remplacez {olddata} par {newdata} : [Y] pour valider la modification : "
        )

    def ask_for_other_changes_or_save(self):
        return input(
            f"Souhaitez-vous poursuivre les modifications [M] \n"
            f"ou Sauvegarder les changements effectués [S] ? : "
        )

    def modification_validated(self):
        print("La modification est validée")

    def modification_cancelled(self):
        print("La modification est annulée")

    def save_ok(self):
        print("*****")
        print("Enregistrement des informations")
        print("*****")

