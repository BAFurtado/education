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


def gov_transfers(g, ins):
    # 1. Government transfer
    # Cycle over institutions
    for f in ins:
        g.transfer(parameters.transfer_amount_per_std, f)
    return g, ins


def pay_tuition(s):
    ifs = s.get_ifes()
    if s.get_debt() > 0:
        max_payment = s.get_wage() * parameters.ecr
        if max_payment < s.get_debt():
            ifs.deposit(s.transfer(max_payment))
            s.pay_principal(max_payment)
        else:
            ifs.deposit(s.transfer(s.get_debt()))
            s.pay_principal(s.get_debt())


def evolve(g, ins, std):
    """ What happens every year?
    """
    # Cycle over the years
    for y in range(parameters.period):

        # Government yearly transferes
        g, ins = gov_transfers(g, ins)

        # Citizens get paid
        [i.income(i.get_wage()) for i in std]

        # Cycle over students
        for each in std:
            # If registered, updated debt and years of study
            if each.get_ifes() is not None:
                each.update_schooling()
                if each.get_ifes().is_registered(each):
                    each.update_debt(parameters.year_tuition)
            # 1. Students enter school
            # TODO: Change citizens to generators, immediately before entereing school.
            #  a quarter of places untile year 4 and num_places henceforth
            # Estimated number of agents: 470 thousand
            if (each.get_age() > 18 & each.get_age() < 30) & (each.get_ifes() is None):
                school = random.choice(ins)
                if school.check_place():
                    school.register(each)
                    each.register(school, y)
            # 2. Graduate students
            if each.get_graduate() is False and each.get_ifes() is not None:
                if each.get_schooling() > parameters.grad_len:
                    each.collate()
                    # Deregister at school and open up place
                    each.get_ifes().deregister(each)

            # 3. Ifes collect payment
            if each.get_ifes() is not None:
                pay_tuition(each)
            # Update age
            each.update_age()
            if each.get_age() > 80:
                if random.random() > .5:
                    std.remove(each)
    return g, ins, std


if __name__ == '__main__':
    gov, insts, stds = generate_agents(parameters.num_ifes, parameters.num_citizens)
    gov, insts, stds = evolve(gov, insts, stds)
    output.produce_output(gov, insts, stds)
