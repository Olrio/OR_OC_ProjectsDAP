import os


class View:
    def __init__(self):
        pass

    def home(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Chess Manager : gestionnaire de tournois d'échecs\n")
        self.press_key()

    def press_key(self):
        input("Pressez une touche pour continuer")

    def load_or_create_tournament(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Voulez-vous charger un tournoi existant [L]")
        print("Créer un nouveau tournoi                [C]")
        print("Revenir à l'accueil                     [H]")
        print("Quitter                                 [Q]")
        return input("-->  ")

    def display_all_players(self, players, tournament = None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Liste des joueurs existants\n")
        print(f"{'Nom':<12}{'Prénom':<15}{'Classement':<10}\n")
        for player in players.values():
            print(f"{player}", end="")
            if player not in tournament.players:
                print(f"[{player.ident}]")
            else:
                print()
        print(f"\n Saisissez le numéro du joueur à ajouter/enlever au tournoi ", end="")
        if tournament:
            print(f"{tournament.name}\n")
            print("Joueurs participant au tournoi :\n")
            for player in tournament.players:
                print(f"{player} [{player.ident}]")
        print("\nTapez [N] pour valider et passer à la suite")
        print("Tapez [C] pour annuler et revenir au menu précédent")
        return input("-->  ")

    def display_all_tournaments(self, tournaments):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Liste des tournois existants\n")
        print(f"{'Nom':<30}{'Ville':<20}{'Pays':<10}\n")
        for tournament in tournaments.values():
            print(f"{tournament} [{tournament.ident}]")
        print("\n Saisissez le numéro du tournoi sélectionné")
        print("Tapez [C] pour annuler et revenir au menu précédent")
        return input("-->  ")

    def show_players_in_tournament(self, tournament, text):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Classement des joueurs du tournoi {tournament.name} {text}\n")
        print(f"{'Nom':<12}{'Prénom':<10}{'Classement':<15}{'Score':<10}\n")
        for player in tournament.players:
            print(f"{player}{tournament.rounds[-1].scores[player.ident]:<10}")
        self.press_key()

    def no_player_in_tournament(self, tournament):
        print(f"Il n'y a actuellement aucun participant pour le tournoi {tournament.name}.")
        self.press_key()

    def not_enought_players_in_tournament(self, tournament):
        print(f"Il faut au moins 2 joueurs pour débuter le tournoi {tournament.name}")
        self.press_key()

    def load_or_create_player(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Voulez-vous charger un joueur existant [L]")
        print("Créer un nouveau joueur                [C]")
        print("Revenir à l'accueil                    [H]")
        print("Quitter                                [Q]")
        return input("-->  ")

    def add_another_player(self):
        return input("Voulez-vous ajouter d'autres joueurs au tournoi ([Y]/[N]) ?")

    def show_matchs_of_the_round(self, tournament):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Matchs de la ronde : {len(tournament.rounds):<15} Début de la ronde : {tournament.rounds[-1].start}\n")
        for match in tournament.rounds[-1].matchs:
            if not match.data[1][0]:
                print(f"\nMatch N° {match.ident}{':':<10} {match.data[0][0]}  {tournament.rounds[-1].scores[match.data[0][0].ident]:<10}Joueur flottant")
            else:
                print(f"Match N° {match.ident}{':':<10} {match.data[0][0]}  {tournament.rounds[-1].scores[match.data[0][0].ident]:<10}{'vs':<10} {match.data[1][0]}  {tournament.rounds[-1].scores[match.data[1][0].ident]:<10}",end="")
                if match.data[0][1]==0 and match.data[1][1]==0:
                    print(f"[{match.ident}]")
                else:
                    print("")

        print("\nSaisissez le numéro du match pour entrer les résultats")
        print("Tapez [N] pour valider ces résultats et passer à la suite")
        return input("-->  ")

    def result_of_a_match(self, match):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Résultat du {match}\n")
        print(
            f"Victoire de            : {match.data[0][0].firstname:>15} {match.data[0][0].lastname:<15}  {'[':>10}{match.data[0][0].ident}]")
        print(
            f"Victoire de            : {match.data[1][0].firstname:>15} {match.data[1][0].lastname:<15}  {'[':>10}{match.data[1][0].ident}]")
        print(f"Match nul              : {'[N]':>45}")
        print(f"Revenir aux matchs     : {'[C]':>45}")
        return input("--> ")

    def some_results_missing(self, tournament):
        print(f"Vous n'avez pas entré tous les résultats de la ronde {len(tournament.rounds)}")
        print(f"Veuillez compléter vos saisies avant de lancer le tour suivant")
        self.press_key()

    def get_data_new_tournament(self):
        data = {"Nom":"Masterchess", "Ville":"New York", "Pays":"USA", "Date de début":"", "Date de fin":"", "Nombre de rondes":4, "Type de partie":"rapid", "Système": "swiss", "Commentaires":""}
        print("Veuillez saisir les informations du nouveau tournoi :")
        for item in data.items():
            entry = input(f"{item[0]} : {item[1]} --> ")
            if entry == "":
                pass
            else:
                data[item[0]] = entry
        return data

    def get_data_new_player(self):
        data = {"Nom":"", "Prénom":"", "Classement": 1000, "Date de naissance":"", "Sexe":""}
        print("Veuillez saisir les informations du nouveau joueur :")
        for item in data.items():
            entry = input(f"{item[0]} : {item[1]} --> ")
            if entry == "":
                pass
            else:
                data[item[0]] = entry
        return data

    def menu_home(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choisissez un menu :")
        print("Tournoi  [T]")
        print("Joueur   [P]")
        print("Rapports [R]")
        print("Quitter  [Q]")
        return input("--> ")

