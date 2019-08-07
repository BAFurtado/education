import logging
import random

import ecr
import output
import parameters
import plotter
from government import Government
from ifes import Institutions
from students import Citizens

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def loop(agent, n):
    l = list()
    for i in range(n):
        l.append(agent(i))
    return l


def generate_agents(ni):
    g = Government()
    inst = loop(Institutions, ni)
    return g, inst


def generate_std_candidates(size, lst):
    for i in range(size):
        lst.append(Citizens(i))
    return lst


def gov_transfers(g, ins):
    # 1. Government transfer
    # Cycle over institutions
    for f in ins:
        g.transfer(parameters.transfer_amount_per_ifes, f)
    return g, ins


def pay_tuition(s, year):
    ifs = s.get_ifes()
    if s.get_debt() > 0:
        max_payment = ecr.calculate_ecr_max(s.get_wage())
        if max_payment > 0:
            if max_payment < s.get_debt():
                ifs.deposit(max_payment * parameters.sampling_stds, ecrm=True, year=year)
                s.pay_principal(max_payment)
            else:
                ifs.deposit(s.get_debt() * parameters.sampling_stds, ecrm=True, year=year)
                s.pay_principal(s.get_debt())
                s.set_debt()


def evolve(g, ins, std):
    """ What happens every year?
    """
    # Cycle over the years
    for y in range(parameters.starting_year, parameters.starting_year + parameters.period):
        logger.info('Initiating year {}...'.format(y))

        # Government yearly transferes
        g, ins = gov_transfers(g, ins)

        # Citizens get paid for the first time
        [i.income(i.get_wage()) for i in std if i.get_age() == 24]

        # Generate students for a given year
        # First 4 years populate the system
        if y < parameters.starting_year + 3:
            logger.info('Generating {:,.0f} students...'
                        .format(parameters.num_stds_per_year * parameters.sampling_stds))
            std = generate_std_candidates(parameters.num_stds_per_year, std)
        else:
            num = sum([i.num_students() for i in ins])
            size = parameters.graduate_num_2017 - num
            logger.info('Generating {:,.0f} students...'.format(size))
            std = generate_std_candidates(size, std)

        # Cycle over students
        logger.info('Cycling over {:,.0f} students...'.format(len(std) * parameters.sampling_stds))
        for each in std:
            # Estimated number of agents: 470 thousand
            # Registering at first year
            if (each.get_age() == 19) & (each.get_ifes() is None):
                # All students at 19 enter the system somewhere
                while each.get_ifes() is None:
                    school = random.choice(ins)
                    if school.check_place():
                        school.register(each)
                        each.register(school, 0)
                        # Add extra 25% tuition fee on top of total value
                        each.update_debt(school.get_tuition() * parameters.grad_len * parameters.surcharge)
                    else:
                        print('place not found')
            # If registered, updated debt and years of study
            if each.get_ifes() is not None:
                each.update_schooling()
                if each.get_ifes().is_registered(each):
                    each.update_debt(each.get_ifes().get_tuition())
            # 1. Students enter school
            # 2. Graduate students
            if each.get_graduate() is False and each.get_ifes() is not None:
                if each.get_schooling() == parameters.grad_len:
                    each.collate()
                    # Deregister at school and open up place
                    each.get_ifes().deregister(each)

            # 3. Ifes collect payment
            if each.get_ifes() is not None and each.get_age() > 23:
                pay_tuition(each, year=y)
            # Update age
            each.update_age()
            if each.get_age() > 65:
                std.remove(each)

        # 4. Free students without debt
        logger.info('Providing documentation for students who have paid their debts...')
        debt_free = [s for s in std if s.get_ifes() is not None and s.get_debt() == 0]
        for df in debt_free:
            std.remove(df)

        # 5. Update debts using interest rate
        [s.debt_interest(parameters.interest_on_tuition + 1) for s in std if s.get_wage() > ecr.ecr['isento'][1]]

        # 6. Update wages using distribution if students are over 24
        [i.update_wage() for i in std if i.get_age() > 24]
        [i.income(i.get_wage()) for i in std if i.get_age() > 24]

        # Register ECR hitherto
        print('ECR up to year {} at present value: ${:,.0f}'
              .format(y, ecr.calculate_npv(sum([i.get_ecr(y) for i in ins]), y)))

    return g, ins, std


if __name__ == '__main__':
    stds = list()
    gov, insts = generate_agents(parameters.num_ifes)
    gov, insts, stds = evolve(gov, insts, stds)
    output.produce_output(gov, insts, stds)
