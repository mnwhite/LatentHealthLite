'''
Load parameters for estimating the model only on women over 23 from the PSID,
treating each period as a year.
'''
import numpy as np
import os
file_name = os.path.basename(__file__)
dot_i = file_name.find('.')
param_file_name = file_name[:dot_i]
eval_count = 0

# Specify parameters for the continuous state grid
x_min = -12.
x_max = 28.
x_count = 200

# Define parameters for loading in the data file
data_file = '../Data/Estimation/PSIDallAnnual.txt'
source_name = 'PSID' # Name of dataset
figure_label = 'PSIDover23a' # Text string to use as prefix for figure filenames
sex_list = [0]    # Only women in this dataset
T_max = 21        # Maximum number of periods for each individual
weight_col = 1    # Column of the data with observation weight
age_col = 3       # Column of the data with age
sex_col = 2       # Column of the data with male dummy
data_init_col = 4 # Column where data starts
measure_count = 1 # Number of measures in data per period
category_counts = [5]  # Number of categorical responses for each measure (list)
measure_names = ['SRHS'] # Abbreviation for each measure in data (list)
age_min = 23.0    # Minimum age in the data
age_max = 110.0   # Maximum age in the data
age_incr = 1.0    # Age increment in years
wave_length = 2   # Number of periods between actual data collection waves
report_type_count = 1 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = False # Whether health shocks are a mixed normal


# Define a test parameter vector
current_param_vec = np.array([ 
    2.6223204167367924,  # 0 Mort0
    0.0,  # 1 MortSex
    1.3801773145861496,  # 2 MortHealth1
    -0.2408126065548719,  # 3 MortHealth2
    -0.832343250628,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -3.1185886337481064,  # 6 MortAge1
    13.581905116247926,  # 7 MortAge2
    -57.05332679303661,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -2.58717724721413,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.1369553062412336,  # 12 Corr0
    5.2899592596828935,  # 13 CorrAge1
    -20.695219222943294,  # 14 CorrAge2
    38.38761174280421,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    10.543280833643749,  # 17 Health0
    0.0,  # 18 HealthSex
    -6.22471910211039,  # 19 HealthAge1
    3.7037843891363087,  # 20 HealthAge2
    -1.4188846312899768,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    10.515129564141967,  # 24 xInitMean
    3.7507482692472176,  # 25 xInitStd
    0.43753491819662543,  # 26 SRHS_Coeff
    1.6669923458228084,  # 27 SRHS_Cut2
    1.9628698307864938,  # 28 SRHS_Cut3
    2.05434866263751,  # 29 SRHS_Cut4
]) 

which_indices = np.array([0,2,3,4,6,7,8,10,12,13,14,15,17,19,20,21,24,25,26,27,28,29]) 
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([12,13,14,15,17,19,20,21,24,25])
#which_indices = np.array([17,19,20,21])

# 87903.26903145891