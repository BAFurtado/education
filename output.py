import parameters
from numpy import median


def print_parameters():
    print('This run used the following parameters')
    print('Amount transfered per year, per institution: {:,.0f}'.format(parameters.transfer_amount_per_std))
    print('Number of years simulation run: {}'.format(parameters.period))
    print('Number of institutions: {}'.format(parameters.num_ifes))
    print('Number of citizens: {}'.format(parameters.num_citizens))
    print('Lenght of years to graduate: {}'.format(parameters.grad_len))
    print('Minimum wage: {}'.format(parameters.min_wage))
    print('ECR percentage discounted from wages: {}'.format(parameters.ecr))
    print('Percentage cost of tuition per year: {}'.format(parameters.year_tuition))


def produce_output(g, ins, st):
    print_parameters()
    print('---------------------------')
    print('Government balance is: ${:,.0f}'.format(g.balance))
    print('Median wealth of citizens: ${:,.2f}'.format(median([s.get_balance() for s in st])))
    print('Median wealth of graduates: ${:,.2f}'.format(median([s.get_balance() for s in st if s.graduate])))
    print('Median debt of students: ${:,.2f}'.format(median([s.get_debt() for s in st if s.graduate])))
    print('Expected Median balance of institutions with Government transfer only: ${:,.2f}'.format(parameters.period * parameters.transfer_amount_per_std))
    print('Median balance of institutions: ${:,.2f}'.format(median([i.get_balance() for i in ins])))
    print('Graduated students in the economy: {:,.0f}'.format(sum([s.graduate is True for s in st])))
