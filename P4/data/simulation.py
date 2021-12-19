players_data = {"1": ("Prof", "Albert", 1, (1975, 5, 17), "M"),
                "2": ("Neige", "Blanche", 2, (1974, 2, 9), "F"),
                "3": ("Joyeux", "Noël", 556, (1980, 11, 23), "M"),
                "4": ("Distrait", "Anatole", 17, (1980, 11, 23), "M"),
                "5": ("Simplet", "Victor", 223, (1988, 1, 3), "M"),
                "6": ("Timide", "Jean-Pierre", 45, (1990, 9, 9), "M"),
                "7": ("Grincheux", "Marcel", 688, (1980, 2, 29), "M"),
                "8": ("Dormeur", "Paul", 103, (1985, 10, 5), "M"),
                "9": ("Pan", "Peter", 777, (1948, 8, 22), "M"),
                "10": ("Haddock", "Archibald", 51, (1933, 6, 30), "M"),
                "11": ("Bond", "James", 7, (1977, 7, 7), "M"),
                "12": ("Kasparov", "Gary", 3, (1963, 4, 13), "M"),
                "13": ("Duck", "Donald", 10, (1958, 2, 21), "M")}

rounds_data = {"1": ("Round 1", ["2", "3", "4", "5", "6", "8", "9", "10", "11"], {}, [], (2021, 12, 10, 15, 10, 30))}  # (name, players, scores, matchs, time_start)

# name, town, country, starting date, ending date, status, control time, description, system, nb rounds, rounds, players, singleton
tournaments_data = {"1": ("Europe Grand Masters", "Paris", "France", (2022,7,14), (2022, 7, 16), "in progress", "rapid", "", "swiss", 4, ["1"], ["2", "3", "4", "5", "6", "8", "9", "10", "11"], [])}

matchs_data = {}  # data format = {id: ([player1, score1], [player2, score2])}
