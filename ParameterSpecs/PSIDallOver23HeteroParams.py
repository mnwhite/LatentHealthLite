'''
Load parameters for estimating the model for all respondents  over 23 from the PSID,
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
data_file = '../Data/Estimation/PSIDallAnnual.txt'
source_name = 'PSID' # Name of dataset
figure_label = 'PSIDover23a' # Text string to use as prefix for figure filenames
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
age_min = 23.0    # Minimum age in the data
age_max = 110.0   # Maximum age in the data
age_incr = 1.0    # Age increment in years
wave_length = 2   # Number of periods between actual data collection waves
report_type_count = 3 # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.2864640678149306,  # 0 Mort0
    -0.2634556263405404,  # 1 MortSex
    1.3736957188480239,  # 2 MortHealth1
    -0.6079357191866499,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    0.8283587314256753,  # 6 MortAge1
    -9.140589824807769,  # 7 MortAge2
    0.0,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -2.909546269546994,  # 10 MortHealthAge
    1.1277519238425333,  # 11 MortSexAge
    3.189425034692818,  # 12 Corr0
    4.8609242596959685,  # 13 CorrAge1
    -6.647259922362009,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    11.128279591015875,  # 17 Health0
    2.406545801945312,  # 18 HealthSex
    -8.685254406849674,  # 19 HealthAge1
    5.986902332925849,  # 20 HealthAge2
    -2.824686506614564,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    -115.29256770772459,  # 23 HealthAgeSex
    11.192728871821842,  # 24 xInitMean
    3.6387774275158695,  # 25 xInitStd
    -1.2042253636529796,  # 26 HealthShockAvg1
    1.2077200511099844,  # 27 HealthShockLogStd1
    -2.652355769933867,  # 28 HealthShockLogit1
    -0.7001766235507946,  # 29 SRHSlogStd1
    0.05051729018413197,  # 30 SRHSlogStd2
    1.5437041428790972,  # 31 TypeLogit1
    1.5387021079550498,  # 32 TypeLogit2
    0.40322875308623496,  # 33 SRHS_Coeff
    1.7223102240723314,  # 34 SRHS_Cut2
    1.8390861328705725,  # 35 SRHS_Cut3
    1.7749749398651151,  # 36 SRHS_Cut4
]) 

# 158974.5920248535

which_indices = np.array([0,1,2,3,6,7,10,11,12,13,14,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14])
#which_indices = np.array([0,1,2,3,6,7,10,11])
#which_indices = np.array([1,11,18,23])
