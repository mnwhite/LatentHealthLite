'''
Load parameters for estimating the model on all respondents over 50 from the HRS,
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
x_max = 20.
x_count = 360

# Define parameters for loading in the data file
data_file = '../Data/Estimation/HRSallAnnual.txt'
source_name = 'HRS' # Name of dataset
figure_label = 'HRSover50a' # Text string to use as prefix for figure filenames
sex_list = [0,1]  # Both men and women
T_max = 21        # Maximum number of periods for each individual
id_col = None     # Column with individual's id number (can be None)
weight_col = 1    # Column of the data with observation weight
age_col = 3       # Column of the data with age
sex_col = 2       # Column of the data with male dummy
data_init_col = 4 # Column where data starts
measure_count = 1 # Number of measures in data per period
category_counts = [5]  # Number of categorical responses for each measure (list)
measure_names = ['SRHS'] # Abbreviation for each measure in data (list)
age_min = 50.0    # Minimum age in the data
age_max = 115.0   # Maximum age in the data
age_incr = 1.0    # Age increment in years
wave_length = 2   # Number of periods between actual data collection waves
report_type_count = 3 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.40533561782935,  # 0 Mort0
    -0.22240079691556613,  # 1 MortSex
    1.5594119356773835,  # 2 MortHealth1
    -0.7356349814094966,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -5.184263261390221,  # 6 MortAge1
    22.995676940244223,  # 7 MortAge2
    -134.86122595905053,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -3.1573975548703888,  # 10 MortHealthAge
    0.2630264101375445,  # 11 MortSexAge
    3.541133340817153,  # 12 Corr0
    1.4827731781353262,  # 13 CorrAge1
    0.0,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    1.8862370187662894,  # 17 Health0
    -0.42789266938917625,  # 18 HealthSex
    2.28793310326417,  # 19 HealthAge1
    -5.437703333437414,  # 20 HealthAge2
    1.990858875285235,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    -18.211857330830593,  # 23 HealthAgeSex
    7.5973111889273985,  # 24 xInitMean
    4.082891259642308,  # 25 xInitStd
    -2.204294279107545,  # 26 HealthShockAvg1
    1.3246333656536864,  # 27 HealthShockLogStd1
    -3.154610989468442,  # 28 HealthShockLogit1
    -0.6945578422472425,  # 29 SRHSlogStd1
    0.741279718236912,  # 30 SRHSlogStd2
    0.031818293264314394,  # 31 TypeLogit1
    -1.8138142366053192,  # 32 TypeLogit2
    0.47249156156532757,  # 33 SRHS_Coeff
    1.7565804797847984,  # 34 SRHS_Cut2
    1.6738220293673702,  # 35 SRHS_Cut3
    1.9317292492387907,  # 36 SRHS_Cut4
]) 

which_indices = np.array([0,1,2,3,6,7,8,10,11,12,13,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36]) 
#which_indices = np.array([26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([1,11,18,23])
#which_indices = np.array([0,1,2,3,4])

# 229665.37705951568