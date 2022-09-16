'''
Load parameters for estimating the model only on women over 50 from the HRS,
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
data_file = '../Data/Estimation/HRSallAnnual.txt'
source_name = 'HRS' # Name of dataset
figure_label = 'HRSover50a' # Text string to use as prefix for figure filenames
sex_list = [0]    # Only women in this dataset
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
    2.4674919811053693,  # 0 Mort0
    0.0,  # 1 MortSex
    1.2458452677701333,  # 2 MortHealth1
    -0.6396765420809506,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -5.782493923526624,  # 6 MortAge1
    26.980478942336376,  # 7 MortAge2
    -148.11160609728725,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -0.30269815659662674,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.6688164441335402,  # 12 Corr0
    0.5421521313103378,  # 13 CorrAge1
    0.0,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    1.2475271845956661,  # 17 Health0
    0.0,  # 18 HealthSex
    3.8952800005290937,  # 19 HealthAge1
    -7.184791276666107,  # 20 HealthAge2
    3.146440766604456,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    7.8590026441415155,  # 24 xInitMean
    4.340872291443153,  # 25 xInitStd
    -2.0125316562568116,  # 26 HealthShockAvg1
    1.3056241529311874,  # 27 HealthShockLogStd1
    -3.087737449335291,  # 28 HealthShockLogit1
    -0.7230805397819725,  # 29 SRHSlogStd1
    0.668168207601892,  # 30 SRHSlogStd2
    -0.09826627988312629,  # 31 TypeLogit1
    -1.592265016249335,  # 32 TypeLogit2
    0.4633630900579935,  # 33 SRHS_Coeff
    1.7801133454301064,  # 34 SRHS_Cut2
    1.7079714784786577,  # 35 SRHS_Cut3
    2.0227250789887177,  # 36 SRHS_Cut4
]) 

which_indices = np.array([0,2,3,6,7,8,10,12,13,17,19,20,21,24,25,26,27,28,29,30,31,32,33,34,35,36]) 
#which_indices = np.array([26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([0,2,3])
#which_indices = np.array([17,19,20,21])

# 129289.63774378663