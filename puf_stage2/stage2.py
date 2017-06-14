import numpy as np
import pandas as pd
from solve_lp_for_year import (solve, solve_lp_for_year_cylp,
                               solve_lp_for_year_reformat)

# Read private CPS-matched-PUF file into a Pandas DataFrame
puf = pd.read_csv("../puf_data/cps-matched-puf.csv")

# Read stage1 factors and stage2 targets written by stage1.py script
Stage_I_factors = pd.read_csv("../stage1/Stage_I_factors_transpose.csv",
                              index_col=0)
Stage_II_targets = pd.read_csv("../stage1/Stage_II_targets.csv",
                               index_col=0)

# Use the matched_weight variable in CPS as the final weight

# Create two-dimensional array to hold sample weights for each year
length = len(puf.s006)
z = np.empty([length, 18])
z[:, 0] = puf.s006

# puf_samp = puf.sample(n=length/10, weights=puf.s006)

# Execute stage2 logic for each year using a year-specific LP tolerance
df_orig = solve(puf, Stage_I_factors, Stage_II_targets, "2010", 0.45,
                solve_lp_for_year_cylp)
df_orig.to_csv('weights_orig_2010.csv', index=False)
df_test = solve(puf, Stage_I_factors, Stage_II_targets, "2010", 0.45,
                solve_lp_for_year_reformat)
df_test.to_csv('weights_test_2010.csv', index=False)
# z[:, 2] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2011', tol=0.45)
# z[:, 3] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2012', tol=0.52)
# z[:, 4] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2013', tol=0.47)
# z[:, 5] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2014', tol=0.50)
# z[:, 6] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2015', tol=0.50)
# z[:, 7] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2016', tol=0.51)
# z[:, 8] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2017', tol=0.51)
# z[:, 9] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                             year='2018', tol=0.52)
# z[:, 10] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2019', tol=0.52)
# z[:, 11] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2020', tol=0.52)
# z[:, 12] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2021', tol=0.54)
# z[:, 13] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2022', tol=0.53)
# z[:, 14] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2023', tol=0.53)
# z[:, 15] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2024', tol=0.54)
# z[:, 16] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2025', tol=0.54)
# z[:, 17] = solve_lp_for_year(puf, Stage_I_factors, Stage_II_targets,
#                              year='2026', tol=0.54)
#
# # Write all weights (rounded to nearest integer) to puf_weights.csv file
# z = pd.DataFrame(z,
#                  columns=['WT2009', 'WT2010', 'WT2011', 'WT2012', 'WT2013',
#                           'WT2014', 'WT2015', 'WT2016', 'WT2017', 'WT2018',
#                           'WT2019', 'WT2020', 'WT2021', 'WT2022', 'WT2023',
#                           'WT2024', 'WT2025', 'WT2026'])
# z = z.round(0).astype('int64')
# z.to_csv('puf_weights.csv', index=False)
