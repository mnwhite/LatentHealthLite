'''
Load parameters for estimating the model for all respondents over 23 from the
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
sex_list = [0,1]    # Only women in this dataset
T_max = 21        # Maximum number of periods for each individual
id_col = None
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
    2.700565609799692,  # 0 Mort0
    -0.274992160152529,  # 1 MortSex
    1.0920111742249294,  # 2 MortHealth1
    -0.40110122273727256,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -1.8019430572911714,  # 6 MortAge1
    2.4831787358610926,  # 7 MortAge2
    -26.795323620325913,  # 8 MortAge3
    0.0,  # 9 MortAge4
    0.3656742977510194,  # 10 MortHealthAge
    1.0235273915569636,  # 11 MortSexAge
    3.0267124281838047,  # 12 Corr0
    9.116424177998589,  # 13 CorrAge1
    -56.66332232995522,  # 14 CorrAge2
    149.15811424830918,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    11.173009335199781,  # 17 Health0
    0.8741344466967371,  # 18 HealthSex
    -8.269996777906195,  # 19 HealthAge1
    5.289450384794128,  # 20 HealthAge2
    -1.7306539902752565,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    -45.40857137190111,  # 23 HealthAgeSex
    10.580913574250525,  # 24 xInitMean
    3.7472467285178648,  # 25 xInitStd
    0.4372414837539217,  # 26 SRHS_Coeff
    1.6791265763158918,  # 27 SRHS_Cut2
    1.837487407777273,  # 28 SRHS_Cut3
    2.0501720630627314,  # 29 SRHS_Cut4
]) 

# 424485.75390019006

#which_indices = np.array([0, 6, 17, 19])
which_indices = np.array([0,1,2,3,6,7,8,10,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,28,29])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14,15,17,19,20,21,24,25])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([0,2,3,10])
