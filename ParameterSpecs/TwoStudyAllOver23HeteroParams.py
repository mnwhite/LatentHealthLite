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
x_min = -12.
x_max = 28.
x_count = 360

# Define parameters for loading in the data file
data_file = '../Data/Estimation/TwoStudyData.txt'
source_name = 'HRS & PSID' # Name of dataset
figure_label = 'TwoStudyOver23' # Text string to use as prefix for figure filenames
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
    2.5651782391797147,  # 0 Mort0
    -0.2726891004179305,  # 1 MortSex
    1.3673835765781392,  # 2 MortHealth1
    -0.5991236082491905,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -1.089810166831798,  # 6 MortAge1
    0.3197538738268369,  # 7 MortAge2
    -23.636621450522757,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -2.305210977585802,  # 10 MortHealthAge
    0.9687236800562369,  # 11 MortSexAge
    3.1191057947425778,  # 12 Corr0
    8.251632788179046,  # 13 CorrAge1
    -48.473020527748766,  # 14 CorrAge2
    135.22264449780184,  # 15 CorrAge3
    -1.0,  # 16 CorrAge4
    11.060541336040018,  # 17 Health0
    0.9280069314630262,  # 18 HealthSex
    -9.125663409910988,  # 19 HealthAge1
    6.0513357052868875,  # 20 HealthAge2
    -2.1458981801733388,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    -49.225651394775625,  # 23 HealthAgeSex
    10.460006292367668,  # 24 xInitMean
    3.4458025039897815,  # 25 xInitStd
    -1.6374367385251107,  # 26 HealthShockAvg1
    1.2575362801537133,  # 27 HealthShockLogStd1
    -2.887532241669435,  # 28 HealthShockLogit1
    -0.711398750756505,  # 29 SRHSlogStd1
    0.06599718760961476,  # 30 SRHSlogStd2
    1.6201648044929482,  # 31 TypeLogit1
    1.649252643445411,  # 32 TypeLogit2
    0.4334927344845934,  # 33 SRHS_Coeff
    1.7644379961708607,  # 34 SRHS_Cut2
    1.7519425099103467,  # 35 SRHS_Cut3
    1.8495937948947738,  # 36 SRHS_Cut4
]) 
# 415389.6102823704

#which_indices = np.array([0,1,2,3,6,7,8,10,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([26,27,28])
which_indices = np.array([12,13,14,15,16,17,18,19,20,21,22])
#which_indices = np.array([0,1,2,3,6,7,8,10,11])
# = np.array([20,21,22])
