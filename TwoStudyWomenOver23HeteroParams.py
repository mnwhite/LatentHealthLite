'''
Load parameters for estimating the model for women over 23 from the
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
sex_list = [0]    # Only women in this dataset
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
    2.631957620094815,  # 0 Mort0
    0.0,  # 1 MortSex
    1.3572422164786768,  # 2 MortHealth1
    -0.6774722765435125,  # 3 MortHealth2
    0.0,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -1.4963180692065672,  # 6 MortAge1
    2.2546698209201255,  # 7 MortAge2
    -28.152516609089528,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -2.144695228214326,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.216310042427278,  # 12 Corr0
    8.676480603284096,  # 13 CorrAge1
    -54.479509006819804,  # 14 CorrAge2
    152.8713130272321,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    10.667586345921686,  # 17 Health0
    0.0,  # 18 HealthSex
    -8.460189183115169,  # 19 HealthAge1
    5.502462231551342,  # 20 HealthAge2
    -1.928626154568222,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    10.376754096926852,  # 24 xInitMean
    3.4934410024471187,  # 25 xInitStd
    -1.5413485890941565,  # 26 HealthShockAvg1
    1.2789954989330734,  # 27 HealthShockLogStd1
    -2.92813894315975,  # 28 HealthShockLogit1
    -0.733424993090625,  # 29 SRHSlogStd1
    0.04525935913958488,  # 30 SRHSlogStd2
    1.3946005998502056,  # 31 TypeLogit1
    1.5051000710951057,  # 32 TypeLogit2
    0.43632343069658236,  # 33 SRHS_Coeff
    1.7857261436923026,  # 34 SRHS_Cut2
    1.7915265282539112,  # 35 SRHS_Cut3
    1.9375131385778694,  # 36 SRHS_Cut4
]) 

# 224662.3143387179
# 224614.66634162626
# 224614.65537413274

which_indices = np.array([0,2,3,6,7,8,10,12,13,14,15,17,19,20,21,24,25,26,27,28,29,30,31,32,33,34,35,36])
#which_indices = np.array([26,27,28])
#which_indices = np.array([12,13,14,15,17,19,20,21,24,25])
#which_indices = np.array([0,2,3,6,7,8,10])
