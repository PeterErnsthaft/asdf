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

    def serialize(self):
        # TODO implement some serious serialization when User starts having object attributes
        # see: http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
        # not 100% trustworthy: https://www.reddit.com/r/Python/comments/2kq4a0/pypi_packages_safe/
        #                            ->     https://pypi.python.org/pypi/jsonpickle/0.4.0
        return self.__dict__
