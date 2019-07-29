""" This agent represents the government
    The government finances mandatory and discretionary transfers
    """


class Government:

    def __init__(self):
        self.id = 0
        self.balance = 1000

    def transfer(self, amount, recipient):
        self.balance -= amount


if __name__ == '__main__':
    g = Government()
