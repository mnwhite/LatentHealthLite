'''
Load parameters for estimating the model only on men over 50 from the HRS,
treating each period as a year. This version has three reporting types and a
mixed normal health shock distribution.
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
data_file = '../Data/Estimation/HRSallAnnual.txt'
source_name = 'HRS' # Name of dataset
figure_label = 'HRSover50a' # Text string to use as prefix for figure filenames
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
age_min = 50.0    # Minimum age in the data
age_max = 115.0   # Maximum age in the data
age_incr = 1.0    # Age increment in years
wave_length = 2   # Number of periods between actual data collection waves
report_type_count = 3       # Number of discrete types whose SRHS report variance differs
mixed_health_shocks = True # Whether health shocks are a mixed normal

# Define a test parameter vector
current_param_vec = np.array([ 
    2.1045441873618382,  # 0 Mort0
    0.0,  # 1 MortSex
    1.9146039449285808,  # 2 MortHealth1
    -0.14584418616864758,  # 3 MortHealth2
    -1.6169023004714786,  # 4 MortHealth3
    0.0,  # 5 MortHealth4
    -4.748510926023278,  # 6 MortAge1
    21.470280714069798,  # 7 MortAge2
    -132.1428100592593,  # 8 MortAge3
    0.0,  # 9 MortAge4
    -7.143127693593169,  # 10 MortHealthAge
    0.0,  # 11 MortSexAge
    3.346083037519849,  # 12 Corr0
    2.9572962316096154,  # 13 CorrAge1
    0.0,  # 14 CorrAge2
    0.0,  # 15 CorrAge3
    0.0,  # 16 CorrAge4
    2.432266767950102,  # 17 Health0
    0.0,  # 18 HealthSex
    0.1918245652139637,  # 19 HealthAge1
    -3.160745323372365,  # 20 HealthAge2
    0.0,  # 21 HealthAge3
    0.0,  # 22 HealthAge4
    0.0,  # 23 HealthAgeSex
    7.368492255457024,  # 24 xInitMean
    3.850185617336482,  # 25 xInitStd
    -2.2910986470712698,  # 26 HealthShockAvg1
    1.3270814822342571,  # 27 HealthShockLogStd1
    -3.1486389999739886,  # 28 HealthShockLogit1
    0.11912419794321165,  # 29 SRHSlogStd1
    0.7853345992898264,  # 30 SRHSlogStd2
    -0.1155308713253138,  # 31 TypeLogit1
    -2.0209483668233856,  # 32 TypeLogit2
    0.4810582660854592,  # 33 SRHS_Coeff
    1.7401153291729339,  # 34 SRHS_Cut2
    1.6365157706604863,  # 35 SRHS_Cut3
    1.8363814101950675,  # 36 SRHS_Cut4
]) 

which_indices = np.array([0,2,3,4,6,7,8,10,12,13,17,19,20,24,25,26,27,28,29,30,31,32,33,34,35,36]) 
#which_indices = np.array([26,27,28,29,30,31,32])
#which_indices = np.array([12,13,17,19,20])
#which_indices = np.array([17,19,20])
#  100511.9552370834
