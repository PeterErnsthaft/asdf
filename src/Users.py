import User

class Users:

    def __init__(self):
        self.list = []

    def add_user(self,msg):
        id_ = msg['from']['id']
        name_ = msg['from']['first_name']

        # find out whether the user already exists
        is_new_user = "true"
        for user in self.list:
            if id_ == user.id_nr:
                is_new_user = False
                break

        # accordingly add it or don't
        if is_new_user:
            self.list.append(User.User(id_, name_))
            output = "added user: " + name_;
        else:
            output = "I already made your acquaintance " + name_ + "."

        return output


    def get_user(self, user_name):
        '''find the user of the given name in the users list and return it,
        if it does not exist delete return false'''
        for user in self.list:
            names = user.aliases
            names.append(user.name)
            for name in names:
                if user_name == name:
                    return user
        return False