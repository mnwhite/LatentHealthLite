'''
Load parameters for estimating the model only all respondents in the MEPS.  This version
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
sex_list = [0,1]    # Only women in this dataset
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
    2.657774603258625,  # 0 Mort0
    -0.27215901820296456,  # 1 MortSex
    1.1919757456715,  # 2 MortHealth1
    0.7723731895193932,  # 3 MortHealth2
    -2.9700235187234156,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    1.0066677275282037,  # 6 MortAge1
    -10.659881782400838,  # 7 MortAge2
    9.43167762869863,  # 8 MortAge3
    0.0,  # 9 MortAge4
    1.0351721532044782,  # 10 MortHealthAge
    1.4456391654581344,  # 11 MortSexAge
    2.4804843108917165,  # 12 Corr0
    3.1732036754145305,  # 13 CorrAge1
    -4.789714037137521,  # 14 CorrAge2
    -4.7372579376709165,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    7.6383671148686885,  # 17 Health0
    0.7131709019169005,  # 18 HealthSex
    1.3432414808686675,  # 19 HealthAge1
    -2.5226592875169924,  # 20 HealthAge2
    1.8959566837141129,  # 21 HealthAge3
    -0.6407083622402707,  # 22 HealthAge4
    -21.462963430341574,  # 23 HealthAgeSex
    9.850258935377294,  # 24 xInitMean
    2.818862680737917,  # 25 xInitStd
    -0.8048205017708492,  # 26 HealthShockAvg1
    1.2282152974521763,  # 27 HealthShockLogStd1
    -2.6589991817464838,  # 28 HealthShockLogit1
    -0.7791471527048717,  # 29 SRHSlogStd1
    0.15250878402199147,  # 30 SRHSlogStd2
    1.9818256350127423,  # 31 TypeLogit1
    2.090760955724485,  # 32 TypeLogit2
    0.4939661098714674,  # 33 SRHS_Coeff
    1.7419890319859892,  # 34 SRHS_Cut2
    1.7755568284287309,  # 35 SRHS_Cut3
    1.498554984334729,  # 36 SRHS_Cut4
]) 

# 1369948.4309536682

which_indices = np.array([0,1,2,3,4,6,7,8,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([12,13,14,15,16])
#which_indices = np.array([0,2,3,4,6,7,8,10])
#which_indices = np.array([17,19,20,21,22])
#which_indices = np.array([1,11,18,23])
