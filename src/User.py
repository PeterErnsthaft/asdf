class User:

    def __init__(self, id_nr, name):

        self.id_nr = id_nr
        self.name = name
        self.aliases = []
        self.score = 0

    def print_user(self): #TODO print whole user data
        print ( self.name )

    def manipulate_score(self, amount):
        self.score += amount