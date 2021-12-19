import os
import time


class View:
    def __init__(self):
        pass

    def home(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Chess Manager : gestionnaire de tournois d'échecs\n")
        input()

    def load_or_create_tournament(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Voulez-vous charger un tournoi existant [L] ou créer un nouveau tournoi [C] ?\n")
        return input("-->  ")

    def show_players_in_tournament(self, tournament, text):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Classement des joueurs du tournoi {tournament.name} {text}\n")
        print(f"{'Nom':<12}{'Prénom':<10}{'Classement':<15}{'Score':<10}\n")
        for player in tournament.players:
            print(f"{player}{tournament.rounds[-1].scores[player.ident]:<10}")
        print("\nPressez une touche pour continuer")
        return input("-->  ")

    def show_matchs_of_the_round(self, tournament):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Matchs de la ronde : {tournament.rounds[-1].name:<15} Début de la ronde : {tournament.rounds[-1].start}\n")
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
        print(f"Vous n'avez pas entré tous les résultats du {tournament.rounds[-1].name}")
        print(f"Veuillez compléter vos saisies avant de lancer le tour suivant")
        time.sleep(5)