"""
Manage the menus of the script
"""


class Menu:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.submenus = {}
        self.path = []
        self.choices = None




