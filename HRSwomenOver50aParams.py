'''
Load parameters for estimating the model only on women over 50 from the HRS,
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
data_file = '../Data/Estimation/HRSallAnnual.txt'
source_name = 'HRS' # Name of dataset
figure_label = 'HRSover50a' # Text string to use as prefix for figure filenames
sex_list = [0]    # Only women in this dataset
T_max = 21        # Maximum number of periods for each individual
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
report_type_count = 1       # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = False # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.394225902149764,  # 0 Mort0
    0.0,  # 1 MortSex
    1.06013221144,  # 2 MortHealth1
    0.695067330182,  # 3 MortHealth2
    -1.919403104689748,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -5.762486778750872,  # 6 MortAge1
    27.454493420081484,  # 7 MortAge2
    -148.11547371122586,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -1.56997547334,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.7061044378288868,  # 12 Corr0
    -0.768157761961,  # 13 CorrAge1
    0.0,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    1.8419913498439093,  # 17 Health0
    0.0,  # 18 HealthSex
    4.3787539444933286,  # 19 HealthAge1
    -6.733661704421864,  # 20 HealthAge2
    2.8960975893,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    8.369147577762424,  # 24 xInitMean
    4.816250263875338,  # 25 xInitStd
    0.44114138284423676,  # 26 SRHS_Coeff
    1.7362551636882846,  # 27 SRHS_Cut2
    1.8004902892375367,  # 28 SRHS_Cut3
    2.1646706523634394,  # 29 SRHS_Cut4
]) 

which_indices = np.array([0,2,3,4,6,7,8,10,12,13,17,19,20,21,24,25,26,27,28,29]) 
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([12,13])
#which_indices = np.array([17,19,20,21])

# 131815.49998722546