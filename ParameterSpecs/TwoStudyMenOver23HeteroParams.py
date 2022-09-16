'''
Load parameters for estimating the model for men over 23 from the
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
sex_list = [1]    # Only women in this dataset
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
report_type_count = 3 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.222353481026447,  # 0 Mort0
    0.0,  # 1 MortSex
    1.3853088537328007,  # 2 MortHealth1
    -0.5138267901575959,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -0.4036097724668611,  # 6 MortAge1
    -2.525467508152688,  # 7 MortAge2
    -16.885602960682125,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -2.5719659097024388,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.10977123134165,  # 12 Corr0
    6.894261416340662,  # 13 CorrAge1
    -36.85735592639089,  # 14 CorrAge2
    103.0613546270991,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    12.04947025888963,  # 17 Health0
    0.0,  # 18 HealthSex
    -9.956109962330514,  # 19 HealthAge1
    6.458341680774027,  # 20 HealthAge2
    -2.356323488458161,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    10.551932333397469,  # 24 xInitMean
    3.3178166628254666,  # 25 xInitStd
    -1.754018505243344,  # 26 HealthShockAvg1
    1.2407635147427818,  # 27 HealthShockLogStd1
    -2.8677014197361355,  # 28 HealthShockLogit1
    -0.6993445765557016,  # 29 SRHSlogStd1
    0.07286939542485951,  # 30 SRHSlogStd2
    1.7469499370926693,  # 31 TypeLogit1
    1.7172529364939026,  # 32 TypeLogit2
    0.4302164616785432,  # 33 SRHS_Coeff
    1.7386651899458891,  # 34 SRHS_Cut2
    1.7073678721408538,  # 35 SRHS_Cut3
    1.7569306005658085,  # 36 SRHS_Cut4
]) 

# 191074.42936344806
# 190727.30153673925
# 190676.83791829826

#which_indices = np.array([0, 6, 17, 19])
which_indices = np.array([0,2,3,6,7,8,10,12,13,14,15,17,19,20,21,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14,15,17,19,20,21,24,25])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([0,2,3,10])
