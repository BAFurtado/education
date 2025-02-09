""" These are auxiliary functions that calculate Income Contingent Loans (ICL).
"""

import os

import pandas as pd
from numpy import npv

import parameters

# ICL is tested for the Brazilian case using the same table used for Income Rate discounts. In Reals R$.
icl = {'initial_threshold': [0, 22847.76, 0],
       'threshold2': [22847.77, 33919.8, 0.0375],
       'threshold3': [33919.81, 45012.6, 0.075],
       'threshold4': [45012.61, 55976.16, 0.1125],
       'threshold5': [55976.16, 1000000, 0.1375]}


def calculate_icl_max(income, value=0):
    """ Calculates ICL considering marginal values by income thresholds
        Given an income, it returns the amount to be deducted.
    """
    if income < icl['initial_threshold'][1]:
        return value
    elif income < icl['threshold2'][1]:
        value += (income - icl['threshold2'][0]) * icl['threshold2'][2]
        return calculate_icl_max(income - icl['threshold2'][0], value=value)
    elif income < icl['threshold3'][1]:
        value += (income - icl['threshold3'][0]) * icl['threshold3'][2]
        return calculate_icl_max(income - icl['threshold3'][0], value=value)
    elif income < icl['threshold4'][1]:
        value += (income - icl['threshold4'][0]) * icl['threshold4'][2]
        return calculate_icl_max(income - icl['threshold4'][0], value=value)
    elif income < icl['threshold5'][1]:
        value += (income - icl['threshold5'][0]) * icl['threshold5'][2]
        return calculate_icl_max(income - icl['threshold5'][0], value=value)
    return value


def register_values(value, year, name):
    """ Save yearly information to a file """
    if year == parameters.starting_year:
        if os.path.exists(name):
            os.remove(name)
        with open(name, 'a') as f:
            f.write('value;year\n')
            f.write('{};{}\n'.format(value, year))
    else:
        with open(name, 'a') as f:
            f.write('{};{}\n'.format(value, year))


def calculate_npv(value, year, add_data=True):
    """ Calculates the present value"""
    file_name = 'results/nominal_value_{}.csv'.format(parameters.wage_rules)
    if add_data:
        register_values(value, year, file_name)
    data = pd.read_csv(file_name, sep=';')
    present_value = npv(parameters.interest_on_tuition, data.value)
    if add_data:
        register_values(present_value, year, 'results/present_value_{}.csv'.format(parameters.wage_rules))
    return present_value


if __name__ == '__main__':
    print(calculate_icl_max(14000))
    # for i in range(10000, 300000, 20000):
    #     print('Renda: {:,.0f}, ECR: {:,.0f}'.format(i, calculate_icl_max(i)))
