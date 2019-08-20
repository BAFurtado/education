from numpy import median

import ecr
import parameters


def print_parameters():
    print('Age students start getting paid: 24. Age debts start getting collected: 24.')
    print('This run used the following parameters')
    print('Amount transferred per year, per institution: {:,.0f}'.format(parameters.transfer_amount_per_universities))
    print('Number of years simulation run: {}'.format(parameters.period))
    print('Number of institutions: {}'.format(parameters.num_universities))
    print('Length of years to graduate: {}'.format(parameters.grad_len))


def produce_output(g, ins, st):
    print_parameters()
    print('---------------------------')
    print('Government transfer in the period: ${:,.0f}'.format(g.balance))
    print('Median wage of graduates ex-post: ${:,.0f}'.format(median([s.get_wage() for s in st])))
    print('Median wealth of graduates: ${:,.0f}'.format(median([s.get_balance() for s in st if s.graduate])))
    print('Median debt of students: ${:,.0f}'.format(median([s.get_debt() for s in st if s.graduate])))
    inst_gov_transfer = parameters.period * parameters.transfer_amount_per_universities
    print('Expected Median balance of institutions with Government transfer only: ${:,.0f}'
          .format(inst_gov_transfer))
    print('Median ECR gain per institution: ${:,.0f}'
          .format(median([i.get_balance() for i in ins]) - inst_gov_transfer))
    print('Total ECR gain in nominal value at end of period: ${:,.0f}'
          .format(sum([i.get_balance() for i in ins]) - (inst_gov_transfer * parameters.num_universities)))
    print('Graduated students in the economy: {:,.0f}'
          .format(sum([s.graduate is True for s in st]) * parameters.sampling_stds))
    print('ECR up to year {} at present value: ${:,.0f}'
          .format(parameters.starting_year + parameters.period, ecr.calculate_npv(None, None, False)))
