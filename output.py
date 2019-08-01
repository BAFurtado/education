import parameters
from numpy import median


def print_parameters():
    print('This run used the following parameters')
    print('Amount transferred per year, per institution: {:,.0f}'.format(parameters.transfer_amount_per_ifes))
    print('Number of years simulation run: {}'.format(parameters.period))
    print('Number of institutions: {}'.format(parameters.num_ifes))
    print('Length of years to graduate: {}'.format(parameters.grad_len))
    print('Average per capita wage ex-ante: {:,.0f}'.format(parameters.avg_wage))


def produce_output(g, ins, st):
    print_parameters()
    print('---------------------------')
    print('Government transfer in the period: ${:,.0f}'.format(g.balance))
    print('Median wage of graduates ex-post: ${:,.2f}'.format(median([s.get_wage() for s in st])))
    print('Median wealth of graduates: ${:,.2f}'.format(median([s.get_balance() for s in st if s.graduate])))
    print('Median debt of students: ${:,.2f}'.format(median([s.get_debt() for s in st if s.graduate])))
    inst_gov_transfer = parameters.period * parameters.transfer_amount_per_ifes
    print('Expected Median balance of institutions with Government transfer only: ${:,.0f}'
          .format(inst_gov_transfer))
    print('Median ECR gain per institution: ${:,.2f}'
          .format(median([i.get_balance() for i in ins]) - inst_gov_transfer))
    print('Graduated students in the economy: {:,.0f}'
          .format(sum([s.graduate is True for s in st]) * parameters.sampling_stds))
