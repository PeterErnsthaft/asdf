class User:

    def __init__(self, id_nr, name, aliases):

        self.id_nr = id_nr
        self.name = name
        self.aliases = aliases
        self.score = 0

    def print_user(self):
        print ( self.name )
