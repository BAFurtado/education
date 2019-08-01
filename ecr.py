

ecr = {'isento': [0, 22847.76, 0],
       'faixa2': [22847.77, 33919.8, 0.0375],
       'faixa3': [33919.81, 45012.6, 0.075],
       'faixa4': [45012.61, 55976.16, 0.1125],
       'faixa5': [55976.16, 1000000, 0.1375]}


def calculate_ecr_max(income, value=0):
    if income < ecr['isento'][1]:
        return value
    elif income < ecr['faixa2'][1]:
        value += (income - ecr['faixa2'][0]) * ecr['faixa2'][2]
        return calculate_ecr_max(income - ecr['faixa2'][0], value=value)
    elif income < ecr['faixa3'][1]:
        value += (income - ecr['faixa3'][0]) * ecr['faixa3'][2]
        return calculate_ecr_max(income - ecr['faixa3'][0], value=value)
    elif income < ecr['faixa4'][1]:
        value += (income - ecr['faixa4'][0]) * ecr['faixa4'][2]
        return calculate_ecr_max(income - ecr['faixa4'][0], value=value)
    elif income < ecr['faixa5'][1]:
        value += (income - ecr['faixa5'][0]) * ecr['faixa5'][2]
        return calculate_ecr_max(income - ecr['faixa5'][0], value=value)
    return value


if __name__ == '__main__':
    print(calculate_ecr_max(14000))
    # for i in range(10000, 300000, 20000):
    #     print('Renda: {:,.0f}, ECR: {:,.0f}'.format(i, calculate_ecr_max(i)))
