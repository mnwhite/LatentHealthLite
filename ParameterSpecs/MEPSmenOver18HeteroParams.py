'''
Load parameters for estimating the model on men in the MEPS.  This version
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
sex_list = [1]    # Only men in this dataset
T_max = 5         # Maximum number of periods for each individual
id_col = None     # Column with individual's id number (can be None)
weight_col = 2    # Column of the data with observation weight
age_col = 4       # Column of the data with age
sex_col = 3       # Column of the data with male dummy
data_init_col = 5 # Column where data starts
measure_count = 1 # Number of measures in data per period
category_counts = [5] # Number of categorical responses for each measure (list)
measure_names = ['SRHS'] # Abbreviation for each measure in data (list)
age_min = 18.0    # Minimum age in the data
age_max = 87.0    # Maximum age in the data
age_incr = 0.5    # Age increment in years
wave_length = 1   # Number of periods between actual data collection waves
report_type_count = 3       # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True  # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.429054009623022,  # 0 Mort0
    0.0,  # 1 MortSex
    0.9810844102507245,  # 2 MortHealth1
    1.098471956702974,  # 3 MortHealth2
    -3.380038391587822,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    1.454833595692872,  # 6 MortAge1
    -13.416179809001013,  # 7 MortAge2
    17.103340895274712,  # 8 MortAge3
    0.0,  # 9 MortAge4
    3.328827184487464,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    2.5072432411828274,  # 12 Corr0
    1.7240325971788277,  # 13 CorrAge1
    6.122031047450734,  # 14 CorrAge2
    -34.83264036802574,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    8.101739461044978,  # 17 Health0
    0.0,  # 18 HealthSex
    1.256036937983589,  # 19 HealthAge1
    -2.5650743365614166,  # 20 HealthAge2
    1.9063591123898738,  # 21 HealthAge3
    -0.6462166869534741,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    10.02654463004765,  # 24 xInitMean
    2.661054303567986,  # 25 xInitStd
    -0.7833613238801251,  # 26 HealthShockAvg1
    1.2502581663562775,  # 27 HealthShockLogStd1
    -2.7327704321289312,  # 28 HealthShockLogit1
    -0.7943788010229635,  # 29 SRHSlogStd1
    0.14746665836630668,  # 30 SRHSlogStd2
    1.9873004958510958,  # 31 TypeLogit1
    2.1369980397663504,  # 32 TypeLogit2
    0.4969885233416651,  # 33 SRHS_Coeff
    1.7257709087550037,  # 34 SRHS_Cut2
    1.7821888614228358,  # 35 SRHS_Cut3
    1.4553619044906763,  # 36 SRHS_Cut4
])

# 586962.0690172506

which_indices = np.array([0,2,3,4,6,7,8,10,12,13,14,15,17,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([12,13,14,15])
#which_indices = np.array([29,30,31,32])

