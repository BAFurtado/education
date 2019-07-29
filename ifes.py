""" Institutions that provide schooling to students

"""


class Institutions:
    def __init__(self, id_):
        self.id = id_
        self.places = 0
        self.balance = 0
        self.studying = list()

    def deposit(self, amount):
        self.balance += amount

    def open_places(self, amount):
        self.places += amount

    def register(self, student):
        self.studying.append(student)

    def get_balance(self):
        return self.balance


if __name__ == '__main__':
    i = Institutions(0)
