class BotUser:

    def __init__(self, id_nr, name, score=0, aliases=[]):
        self.id_nr = id_nr
        self.name = name
        self.aliases = aliases
        self.score = score

    def print_user(self): #TODO print whole user data
        print(self.name)

    def manipulate_score(self, amount):
        self.score += amount

    def add_alias(self, alias):
        alias_lower = alias.lower()  # converted to lower case
        self.aliases.append(alias_lower)

