'''
Load parameters for estimating the model only on women over 23 from the PSID,
treating each period as a year.  This version has three reporting types.
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
x_count = 360

# Define parameters for loading in the data file
data_file = '../Data/Estimation/PSIDallBiannual.txt'
source_name = 'PSID' # Name of dataset
figure_label = 'PSIDover23a' # Text string to use as prefix for figure filenames
sex_list = [0]    # Only women in this dataset
T_max = 11        # Maximum number of periods for each individual
id_col = None     # Column with individual's id number (can be None)
weight_col = 1    # Column of the data with observation weight
age_col = 3       # Column of the data with age
sex_col = 2       # Column of the data with male dummy
data_init_col = 4 # Column where data starts
measure_count = 1 # Number of measures in data per period
category_counts = [5]  # Number of categorical responses for each measure (list)
measure_names = ['SRHS'] # Abbreviation for each measure in data (list)
age_min = 23.0    # Minimum age in the data
age_max = 109.0   # Maximum age in the data
age_incr = 2.0    # Age increment in years
wave_length = 1   # Number of periods between actual data collection waves
report_type_count = 3 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.1323628743403407,  # 0 Mort0
    0.0,  # 1 MortSex
    1.7423127083480596,  # 2 MortHealth1
    -0.9565577629256713,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    1.564629688900291,  # 6 MortAge1
    -10.6726378350947,  # 7 MortAge2
    0.0,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -5.843928661608701,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.468664666256467,  # 12 Corr0
    2.485019851130606,  # 13 CorrAge1
    0.0,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    11.142284625418318,  # 17 Health0
    0.0,  # 18 HealthSex
    -8.854995212976462,  # 19 HealthAge1
    6.731671986221899,  # 20 HealthAge2
    -3.188722174029679,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    10.80104592100898,  # 24 xInitMean
    3.55526201425079,  # 25 xInitStd
    -1.109139093011744,  # 26 HealthShockAvg1
    1.2525918556986064,  # 27 HealthShockLogStd1
    -2.7639328759898145,  # 28 HealthShockLogit1
    -0.7004161743396078,  # 29 SRHSlogStd1
    0.0717406555030173,  # 30 SRHSlogStd2
    1.5420074040623648,  # 31 TypeLogit1
    1.5055727740743179,  # 32 TypeLogit2
    0.4126699307391219,  # 33 SRHS_Coeff
    1.7143077616529965,  # 34 SRHS_Cut2
    1.8803977341728344,  # 35 SRHS_Cut3
    1.850248498857331,  # 36 SRHS_Cut4
]) 

# 85919.41616862916

which_indices = np.array([0,2,3,6,7,10,12,13,17,19,20,21,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14,15,17,19,20,21,24,25])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([12,13])
