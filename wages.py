import pandas as pd
from scipy.stats import truncnorm


wages = pd.read_csv('wage_params.csv', sep=',')
wages.index = wages.age
wages.drop('age', axis=1, inplace=True)


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def generate_wage(age, gender):
    out = get_truncated_normal(mean=wages.loc[gender + str(age), 'avg'],
                               sd=wages.loc[gender + str(age), 'std'],
                               low=wages.loc[gender + str(age), 'min'],
                               upp=wages.loc[gender + str(age), 'max'])
    return out.rvs()


if __name__ == '__main__':
    l = list()
    for k in range(100):
        for i in range(24, 65):
            for j in ['Male', 'Female']:
                age = i
                gender = j
                l.append(generate_wage(age, gender))
