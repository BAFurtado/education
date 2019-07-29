

class Citizens:
    def __init__(self, id_):
        self.id = id_
        self.graduate = False

    def collate(self):
        self.graduate = True

    def __str__(self):
        return 'Student {}. Graduate: {}'.format(self.id, self.graduate)


if __name__ == '__main__':
    c = Citizens(0)
    c.collate()
    print(c)
