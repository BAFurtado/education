import random


class Citizens:
    def __init__(self, id_):
        self.id = id_
        self.graduate = False
        self.age = random.randint(0, 65)
        self.schooling = None
        self.ifes = None
        self.balance = 0
        self.debt = 0

    def collate(self):
        self.graduate = True

    def update_age(self):
        self.age += 1

    def update_schooling(self):
        self.schooling += 1

    def update_debt(self, amount):
        self.debt += amount

    def register(self, ife, y):
        self.ifes = ife
        self.schooling = y

    def income(self, amount):
        self.balance += amount

    def transfer(self, amount):
        self.balance -= amount
        return amount

    def pay_principal(self, amount):
        self.debt -= amount

    def get_age(self):
        return self.age

    def get_debt(self):
        return self.debt

    def get_balance(self):
        return self.balance

    def get_schooling(self):
        return self.schooling

    def get_graduate(self):
        return self.graduate

    def get_ifes(self):
        return self.ifes

    def __str__(self):
        return 'Student {}. Age {}. Graduate: {}'.format(self.id, self.age, self.graduate)


if __name__ == '__main__':
    c = Citizens(0)
    c.collate()
    print(c)
