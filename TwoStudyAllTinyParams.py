'''
Load parameters for estimating the model for all respondents  over 23 from the
PSID and HRS treating each period as a year.  This version has three reporting types
and mixed normal health shocks.
'''
import numpy as np
import os
file_name = os.path.basename(__file__)
dot_i = file_name.find('.')
param_file_name = file_name[:dot_i]
eval_count = 0

# Specify parameters for the continuous state grid
x_min = -6.
x_max = 22.
x_count = 45

# Define parameters for loading in the data file
data_file = '../Data/Estimation/TwoStudyData.txt'
source_name = 'HRS & PSID' # Name of dataset
figure_label = 'TwoStudyTiny' # Text string to use as prefix for figure filenames
sex_list = [0,1]  # Both men and women in this dataset
T_max = 21        # Maximum number of periods for each individual
id_col = 1        # Column with individual's id number (can be None)
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
report_type_count = 3 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector CURRENT ESTIMATES
current_param_vec = np.array([ 
    2.5930505520898004,  # 0 Mort0
    -0.2660934764960399,  # 1 MortSex
    1.3526851669512048,  # 2 MortHealth1
    -0.6426450119837875,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -1.3538602219100189,  # 6 MortAge1
    1.1297389157510818,  # 7 MortAge2
    -24.613504649819593,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -1.538985186886927,  # 10 MortHealthAge
    0.8960549690349597,  # 11 MortSexAge
    2.5890715832565925,  # 12 Corr0
    6.055617728239338,  # 13 CorrAge1
    -33.63329588560898,  # 14 CorrAge2
    98.83174232796671,  # 15 CorrAge3
    -1.0,  # 16 CorrAge4
    12.408500501118885,  # 17 Health0
    0.9671008351929726,  # 18 HealthSex
    -8.597787993985275,  # 19 HealthAge1
    6.063837692573281,  # 20 HealthAge2
    -2.303892323144151,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    -52.029441259393444,  # 23 HealthAgeSex
    10.600304651666479,  # 24 xInitMean
    3.502456384954448,  # 25 xInitStd
    -1.3177638567835626,  # 26 HealthShockAvg1
    1.2537922491359499,  # 27 HealthShockLogStd1
    -2.8016486726034637,  # 28 HealthShockLogit1
    -0.6270615502484442,  # 29 SRHSlogStd1
    0.11558945058661968,  # 30 SRHSlogStd2
    1.9255418272025906,  # 31 TypeLogit1
    1.7422589381103195,  # 32 TypeLogit2
    0.4245894191822325,  # 33 SRHS_Coeff
    1.7582915012922873,  # 34 SRHS_Cut2
    1.7475346476709168,  # 35 SRHS_Cut3
    1.8527063749999324,  # 36 SRHS_Cut4
]) 
# 415212.02851145534

which_indices = np.array([0,1,2,3,6,7,8,10,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14,15,16,17,18,19,20,21,22])
#which_indices = np.array([0,1,2,3,6,7,8,10,11])
# = np.array([20,21,22])
