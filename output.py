import parameters
from numpy import median


def print_parameters():
    print('This run used the following parameters')
    print('Amount transfered per year, per institution: {}'.format(parameters.transfer_amount))
    print('Number of years run: {}'.format(parameters.period))
    print('Number of institutions: {}'.format(parameters.num_ifes))
    print('Number of students: {}'.format(parameters.num_stds))
    print('Lenght of years studying: {}'.format(parameters.grad_len))
    print('Minimum wage: {}'.format(parameters.min_wage))
    print('ECR percentage discounted from wages: {}'.format(parameters.ecr))
    print('Percentage cost of tuition per year: {}'.format(parameters.year_tuition))


def produce_output(g, ins, st):
    print_parameters()
    print('---------------------------')
    print('Government balance is: ${}'.format(g.balance))
    print('Median balance of students: ${:.2f}'.format(median([s.balance for s in st])))
    print('Median balance of institutions: ${:.2f}'.format(median([i.balance for i in ins])))
