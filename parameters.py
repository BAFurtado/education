
sampling_stds = 100
num_hei = 63
transfer_amount_per_hei = 5000000000 / num_hei
starting_year = 2017
period = 10

grad_len = 4
# Extra fee to participate in ICL program on top of full tuition
surcharge = .25

# Interests
interest_on_tuition = 0.028

graduate_num_2017 = int(151376 / sampling_stds)
num_stds_per_year = graduate_num_2017
num_stds_per_hei = int((num_stds_per_year * grad_len) / num_hei)

# Wage rules
# If static, drawing from truncated normal from wages.py
# If dynamic, drawing from 20,000 sample individuals read from female.csv and male.csv
# Options: 'dynamic' or 'static'
wage_rules = 'static'
