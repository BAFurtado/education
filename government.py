""" This agent represents the government
    The government finances mandatory and discretionary transfers
    """


class Government:

    def __init__(self):
        self.id = 0
        self.balance = 0

    def transfer(self, amount, recipient):
        self.balance -= amount
        recipient.deposit(amount)

    def collect(self, amount):
        self.balance += amount

    def __str__(self):
        return 'Available budget'.format(self.balance)


if __name__ == '__main__':
    g = Government()
