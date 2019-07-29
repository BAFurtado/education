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


def evolve(y):
    for i in range(y):
        pass


if __name__ == '__main__':
    gov, insts, stds = generate_agents(10, 100)
