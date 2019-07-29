import random


class Citizens:
    def __init__(self, id_):
        self.id = id_
        self.graduate = False
        self.age = random.randint(5, 25)
        self.year = 0
        self.ifes = None

    def collate(self):
        self.graduate = True

    def update_age(self):
        self.age += 1

    def register(self, ife, y):
        self.ifes = ife
        self.year = y


    def __str__(self):
        return 'Student {}. Graduate: {}'.format(self.id, self.graduate)


if __name__ == '__main__':
    c = Citizens(0)
    c.collate()
    print(c)
