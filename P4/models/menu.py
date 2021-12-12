"""
Manage the menus of the script
"""


class Menu:
    def __init__(self, name, m_id):
        self.name = name
        self.id = m_id
        self.submenus = {}
        self.path = []
        self.choices = None
