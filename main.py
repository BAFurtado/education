import random

from government import Government
from ifes import Institutions
from students import Citizens


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


def evolve(y, g, ins, std):
    """ What happens every year?
    """
    for i in range(y):
        # 1. Government transfer
        for each in ins:
            g.transfer(10, each)
        # 2. Students enter school
        for each in std:
            if each.age == 15:
                school = random.choice(ins)
                school.register(each)
                each.register(school, i)
        # 3. Students graduate
        # 4. Students receive payment
        # 5. Ifes/Goverment collect payment


if __name__ == '__main__':
    gov, insts, stds = generate_agents(10, 100)
    evolve(10, gov, insts, stds)
