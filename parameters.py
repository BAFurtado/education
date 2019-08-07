
sampling_stds = 100
num_ifes = 63
transfer_amount_per_ifes = 5000000000 / num_ifes
starting_year = 2017
period = 10

grad_len = 4
# Extra fee to participate in ECR program on top of full tuition
surcharge = .25

# Interests
interest_on_tuition = 0.028
real_interest_on_wages = 0.01

graduate_num_2017 = int(151376 / sampling_stds)
num_stds_per_year = graduate_num_2017
num_stds_per_ifes = int((num_stds_per_year * grad_len) / num_ifes)
