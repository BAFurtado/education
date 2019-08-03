import random

from wages import generate_wage


class Citizens:
    def __init__(self, id_):
        self.id = id_
        self.graduate = False
        self.age = 19
        self.schooling = None
        self.ifes = None
        self.balance = 0
        self.debt = 0
        self.gender = random.choices(['Male', 'Female'], [.4, .6])[0]
        # Draw a number from Beta distribution to get a Gini distribution for Brazil
        # Multiply by the inverse of the average of the Beta distribution to have an average mean
        self.wage = generate_wage(24, self.gender)

    def collate(self):
        self.graduate = True

    def update_age(self):
        self.age += 1

    def update_schooling(self):
        self.schooling += 1

    def update_debt(self, amount):
        self.debt += amount

    def debt_interest(self, r):
        self.debt *= r

    def register(self, ife, y):
        self.ifes = ife
        self.schooling = y

    def income(self, amount):
        self.balance += amount

    def update_wage(self):
        self.wage = generate_wage(self.get_age(), self.gender)

    def transfer(self, amount):
        self.balance -= amount
        return amount

    def pay_principal(self, amount):
        self.debt -= amount

    def set_debt(self):
        self.debt = 0

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

    def get_wage(self):
        return self.wage

    def __str__(self):
        return 'Student {}. Age {}. Graduate: {} Wage: {:,.2f}'.format(self.id, self.age, self.graduate, self.wage)


if __name__ == '__main__':
    c = Citizens(0)
    c.collate()
    print(c)
