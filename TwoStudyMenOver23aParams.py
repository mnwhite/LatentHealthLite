'''
Load parameters for estimating the model for men over 23 from the
PSID and HRS treating each period as a year.  This version is the basic one.
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
data_file = '../Data/Estimation/TwoStudyData.txt'
source_name = 'HRS & PSID' # Name of dataset
figure_label = 'TwoStudyOver23basic' # Text string to use as prefix for figure filenames
sex_list = [1]    # Only men in this dataset
T_max = 21        # Maximum number of periods for each individual
weight_col = 2    # Column of the data with observation weight
age_col = 4       # Column of the data with age
sex_col = 3       # Column of the data with male dummy
data_init_col = 5 # Column where data starts
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
    2.362956942051433,  # 0 Mort0
    0.0,  # 1 MortSex
    1.1556912895099036,  # 2 MortHealth1
    -0.4107572141605589,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -1.1181891575510765,  # 6 MortAge1
    -0.37904659211179603,  # 7 MortAge2
    -20.00274518184808,  # 8 MortAge3
    0.0,  # 9 MortAge4
    0.05019985129766705,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.149491665599231,  # 12 Corr0
    6.677395644496982,  # 13 CorrAge1
    -40.77968851218394,  # 14 CorrAge2
    109.40278624627555,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    12.099966842779342,  # 17 Health0
    0.0,  # 18 HealthSex
    -9.193348796064347,  # 19 HealthAge1
    5.80667208365459,  # 20 HealthAge2
    -1.9416708954778488,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    10.733519142509827,  # 24 xInitMean
    3.6483853254873857,  # 25 xInitStd
    0.43165618292812424,  # 26 SRHS_Coeff
    1.6271559527596393,  # 27 SRHS_Cut2
    1.7958672118939096,  # 28 SRHS_Cut3
    1.9664344332227452,  # 29 SRHS_Cut4
]) 

# 194931.8340577961

#which_indices = np.array([0, 6, 17, 19])
which_indices = np.array([0,2,3,6,7,8,10,12,13,14,15,17,19,20,21,24,25,26,27,28,29])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14,15,17,19,20,21,24,25])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([0,2,3,10])
