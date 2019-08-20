""" Institutions that provide schooling to students

"""
from random import normalvariate
from parameters import num_stds_per_universities
from collections import defaultdict


class Universities:
    def __init__(self, id_):
        self.id = id_
        self.places = num_stds_per_universities
        self.balance = 0
        self.studying = list()
        self.tuition = normalvariate(50000, 10000) / 4
        self.ecr = defaultdict(float)

    def deposit(self, amount, ecrm=False, year=2017):
        self.balance += amount
        if ecrm:
            self.ecr[year] += amount

    def register(self, student):
        self.studying.append(student)

    def num_students(self):
        return len(self.studying)

    def deregister(self, student):
        self.studying.remove(student)

    def get_balance(self):
        return self.balance

    def get_tuition(self):
        return self.tuition

    def get_ecr(self, y):
        return self.ecr[y]

    def is_registered(self, student):
        if student in self.studying:
            return True
        else:
            return False

    def check_place(self):
        if len(self.studying) < self.places:
            return True
        else:
            return False

    def __str__(self):
        return 'IFES {} Tuition {:,.2f} Balance {:,.2f}'.format(self.id, self.tuition, self.balance)


if __name__ == '__main__':
    i = Universities(0)
