import random

from government import Government
from ifes import Institutions
from students import Citizens
import output
import parameters


def loop(agent, n):
    l = list()
    for i in range(n):
        l.append(agent(i))
    return l


def generate_agents(ni, ns):
    g = Government()
    inst = loop(Institutions, ni)
    std = loop(Citizens, ns)
    return g, inst, std


def evolve(g, ins, std):
    """ What happens every year?
    """
    # Cycle over the years
    for y in range(parameters.period):
        # 1. Government transfer
        # Cycle over institutions
        for f in ins:
            g.transfer(parameters.transfer_amount, f)
        # Cycle over students
        # 2. Students enter school
        for each in std:
            if each.get_ifes() is not None:
                each.update_schooling()
                each.update_debt(parameters.year_tuition)
            if (each.get_age() == 18) and (each.get_ifes() is None):
                school = random.choice(ins)
                school.register(each)
                each.register(school, y)
        # 3. Students graduate
            if each.get_schooling() is not None:
                if each.get_schooling() > parameters.grad_len:
                    each.collate()
        # 4. Students receive payment
            if each.get_graduate() is True:
                wage = parameters.min_wage * each.get_schooling()
                each.income(wage)
        # 5. Ifes collects payment
                ifs = each.get_ifes()
                if each.get_debt() > 0:
                    max_payment = wage * parameters.ecr
                    if max_payment > each.get_debt():
                        ifs.deposit(each.transfer(max_payment))
                        each.pay_principal(max_payment)
                    else:
                        ifs.deposit(each.transfer(each.get_debt()))
                        each.pay_principal(each.get_debt())
            # Update age
            each.update_age()
    return g, ins, std




if __name__ == '__main__':
    gov, insts, stds = generate_agents(parameters.num_ifes, parameters.num_stds)
    gov, insts, stds = evolve(gov, insts, stds)
    output.produce_output(gov, insts, stds)
