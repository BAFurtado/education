""" This module reads an external file that provides expected wages per age for Males and Females """


import pandas as pd
from scipy.stats import truncnorm
import parameters

# Reads original data (from Paulo Meyer) to generate 'dynamic' wages procedures
# data = pd.read_csv('dinamico.csv')
#
# cols = [col for col in data.columns if 'income' in col] + ['id', 'female']
# wage_dynamic = data.loc[:, cols]
#
# female = wage_dynamic.loc[wage_dynamic['female'] == 1]
# male = wage_dynamic.loc[wage_dynamic['female'] == 0]
# female.to_csv('female.csv', sep=';')
# male.to_csv('male.csv', sep=';')


if parameters.wage_rules == 'static':
    wages = pd.read_csv('wage_params.csv', sep=',')
    wages.index = wages.age
    wages.drop('age', axis=1, inplace=True)
else:
    wages_m = pd.read_csv('male.csv', sep=';')
    wages_m.drop(['Unnamed: 0', 'female'], axis=1, inplace=True)
    wages_f = pd.read_csv('female.csv', sep=';')
    wages_f.drop(['Unnamed: 0', 'female'], axis=1, inplace=True)


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    # Generates a distribution from the average and standard-deviation
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def generate_wage(age, gender, id=None):
    age = str(age)
    if parameters.wage_rules == 'static':
        # Given an age and gender, it returns a value from the distribution
        out = get_truncated_normal(mean=wages.loc[gender + age, 'avg'],
                                   sd=wages.loc[gender + age, 'std'],
                                   low=wages.loc[gender + age, 'min'],
                                   upp=wages.loc[gender + age, 'max'])
        return out.rvs()
    else:
        if gender == 'female':
            return wages_f.loc[wages_f['id'] == id, 'income' + age].iloc[0]
        else:
            return wages_m.loc[wages_m['id'] == id, 'income' + age].iloc[0]


if __name__ == '__main__':
    l = list()
    for k in range(2):
        for i in range(24, 65):
            for j in ['Male', 'Female']:
                age = i
                gender = j
                l.append(generate_wage(age, gender, 5328))
    print(l)
