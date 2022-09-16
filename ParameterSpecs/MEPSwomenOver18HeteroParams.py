'''
Load parameters for estimating the model only on women in the MEPS.  This version
has three types of agents, with different magnitudes of SRHS reporting errors.
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
data_file = '../Data/Estimation/MEPSall.txt'
source_name = 'MEPS' # Name of dataset
figure_label = 'MEPSover18' # Text string to use as prefix for figure filenames
sex_list = [0]    # Only women in this dataset
T_max = 5         # Maximum number of periods for each individual
id_col = None     # Column with individual's id number (can be None)
weight_col = 2    # Column of the data with observation weight
age_col = 4       # Column of the data with age
sex_col = 3       # Column of the data with male dummy
data_init_col = 5 # Column where data starts
measure_count = 1 # Number of measures in data per period
category_counts = [5]  # Number of categorical responses for each measure (list)
measure_names = ['SRHS'] # Abbreviation for each measure in data (list)
age_min = 18.0    # Minimum age in the data
age_max = 87.0    # Maximum age in the data
age_incr = 0.5    # Age increment in years
wave_length = 1   # Number of periods between actual data collection waves
report_type_count = 3 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.675910663776278,  # 0 Mort0
    0.0,  # 1 MortSex
    1.3902967960811763,  # 2 MortHealth1
    0.47968541875395937,  # 3 MortHealth2
    -2.5320582781925136,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    0.6009493016347142,  # 6 MortAge1
    -8.049959315829144,  # 7 MortAge2
    3.178041970344111,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -1.4031594663997207,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    2.5091427782057147,  # 12 Corr0
    4.101069684933245,  # 13 CorrAge1
    -12.348529319644289,  # 14 CorrAge2
    16.667801341673147,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    7.972024109339117,  # 17 Health0
    0.0,  # 18 HealthSex
    1.2725901068383685,  # 19 HealthAge1
    -2.5360534457238906,  # 20 HealthAge2
    1.917695628482739,  # 21 HealthAge3
    -0.6465607938774168,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    9.785606311039427,  # 24 xInitMean
    2.9628681293131347,  # 25 xInitStd
    -0.8381292608560927,  # 26 HealthShockAvg1
    1.229048880086321,  # 27 LogHealthShockStd1
    -2.6243453983422627,  # 28 HealthShockLogit1
    -0.7633106502284089,  # 29 SRHSlogStd1
    0.1576972664380728,  # 30 SRHSlogStd2
    1.9875920302366241,  # 31 TypeLogit1
    2.0603419805770535,  # 32 TypeLogit2
    0.4824700526598625,  # 33 SRHS_Coeff
    1.753316616900775,  # 34 SRHS_Cut2
    1.7680203954094869,  # 35 SRHS_Cut3
    1.5391026238470493,  # 36 SRHS_Cut4
])

# 685410.8571942361

which_indices = np.array([0,2,3,4,6,7,8,10,12,13,14,15,17,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([12,13,14,15,16])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([17,19,20,21,22])
#which_indices = np.array([27,28,29])

