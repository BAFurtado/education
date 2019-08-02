
sampling_stds = 100
num_ifes = 63
transfer_amount_per_ifes = 5200000000 / num_ifes
starting_year = 2017
period = 30

grad_len = 4
# Extra fee to participate in ECR program on top of full tuition
surcharge = .25

# capacity_stds = 483137
# entering_stds_2013 = 325267
graduate_num_2017 = int(151376 / sampling_stds)
num_stds_per_year = int(graduate_num_2017 / grad_len)
num_stds_per_ifes = int(num_stds_per_year / num_ifes)
avg_wage = 1401 * 12


# Collate at 23
# Wage at 24