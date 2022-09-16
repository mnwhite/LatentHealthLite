'''
Load parameters for estimating the model only on men over 23 from the PSID,
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
report_type_count = 1       # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = False # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.2787511920321397,  # 0 Mort0
    0.0,  # 1 MortSex
    0.9831061318212201,  # 2 MortHealth1
    0.3948663724222225,  # 3 MortHealth2
    -1.2668516158434615,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -0.9985627069946273,  # 6 MortAge1
    -0.8041746986043732,  # 7 MortAge2
    -16.843008992918165,  # 8 MortAge3
    0.0,  # 9 MortAge4
    0.4063633370420743,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    2.985004840733646,  # 12 Corr0
    7.264345975739456,  # 13 CorrAge1
    -20.265968482191937,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    10.831823189486855,  # 17 Health0
    0.0,  # 18 HealthSex
    -4.862231141219824,  # 19 HealthAge1
    0.5387069070375368,  # 20 HealthAge2
    0.0,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    11.468313869578136,  # 24 xInitMean
    3.9820515236956098,  # 25 xInitStd
    0.411374744656956,  # 26 SRHS_Coeff
    1.5970395985730181,  # 27 SRHS_Cut2
    1.862673973695908,  # 28 SRHS_Cut3
    1.9233182130479913,  # 29 SRHS_Cut4
]) 

which_indices = np.array([0,2,3,4,6,7,8,10,12,13,14,17,19,20,24,25,26,27,28,29]) 
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([12,13,14])
#which_indices = np.array([17,19,20])
#which_indices = np.array([10])

# 74772.80931019617