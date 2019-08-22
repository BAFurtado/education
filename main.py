""" This module contains the main sequence of events of the model """

import logging
import random

import icl
import output
import parameters
import plotter
import os
from agents.government import Government
from agents.institutions import Universities
from agents.students import Students

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def loop(agent, n):
    """ Creates an agent"""
    l = list()
    for i in range(n):
        l.append(agent(i))
    return l


def generate_agents(ni):
    g = Government()
    inst = loop(Universities, ni)
    return g, inst


def generate_std_candidates(size, lst):
    for i in range(size):
        lst.append(Students(i))
    return lst


def gov_transfers(g, ins):
    # 1. Government transfer
    # Cycle over institutions
    for f in ins:
        g.transfer(parameters.transfer_amount_per_hei, f)
    return g, ins


def pay_tuition(s, year):
    ifs = s.get_hei()
    if s.get_debt() > 0:
        max_payment = icl.calculate_icl_max(s.get_wage())
        if max_payment > 0:
            if max_payment < s.get_debt():
                ifs.deposit(max_payment * parameters.sampling_stds, iclm=True, year=year)
                s.pay_principal(max_payment)
            else:
                ifs.deposit(s.get_debt() * parameters.sampling_stds, iclm=True, year=year)
                s.pay_principal(s.get_debt())
                s.set_debt()


def evolve(g, ins, std):
    """ What happens every year?
    """
    # Cycle over the years
    for y in range(parameters.starting_year, parameters.starting_year + parameters.period):
        logger.info('Initiating year {}...'.format(y))

        # Government yearly transfers
        g, ins = gov_transfers(g, ins)

        # Generate students for a given year
        # First 4 years populate the system
        if y < parameters.starting_year + 4:
            logger.info('Generating {:,.0f} students...'
                        .format(parameters.num_stds_per_year * parameters.sampling_stds))
            std = generate_std_candidates(parameters.num_stds_per_year, std)
        else:
            # Afterwards, check the number of available positions
            num = sum([i.num_students() for i in ins])
            size = (parameters.graduate_num_2017 * parameters.grad_len) - num
            # Check if number of students is above capacity of the system
            if size < 0:
                size = 0
            logger.info('Generating {:,.0f} new students...'.format(size * parameters.sampling_stds))
            std = generate_std_candidates(size, std)

        # Cycle over students
        logger.info('Cycling over {:,.0f} students... and graduates...'.format(len(std) * parameters.sampling_stds))
        for each in std:
            # Estimated number of agents: 470 thousand
            # Registering at first year
            if (each.get_age() == 20) & (each.get_hei() is None):
                # All students at 19 enter the system somewhere
                while each.get_hei() is None:
                    school = random.choice(ins)
                    if school.check_place():
                        school.register(each)
                        each.register(school, 0)
                        # Add extra 25% tuition fee on top of total value
                        each.update_debt(school.get_tuition() * parameters.grad_len * parameters.surcharge)

            # Update age
            each.update_age()
            if each.get_age() > 65:
                std.remove(each)

            # If registered, updated debt and years of study
            if each.get_hei() is not None:
                each.update_schooling()
                if each.get_hei().is_registered(each):
                    each.update_debt(each.get_hei().get_tuition())
            # 1. Students enter school
            # 2. Graduate students
            if each.get_graduate() is False and each.get_hei() is not None:
                if each.get_schooling() == parameters.grad_len:
                    each.collate()
                    # Deregister at school and open up place
                    each.get_hei().deregister(each)

        # 4. Free students without debt
        logger.info('Providing documentation for students who have paid their debts...')
        debt_free = [s for s in std if s.get_hei() is not None and s.get_debt() == 0]
        for df in debt_free:
            std.remove(df)

        # 5. Update debts using interest rate
        [s.debt_interest(parameters.interest_on_tuition + 1) for s in std if s.get_wage() > icl.icl['initial_threshold'][1]]

        # 6. Update wages using distribution if students are over 24
        # Citizens get paid for the first time
        [i.income(i.get_wage()) for i in std if i.get_age() == 24]
        [i.update_wage() for i in std if i.get_age() > 24]
        [i.income(i.get_wage()) for i in std if i.get_age() > 24]

        # 3. Ifes collect payment
        [pay_tuition(i, year=y) for i in std if i.get_hei() is not None and i.get_age() > 23]

        # Register ICL hitherto
        nominal_value = sum([i.get_icl(y) for i in ins])
        print('ICL for year {}: nominal value ${:,.0f}. Total present value: ${:,.0f}'
              .format(y, nominal_value, icl.calculate_npv(nominal_value, y)))

    return g, ins, std


def main():
    stds = list()
    gov, insts = generate_agents(parameters.num_hei)
    gov, insts, stds = evolve(gov, insts, stds)
    output.produce_output(gov, insts, stds)
    files = [f for f in os.listdir('results') if 'csv' in f]
    for f in files:

        plotter.plotting('results/' + f)


if __name__ == '__main__':
    main()
