'''
Load parameters for estimating the model only on men over 23 from the PSID,
treating each period as a year. This version has three reporting types and no
mixed normal health shocks
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
data_file = '../Data/Estimation/PSIDallAnnual.txt'
source_name = 'PSID' # Name of dataset
figure_label = 'PSIDover23a' # Text string to use as prefix for figure filenames
sex_list = [1]    # Only men in this dataset
T_max = 21        # Maximum number of periods for each individual
id_col = None     # Column with individual's id number (can be None)
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
report_type_count = 3       # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True  # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.1653360640040984,  # 0 Mort0
    0.0,  # 1 MortSex
    1.032951587064545,  # 2 MortHealth1
    -0.22109951647258144,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    0.3372040276331505,  # 6 MortAge1
    -7.7948598050561335,  # 7 MortAge2
    0.0,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -0.7707906625236223,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    2.8356691042656084,  # 12 Corr0
    9.363420528240098,  # 13 CorrAge1
    -23.06316045224926,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    12.43830649802209,  # 17 Health0
    0.0,  # 18 HealthSex
    -6.88134833651342,  # 19 HealthAge1
    0.5801784016551443,  # 20 HealthAge2
    0.0,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    11.817439578971456,  # 24 xInitMean
    3.790878164053378,  # 25 xInitStd
    -1.301632610363486,  # 26 HealthShockAvg1
    1.170264878544392,  # 27 HealthShockLogStd1
    -2.550774424448673,  # 28 HealthShockLogit1
    -0.7054369113300959,  # 29 SRHSlogStd1
    0.7178615959169333,  # 30 SRHSlogStd2
    -0.05793538219982665,  # 31 TypeLogit1
    -1.555093324287757,  # 32 TypeLogit2
    0.3888625359662222,  # 33 SRHS_Coeff
    1.7284657314557608,  # 34 SRHS_Cut2
    1.7878146257273695,  # 35 SRHS_Cut3
    1.6969084659195737,  # 36 SRHS_Cut4
]) 

which_indices = np.array([0,2,3,6,7,10,12,13,14,17,19,20,24,25,26,27,28,29,30,31,32,33,34,35,36]) 
#which_indices = np.array([0,2,3,6,7,10])

# 73083.96757416766
