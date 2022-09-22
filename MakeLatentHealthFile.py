'''
This module contains a subset of the functions in HiddenHealthEstimation.py,
lightly edited to be used only to generate two different kinds of output file
to be used for other research applications.

First, it can produce a binary data file with latent health distributions by age,
Markov matrices over latent health transitions, mortality probabilities by age
and health, and SRHS reporting probabilities by latent health and reporting type.
The data file can be read into memory by another project that uses an exogenous
health process; see LoadLatentHealthProcess.py.

Second, it can produce a tab-delimited text file with summary statistics for the
distribution of latent health (and reporting type) conditional on a respondent's
sex, current age, and a sequence of SRHS reported in current and prior survey
waves. The text file can be loaded into econometric software (such as Stata)
and merged with panel data to provide the model's prediction of the distribution
of latent health (and reporting type) given observed sequences of SRHS. That is,
it provides a sort of "filtration" of latent health from SRHS observations.

To use this file in applied work, choose a specification of the latent health
model (the main specification is called TwoStudyAllOver23HeteroParams), a number
of nodes in the discretization, minimum and maximum values of latent health,
and a number of survey waves on which to condition the distribution of latent
health (filtration only). Other necessary parameters will be loaded automatically
from the named parameter file. For ease of use, this script can be run from a
command line using the following syntax:
    
> python MakeLatentHealthFile.py worktype spec_name output_name node_count health_min health_max Z_to_cond

worktype    : The type of output to be produced, must be "filter" or "process".
spec_name   : The name of the specification file, with no .py file extension.
output_name : The name of the file to which to write the latent health process.
node_count  : The integer number of nodes in the latent health discretization.
health_min  : The minimum value of latent health in the discretization.
health_max  : The maximum value of latent health in the discretization.
Z_to_cond   : The number of survey waves on which to condition latent health (filter only).

As an example, the coarse discretization based on the main specification, as 
described in section 5 of the paper, can be created by:
    
> python MakeLatentHealthFile.py process TwoStudyAllOver23HeteroParams MainResults.dat 40 -6 22

A very coarse discretization using only 15 latent health nodes, based on parameters
re-estimated with this very coarse grid, can be created by:

> python MakeLatentHealthFile.py process TwoStudyAllTinyParams TinyResults.dat 15 -6 22

A tab-delimited text file with summary statistics for the distribution of latent
health for any combination of sex, age, and observed sequence of SRHS (up to three
waves long), based on the main specification estimated in the paper, can be made by:
    
> python MakeLatentHealthFile.py filter TwoStudyAllOver23HeteroParams ConditionalHealthDstn.txt 120 -12 28

Alternatively, the line 'my_args = sys.argv' near the top of the code can be
commented out, and the nearby line defining my_args can be uncommented and edited.
This allows the script to be run with no additional arguments, if preferred.
The three examples above are included in the code (commented out).

Once a discretization has been made with this script, it can be read from disk
using the file LoadLatentHealthProcess.py; see documentation in that file. The
"filtration" data can be loaded into Stata with the insheet command, sorted,
and then merged (many-to-one) into a panel dataset with SRHS observations.
'''
from struct import pack
from time import time
import sys
import numpy as np
import itertools
from scipy.stats import norm
from scipy.special import perm, factorial
sys.path.insert(0, './ParameterSpecs')

# Get system arguments
my_args = sys.argv
#my_args = [None, 'process', 'TwoStudyAllOver23HeteroParams', 'MainResults.dat', '40', '-6', '22']
#my_args = [None, 'process', 'TwoStudyAllTinyParams', 'TinyResults.dat', '15', '-6', '22']
#my_args = [None, 'filter', 'TwoStudyAllOver23HeteroParams', 'ConditionalHealthDstn.txt', '120', '-12', '28', '3']

# Process required arguments
if len(my_args) < 4:
    print('Please read the documentation at the top of MakeLatentHealthProcess.py to use this file.')
worktype = my_args[1]
spec_name = my_args[2]
output_name = my_args[3]
if not ((worktype == 'filter') or (worktype == 'process')):
    print('First passed argument should be "filter" or "process"; please read the documentation at the top of MakeLatentHealthProcess.py.')
    print('Code will not produce any output file.')

# Initialize a bunch of variables, which will be overwritten. This exists solely so that Spyder doesn't flag a bunch of stuff as errors.
measure_count = None
category_counts = None
report_type_count = None
mixed_health_shocks = None
current_param_vec = None
age_min = None
age_max = None
age_incr = None
x_min = None
x_max = None
x_count = None
source_name = None
wave_length = None

# Import parameters to be used to construct discretized latent health process
import_list = ['measure_count', 'category_counts', 'report_type_count', 'mixed_health_shocks', 'wave_length',\
               'current_param_vec', 'age_min', 'age_max', 'age_incr', 'x_min', 'x_max', 'x_count', 'source_name']
import_command = 'from ' + spec_name + ' import '
for j in range(len(import_list)):
    import_command += import_list[j] + ', '
import_command = import_command[:-2]
exec(import_command)

# Calculate some basic values from the exogenous parameters
report_count = np.sum(category_counts)
measure_starts = np.concatenate((np.array([0]),np.cumsum(category_counts)[:-1]))
h_count = category_counts[0] # Number of SRHS categories
x_count_cond = x_count // report_type_count

# Account for optional parameters
if len(my_args) > 4:
    x_count_cond = int(my_args[4])
    x_count = x_count_cond*report_type_count
if len(my_args) > 5:
    x_min = float(my_args[5])
if len(my_args) > 6:
    x_max = float(my_args[6])
if len(my_args) > 7:
    Z_to_cond = int(my_args[7])

# Define the cut points for the continuous health variable x, and the midpoints
if x_count % report_type_count > 0:
    print('x_count is not divisible by report_type_count, code will break!')
x_cuts = np.linspace(x_min,x_max,num=x_count_cond+1)
x_grid = (x_cuts[1:] + x_cuts[:-1])/2.
x_step = x_grid[1] - x_grid[0]
x_grid_rep = np.tile(x_grid, report_type_count)
age_count_A = int((age_max - age_min)/age_incr + 1)

def mystr(x):
    return "{:.3f}".format(x)

# Define a function to convert from "Taylor parameters" to polynomial coefficients
def changeTaylorToPoly(taylor, x0):
    '''
    Change a vector of derivatives at x0 into a polynomial coefficient vector.
    
    Parameters
    ----------
    taylor : np.array
        Array of derivatives of the function at x0: f(x0), f'(x0), f''(x0), ...
    x0 : float
        Point around which the Taylor expansion is defined.
        
    Returns
    -------
    coeffs : np.array
        Array of polynomial coefficients: f(x) = a0 + a1+x1  + a2*x2**2 + ...
    '''
    coeffs = np.zeros_like(taylor)
    N = taylor.size
    
    for n in range(N-1,-1,-1):
        this = taylor[n]/factorial(n)
        for j in range(N-1,n,-1):
            this -= perm(j,n)/factorial(n)*coeffs[j]*x0**(j-n)
        coeffs[n] = this
        
    return coeffs


# Define the function to produce survival probabilities
def makeLivPrbArray(age_min,age_max,age_incr,Mort0,MortSex,MortHealth1,MortHealth2,
                    MortHealth3,MortHealth4,MortAge1,MortAge2,MortAge3,MortAge4,
                    MortHealthAge,MortSexAge):
    '''
    Make a 3D array of survival probabilitities: sex X age X health.  Uses given
    parameters and boundaries for the age range.
    
    Parameters
    ----------
    age_min : float
        Minimum value that age takes on in model.
    age_max : float
        Maximum value that age takes on in model.
    age_incr : float
        Increment for age in the model.
    Mort0 : float
        Constant in mortality probit function.
    MortSex : float
        Shifter for being male in mortality probit function.
    MortHealth1 : float
        Linear coefficient on health in mortality probit function.
    MortHealth2 : float
        Quadratic coefficient on health in mortality probit function.
    MortHealth3 : float
        Cubic coefficient on health in mortality probit function.
    MortHealth4 : float
        Quartic coefficient on health in mortality probit function.
    MortAge1 : float
        Linear coefficient on age in mortality probit function.
    MortAge2 : float
        Quadratic coefficient on age in mortality probit function.
    MortAge3 : float
        Cubic coefficient on age in mortality probit function.
    MortAge4 : float
        Quartic coefficient on age in mortality probit function.
    MortHealthAge : float
        Interaction term between health and age in mortality probit function.
    MortSexAge : float
        Interaction term between health and sex in mortality probit function.
        
    Returns
    -------
    LivPrbArray : np.array
        Array of shape (2,age_count,x_count) with survival probabilities.
    '''
    ThetaFunc = lambda s,j,x : Mort0 + MortSex*s + MortHealth1*x + MortHealth2*x**2 + MortHealth3*x**3 + MortHealth4*x**4 + MortAge1*j + MortAge2*j**2 + MortAge3*j**3 + MortAge4*j**4 + MortHealthAge*j*x + MortSexAge*s*j
    age_count = int(np.round((age_max - age_min)/age_incr)) + 1
    
    AgeVec = np.linspace(age_min,age_max,num=age_count)
    AgeArray = np.tile(np.reshape(AgeVec,(1,age_count,1)),(1,1,x_count_cond))
    xArray = np.tile(np.reshape(x_grid,(1,1,x_count_cond)),(1,age_count,1))
    
    thetaArray = np.zeros((2,age_count,x_count_cond))
    thetaArray[0,:,:] = ThetaFunc(0,AgeArray,xArray)
    thetaArray[1,:,:] = ThetaFunc(1,AgeArray,xArray)

    LivPrbArray = norm.cdf(thetaArray)
    return LivPrbArray


# Define the function that constructs the array of transition probabilities
def makeTransProbArray(age_min,age_max,age_incr,Corr0,CorrAge1,CorrAge2,CorrAge3,
                       CorrAge4,Health0,HealthSex,HealthAge1,HealthAge2,HealthAge3,
                       HealthAge4,HealthAgeSex,HealthShockAvgs,HealthShockStds,HealthShockPrbs):
    '''
    Make a 4D array of health transition probabilities: sex X age X x_t X x_t+1.
    
    Parameters
    ----------
    age_min : float
        Minimum value that age takes on in model.
    age_max : float
        Maximum value that age takes on in model.
    age_incr : float
        Increment for age in the model.
    Corr0 : float
        Constant in correlation coefficient function.
    CorrAge1 : float
        Linear coefficient on age in correlation coefficient function.
    CorrAge2 : float
        Quadratic coefficient on age in correlation coefficient function.
    CorrAge3 : float
        Cubic coefficient on age in correlation coefficient function.
    CorrAge4 : float
        Quartic coefficient on age in correlation coefficient function.
    Health0 : float
        Constant in expected next health function.
    HealthSex : float
        Shifter for sex in expected next health function.
    HealthAge1 : float
        Linear coefficient in expected next health function.
    HealthAge2 : float
        Quadratic coefficient in expected next health function.
    HealthAge3 : float
        Cubic coefficient in expected next health function.
    HealthAge4 : float
        Quartic coefficient in expected next health function.
    HealthAgeSex : float
        Interaction between age and sex in expected next health function.
    HealthShockAvgs : [float]
        Vector of health shock means; should have overall mean 0 when weighting by probs.
    HealthShockStds : [float]
        Vector of health shock means; should have overall std 1 when weighting by probs.
    HealthShockPrbs : [float]
        Vector of weights for the mixed normal health shocks, summing to 1.
    
    Returns
    -------
    TransPrbArray : np.array
        Array of shape (2,age_count,x_count,x_count) with transition probabilities
        between health states at each sex and age.
    '''
    # Make correlation vector by age
    AgeVec = np.linspace(age_min,age_max,num=age_count_A)
    CorrVecBase = Corr0 + CorrAge1*AgeVec + CorrAge2*AgeVec**2 + CorrAge3*AgeVec**3 + CorrAge4*AgeVec**4
    CorrVec = np.exp(CorrVecBase)/(1. + np.exp(CorrVecBase))
    
    # Make end points of grid go to infinity
    x_cuts_temp = x_cuts.copy()
    x_cuts_temp[0] = -np.inf
    x_cuts_temp[-1] = np.inf
    x_cuts_tiled = np.tile(np.reshape(x_cuts_temp,(1,x_count_cond+1)),(x_count_cond,1))
    
    TransPrbArray = np.zeros((2,age_count_A,x_count_cond,x_count_cond))
    N = len(HealthShockPrbs)
    for s in range(2):
        for j in range(age_count_A):
            Age = AgeVec[j]
            Corr = CorrVec[j]
            ExpHealthBase = Health0 + HealthAge1*Age + HealthAge2*Age**2 + HealthAge3*Age**3 + HealthAge4*Age**4 + HealthSex*s + HealthAgeSex*s*Age
            ExpHealthNext = Corr*x_grid + (1.-Corr)*ExpHealthBase
            ExpHealthNext_tiled = np.tile(np.reshape(ExpHealthNext,(x_count_cond,1)),(1,x_count_cond+1))
            for n in range(N):
                distance_array = (x_cuts_tiled - (ExpHealthNext_tiled + HealthShockAvgs[n]))/HealthShockStds[n]
                CDF_array = norm.cdf(distance_array)
                SF_array  = norm.sf(distance_array)
                these = distance_array[:,:-1] < 4.0
                prob_array_base = np.zeros((x_count_cond,x_count_cond))
                prob_array_base[these] = CDF_array[:,1:][these] - CDF_array[:,:-1][these]
                these = np.logical_not(these)
                prob_array_base[these] = SF_array[:,:-1][these] - SF_array[:,1:][these]
                sum_array = np.tile(np.reshape(np.sum(prob_array_base,axis=1),(x_count_cond,1)),(1,x_count_cond))
                prob_array = prob_array_base/sum_array
                TransPrbArray[s,j,:,:] += HealthShockPrbs[n]*prob_array

    return TransPrbArray


# Define the function that constructs categorical health observation probabilities
def makeReportPrbArray(Constants,Coeffs,CutLists,ReportStds):
    '''
    Make an array with the probability of reporting each categorical response
    from each value on the x_grid, for each measure.
    
    Parameters
    ----------
    Constants : np.array
        Level shifter for each measure in mapping from x to report probit.
    Coeffs : np.array
        Linear coefficient for each measure in mapping from x to report probit.
    CutLists : [np.array]
        List of arrays of size (category_count[j]-2) cutoff points in the space
        of x.  The lowest cut point for each measure is assumed to be zero.
    ReportStds : np.array
        Array of SRHS reporting error standard deviations.
        
    Returns
    -------
    ReportPrbArray : np.array
        Array of shape (type_count,report_count,x_count_cond) with the probability of reporting
        each categorical answer for each measure when the individual's true health is x.
    '''
    ReportPrbArray = np.zeros((report_count,x_count)) + np.nan
    
    pos = 0
    for j in range(measure_count):
        Const = Constants[j]
        Coeff = Coeffs[j]
        CutList = np.cumsum(CutLists[j])
        c_count = category_counts[j]
    
        Cuts_plus = np.concatenate(([-np.inf,0.0],CutList,[np.inf]))
        Cuts_tiled = np.tile(np.reshape(Cuts_plus,(1,c_count+1)),(x_count_cond,1))
        y_grid = Const + Coeff*x_grid
        y_grid_tiled = np.tile(np.reshape(y_grid,(x_count_cond,1)),(1,c_count+1))
        distance_array = (Cuts_tiled - y_grid_tiled)
        
        if j == 0: # If this measure is SRHS, then use different reporting error std for each type
            for n in range(report_type_count):
                distance_array_temp = distance_array / ReportStds[n]
                CDF_array = norm.cdf(distance_array_temp)
                ReportPrbArray[pos:(pos+c_count),(n*x_count_cond):((n+1)*x_count_cond)] = np.transpose(CDF_array[:,1:] - CDF_array[:,:-1])
        else: # For all other measures, use standard normal reporting error
            CDF_array = norm.cdf(distance_array)
            ReportPrbArray[pos:(pos+c_count),:] = np.tile(np.transpose(CDF_array[:,1:] - CDF_array[:,:-1]), report_type_count)
        
        pos += c_count
    
    # Reshape the reporting probabilities and return it
    ReportPrbArrayX = np.zeros((report_type_count, report_count, x_count_cond))
    for k in range(report_type_count):
        bot = k*x_count_cond
        top = (k+1)*x_count_cond
        for h in range(report_count):
            ReportPrbArrayX[k,h,:] = ReportPrbArray[h,bot:top]
    return ReportPrbArrayX


# Define the function that constructs the distribution of health for individuals
# when they are first observed in the data
def makeInitialHealthDstn(LivPrbArray,TransPrbArray,xInitMean,xInitStd,TypePrbs):
    '''
    Make an array with the unconditional distribution of the continuous health
    state x for someone who has been observed for the first time.
    
    Parameters
    ----------
    LivPrbArray : np.array
        Survival probabilities at each sex, age, and health state.
    TransPrbArray : np.array
        Transitions probabilities at each sex, age, and health state combination.
    xInitMean : float
        Mean of health at the earliest age in the model.
    xInitStd : float
        Standard devation of health at the earliest age in the model.
    TypePrbs : np.array
        Array of population shares of each reporting type (should sum to 1).
        
    Returns
    -------
    InitialHealthDstn : np.array
        Array of shape (2,age_count,x_count) with the unconditional distribution
        of continuous health x at age j and sex s.
    '''
    T = LivPrbArray.shape[1]
    InitialHealthDstn = np.zeros((2,T,x_count_cond))
    
    # Approximate the distribution of health at the earliest age in the model
    distances = (x_cuts - xInitMean)/xInitStd
    distances[0] = -20.
    distances[-1] = 20.
    CDFs = norm.cdf(distances)
    prob_base = CDFs[1:] - CDFs[:-1]
    HealthDstn0 = prob_base/np.sum(prob_base)
    
    # Loop over the two sexes
    for s in range(2):
        HealthDstnNow = HealthDstn0.copy()
        for j in range(T):
            InitialHealthDstn[s,j,:] = HealthDstnNow
            LivPrbs = LivPrbArray[s,j,:x_count_cond]
            TempDstn = HealthDstnNow*LivPrbs
            HealthDstnNow = TempDstn/np.sum(TempDstn)
            TransPrbs = TransPrbArray[s,j,:x_count_cond,:x_count_cond]
            HealthDstnNow = np.dot(np.transpose(TransPrbs),HealthDstnNow)
            
    return InitialHealthDstn
    

# Define the function that constructs arrays for the LL evaluation
def makeProbArrays(age_min,age_max,age_incr,Mort0,MortSex,MortHealth1,MortHealth2,
                   MortHealth3,MortHealth4,MortAge1,MortAge2,MortAge3,MortAge4,
                   MortHealthAge,MortSexAge,Corr0,CorrAge1,CorrAge2,CorrAge3,
                   CorrAge4,Health0,HealthSex,HealthAge1,HealthAge2,HealthAge3,
                   HealthAge4,HealthAgeSex,HealthShockAvgs,HealthShockStds,
                   HealthShockPrbs,ReportConstants,ReportCoeffs,ReportCuts,
                   ReportStds,TypePrbs,xInitMean,xInitStd):
    '''
    Construct LivPrbArray, TransPrbArray, ReportPrbArray, and HealthInitDstn
    from model paramaters.
    
    Parameters
    ----------
    age_min : float
        Minimum value that age takes on in model.
    age_max : float
        Maximum value that age takes on in model.
    age_incr : float
        Increment for age in the model.
    Mort0 : float
        Constant in mortality probit function.
    MortSex : float
        Shifter for being male in mortality probit function.
    MortHealth1 : float
        Linear coefficient on health in mortality probit function.
    MortHealth2 : float
        Quadratic coefficient on health in mortality probit function.
    MortHealth3 : float
        Cubic coefficient on health in mortality probit function.
    MortHealth4 : float
        Quartic coefficient on health in mortality probit function.
    MortAge1 : float
        Linear coefficient on age in mortality probit function.
    MortAge2 : float
        Quadratic coefficient on age in mortality probit function.
    MortAge3 : float
        Cubic coefficient on age in mortality probit function.
    MortAge4 : float
        Quartic coefficient on age in mortality probit function.
    MortHealthAge : float
        Interaction term between health and age in mortality probit function.
    MortSexAge : float
        Interaction term between health and sex in mortality probit function.
    Corr0 : float
        Constant in correlation coefficient function.
    CorrAge1 : float
        Linear coefficient on age in correlation coefficient function.
    CorrAge2 : float
        Quadratic coefficient on age in correlation coefficient function.
    CorrAge3 : float
        Cubic coefficient on age in correlation coefficient function.
    CorrAge4 : float
        Quartic coefficient on age in correlation coefficient function.
    Health0 : float
        Constant in expected next health function.
    HealthSex : float
        Shifter for sex in expected next health function.
    HealthAge1 : float
        Linear coefficient in expected next health function.
    HealthAge2 : float
        Quadratic coefficient in expected next health function.
    HealthAge3 : float
        Cubic coefficient in expected next health function.
    HealthAge4 : float
        Quartic coefficient in expected next health function.
    HealthAgeSex : float
        Interaction between age and sex in expected next health function.
    HealthShockAvgs : [float]
        Vector of health shock means; should have overall mean 0 when weighting by probs.
    HealthShockStds : [float]
        Vector of health shock means; should have overall std 1 when weighting by probs.
    HealthShockPrbs : [float]
        Vector of weights for the mixed normal health shocks, summing to 1.
    ReportConstants : [float]
         List of measure_count - 1 constant terms in report probit equations.
    ReportCoeffs : [float]
         List of measure_count linear coefficients on x in report probit equations.
    ReportCuts : [float]
        List of report_count-2*measure_count cutoff points in the space of x.
        The lowest cut point for each measure is assumed to be zero.
    ReportStds : [float]
        List of SRHS reporting error standard deviations by type.
    TypePrbs : [float]
        Accompanying list of probabilities of each reporting type.
    xInitMean : float
        Mean of health at the earliest age in the model.
    xInitStd : float
        Standard devation of health at the earliest age in the model.
        
    Returns
    -------
    LivPrbArray : np.array
        Array of shape (2,age_count,x_count) with survival probabilities.
    TransPrbArray : np.array
        Array of shape (2,age_count,x_count,x_count) with transition probabilities
        between health states at each sex and age.
    ReportPrbArray : np.array
        Array of shape (h_count,x_count) with the probability of reporting health
        status h when the individual's true health is x.
    InitialHealthDstn : np.array
        Array of shape (2,age_count,x_count) with the unconditional distribution
        of continuous health x at age j and sex s.
    '''
    LivPrbArray = makeLivPrbArray(
                    age_min,age_max,age_incr,Mort0,MortSex,MortHealth1,MortHealth2,
                    MortHealth3,MortHealth4,MortAge1,MortAge2,MortAge3,MortAge4,
                    MortHealthAge,MortSexAge)
    
    TransPrbArray = makeTransProbArray(
                       age_min,age_max,age_incr,Corr0,CorrAge1,CorrAge2,CorrAge3,
                       CorrAge4,Health0,HealthSex,HealthAge1,HealthAge2,HealthAge3,
                       HealthAge4,HealthAgeSex,HealthShockAvgs,HealthShockStds,HealthShockPrbs)
    
    ReportCutLists = []
    pos = 0
    for j in range(measure_count):
        c_count = category_counts[j] - 2
        ReportCutLists.append(ReportCuts[pos:(pos+c_count)])
        pos += c_count
    ReportPrbArray = makeReportPrbArray(ReportConstants,ReportCoeffs,ReportCutLists,ReportStds)
    
    HealthInitDstn = makeInitialHealthDstn(LivPrbArray,TransPrbArray,xInitMean,xInitStd,TypePrbs)
    
    return LivPrbArray, TransPrbArray, ReportPrbArray, HealthInitDstn



# Define a function that translates a vector of parameters into a dictionary
def makeParameterDict(param_vec, return_as_array=False):
    '''
    Transforms a vector of size 27 + h_count - 2 into a dictionary.
    
    Parameters
    ----------
    param_vec : np.array
        Array of model parameters; order is shown in code.
    return_as_array : bool
        Indicator for whether this function should return a 1D array of structural
        parameters rather than a dictionary.
        
    Returns
    -------
    param_dict : dictionary
        Dictionary that can be used in makeProbArrays.
    '''
    # Get parameter indices
    a = 26 + mixed_health_shocks*3
    constants = measure_count - 1
    coefficients = measure_count
    b = a + report_type_count - 1
    c = b + report_type_count - 1
    d = c + constants
    e = d + coefficients
    
    # Rescale coefficients
    MortHealthTaylor = np.array([0., param_vec[2]*1e-1, param_vec[3]*1e-2, param_vec[4]*1e-3, param_vec[5]*1e-4])
    MortAgeTaylor = np.array([param_vec[0], param_vec[6]*1e-2, param_vec[7]*1e-4, param_vec[8]*1e-6, param_vec[9]*1e-8])
    CorrTaylor = np.array([param_vec[12], param_vec[13]*1e-2, param_vec[14]*1e-4, param_vec[15]*1e-6, param_vec[16]*1e-8])
    HealthAgeTaylor = np.array([param_vec[17], param_vec[19]*1e-1, param_vec[20]*1e-2, param_vec[21]*1e-3, param_vec[22]*1e-4])
    
    # Transform raw parameters into coefficients
    MortHealthCoeffs = changeTaylorToPoly(MortHealthTaylor, 0.)
    MortAgeCoeffs = changeTaylorToPoly(MortAgeTaylor, age_min)
    CorrCoeffs = changeTaylorToPoly(CorrTaylor, age_min)
    HealthAgeCoeffs = changeTaylorToPoly(HealthAgeTaylor, age_min)
    
    if mixed_health_shocks:
        HealthShockAvgs = np.zeros(2)
        HealthShockStds = np.zeros(2)
        temp = np.array([0., param_vec[28]])
        HealthShockPrbs = np.exp(temp)/np.sum(np.exp(temp))
        HealthShockAvgs[1] = param_vec[26]
        HealthShockAvgs[0] = -HealthShockPrbs[1]*HealthShockAvgs[1]/HealthShockPrbs[0]
        HealthShockStds[1] = np.exp(param_vec[27])
        P = HealthShockPrbs
        M = HealthShockAvgs
        S = HealthShockStds
        HealthShockStds[0] = np.sqrt((1. - P[0]*M[0]**2 - P[1]*(S[1]**2 + M[1]**2))/P[0])
    else:
        HealthShockAvgs = np.zeros(1)
        HealthShockStds = np.ones(1)
        HealthShockPrbs = np.ones(1)
    
    # Calculate SRHS reporting type probabilities and standard deviations
    if report_type_count > 1:
        ExpBase = np.concatenate([[1.], np.exp(param_vec[b:c])])
        TypePrbs = ExpBase/np.sum(ExpBase)
        ReportStds_temp = np.exp(param_vec[a:b])
        ReportVars_temp = ReportStds_temp**2
        ReportVar_new = (1. - np.dot(ReportVars_temp, TypePrbs[1:]))/TypePrbs[0]
        ReportStds = np.sqrt(np.concatenate([[ReportVar_new], ReportVars_temp]))
    else:
        TypePrbs = np.array([1.])
        ReportStds = np.array([1.])
    
    if return_as_array: # This is for standard errors only
        CumulativeCuts = []
        CutPoints = param_vec[e:]
        i = 0
        for m in range(measure_count):
            C = category_counts[m]
            these_cuts = np.cumsum(CutPoints[i:(i+C-2)])
            CumulativeCuts += these_cuts.tolist()
            i += C-2
    
        param_vec_out = np.concatenate([
            param_vec[0:2],
            MortHealthTaylor[1:5],
            MortAgeTaylor[1:5],
            [param_vec[10]*1e-4,
            param_vec[11]*1e-3],
            CorrTaylor,
            param_vec[17:19],
            HealthAgeTaylor[1:5],
            [param_vec[23]*1e-3],
            HealthShockAvgs,
            HealthShockStds,
            HealthShockPrbs,
            param_vec[24:26],
            ReportStds,
            TypePrbs,
            np.concatenate(([0.],param_vec[c:d])),
            param_vec[d:e],
            CumulativeCuts, # Processed into cut points rather than widths
        ])
        return param_vec_out
    
    param_dict = {
            'age_min' :       age_min,
            'age_max' :       age_max,
            'age_incr' :      age_incr,
            'Mort0' :         MortAgeCoeffs[0],
            'MortSex' :       param_vec[1],
            'MortHealth1' :   MortHealthCoeffs[1],
            'MortHealth2' :   MortHealthCoeffs[2],
            'MortHealth3' :   MortHealthCoeffs[3],
            'MortHealth4' :   MortHealthCoeffs[4],
            'MortAge1' :      MortAgeCoeffs[1],
            'MortAge2' :      MortAgeCoeffs[2],
            'MortAge3' :      MortAgeCoeffs[3],
            'MortAge4' :      MortAgeCoeffs[4],
            'MortHealthAge' : param_vec[10]*1e-4,
            'MortSexAge' :    param_vec[11]*1e-3,
            'Corr0' :         CorrCoeffs[0],
            'CorrAge1' :      CorrCoeffs[1],
            'CorrAge2' :      CorrCoeffs[2],
            'CorrAge3' :      CorrCoeffs[3],
            'CorrAge4' :      CorrCoeffs[4],
            'Health0' :       HealthAgeCoeffs[0],
            'HealthSex' :     param_vec[18],
            'HealthAge1' :    HealthAgeCoeffs[1],
            'HealthAge2' :    HealthAgeCoeffs[2], 
            'HealthAge3' :    HealthAgeCoeffs[3],
            'HealthAge4' :    HealthAgeCoeffs[4],
            'HealthAgeSex' :  param_vec[23]*1e-3,
            'HealthShockAvgs' : HealthShockAvgs,
            'HealthShockStds' : HealthShockStds,
            'HealthShockPrbs' : HealthShockPrbs,
            'xInitMean' :     param_vec[24],
            'xInitStd' :      param_vec[25],
            'ReportStds' :    ReportStds,
            'TypePrbs' :      TypePrbs,
            'ReportConstants' : np.concatenate(([0],param_vec[c:d])),
            'ReportCoeffs' :  param_vec[d:e],
            'ReportCuts' :    param_vec[e:],
            }
    
    return param_dict


# Construct latent health arrays from the structural parameter vector
my_dict = makeParameterDict(current_param_vec)
LivPrbArray, TransPrbArray, ReportPrbArray, HealthInitDstn = makeProbArrays(**my_dict)

if worktype == 'process':
    # Write the arrays to disk so that they can be imported in other work
    t0 = time()
    with open(output_name, 'wb') as f:
        
        # Write grid sizes to file
        f.write(int(x_count_cond).to_bytes(1, 'big'))
        f.write(int(age_count_A).to_bytes(1, 'big'))
        f.write(int(report_count).to_bytes(1, 'big'))
        f.write((report_type_count).to_bytes(1, 'big'))
        
        # Write the latent health grid to the file
        for h in range(x_count_cond):
            f.write(pack('>d', x_grid[h]))
            
        # Write survival probabilities to the file
        for s in range(2):
            for j in range(age_count_A):
                for h in range(x_count_cond):
                    f.write(pack('>d', LivPrbArray[s,j,h]))
                    
        # Write transition probabilities to the file
        for s in range(2):
            for j in range(age_count_A):
                for i in range(x_count_cond):
                    for h in range(x_count_cond):
                        f.write(pack('>d', TransPrbArray[s,j,i,h]))
                        
        # Write SRHS reporting probabilities to the file
        for k in range(report_type_count):
            for x in range(report_count):
                for h in range(x_count_cond):
                    f.write(pack('>d', ReportPrbArray[k,x,h]))
                    
        # Write initial health distributions to the file
        for s in range(2):
            for j in range(age_count_A):
                for h in range(x_count_cond):
                    f.write(pack('>d', HealthInitDstn[s,j,h]))
        
        f.close()
    t1 = time()
    
    # Describe the specification used, printing to screen
    print('Wrote discretized latent health process to ' + output_name + ' in ' + mystr(t1-t0) + ' seconds.')
    print('The process is based on the parameters in the specification called ' + spec_name + '.')
    print('It discretizes latent health with ' + str(x_count_cond) + ' nodes equally spaced between ' + str(x_min) + ' and ' + str(x_max) + '.')
    print('There are ' + str(age_count_A) + ' ages from ' + str(age_min) + ' to ' + str(age_max) + ' and ' + str(report_type_count) + ' reporting types.')
    for k in range(report_type_count):
        this_line = 'Reporting type ' + str(k+1) + ' ('
        this_line += "{:.2%}".format(my_dict['TypePrbs'][k])
        this_line += ') has a reporting error standard deviation of '
        this_line += mystr(my_dict['ReportStds'][k]) + '.'
        print(this_line)


if worktype == 'filter':
    t0 = time()
    T = Z_to_cond # Rename
    
    # Reshape discretized latent health arrays
    ReportPrbArray = np.reshape(np.transpose(ReportPrbArray, [0,2,1]), (x_count_cond*report_type_count, report_count))
    LivPrbArray = np.tile(LivPrbArray, (1,1,report_type_count))
    HealthInitDstn = np.tile(HealthInitDstn, (1,1,report_type_count))
    for k in range(report_type_count):
        bot = x_count_cond*k
        top = x_count_cond*(k+1)
        HealthInitDstn[:,:,bot:top] *= my_dict['TypePrbs'][k]
    TransPrbArray_big = np.zeros((2,age_count_A,x_count,x_count))
    for n in range(report_type_count):
        TransPrbArray_big[:,:,(n*x_count_cond):((n+1)*x_count_cond),(n*x_count_cond):((n+1)*x_count_cond)] = TransPrbArray
    TransPrbArray = TransPrbArray_big
    
    # Make all permutations of a SRHS histories of length T
    SRHS_list = [-1] + list(np.arange(1,report_count+1).astype(int))
    SRHS_listX = T*[SRHS_list]
    SRHS_sequences = list(itertools.product(*SRHS_listX))
    
    # Make a list of all ages in the data
    age_list = list(np.arange(age_min, age_max + age_incr, age_incr))
    
    # Loop through each sex, age, and sequence of SRHS
    output = 'sex\tage\t'
    temp = 'SRHSt\t'
    for z in range(T-1):
        temp = 'SRHStm' + str(z+1) + '\t' + temp
    output += temp
    for k in range(report_type_count):
        output += 'typeprob' + str(k+1) + '\t'
    output += 'healthmean\thealthstdev\thealthskew\thealthkurt\n'
    
    for s in range(2):
        for j in range(age_count_A):
            for l in range(len(SRHS_sequences)):
                seq = SRHS_sequences[l]
                j0 = j
                
                # Adjust initial age for missing
                age = age_list[j]
                missing_to_start = 0
                t = 0
                while (t < T and seq[t] == -1):
                    missing_to_start += 1
                    t += 1
                Z = T - missing_to_start
                if Z > 1:
                    T_to_sim = (Z-1)*wave_length
                    age -= T_to_sim*age_incr
                    j0 -= T_to_sim
                else:
                    T_to_sim = 0
                
                if age < age_min:
                    continue # Can't do this sequence, uses SRHS from before age_min
                    
                # Generate a discretized distribution of latent health conditional on initial age and observed sequence
                p_vec = HealthInitDstn[s,j0,:].copy()
                t_to_next_wave = 0
                z = missing_to_start
                for t in range(T_to_sim+1):
                    if (t_to_next_wave == 0):
                        try:
                            SRHS = seq[z]
                        except:
                            SRHS = -1
                        if SRHS != -1: # Update discrete distribution if SRHS is observed
                            SRHS -= 1
                            p_vec *= ReportPrbArray[:, SRHS]
                            p_vec /= np.sum(p_vec)
                        z += 1
                        t_to_next_wave = wave_length
                    if t < (T_to_sim):
                        p_vec *= LivPrbArray[s,j0+t,:] # Apply survival
                        p_vec /= np.sum(p_vec)
                        p_vec = np.dot(np.transpose(TransPrbArray[s,j0+t,:,:]), p_vec) # Apply transitions
                        p_vec /= np.sum(p_vec)
                    t_to_next_wave -= 1
                age += T_to_sim*age_incr # Advance age from the "simulation"
                
                # Reshape the discretization and produce a latent health dstn and type probs
                p_array = np.reshape(p_vec, (report_type_count, x_count_cond))
                HealthDstn = np.sum(p_array, axis=0)
                TypePrbs = np.sum(p_array, axis=1)
                
                # Make a tab-delimited entry for this sex-age-sequence
                HealthMean = np.dot(x_grid, HealthDstn)
                HealthStdev = np.sqrt(np.dot((x_grid - HealthMean)**2, HealthDstn))
                HealthSkew = np.dot(((x_grid - HealthMean)/HealthStdev)**3, HealthDstn)
                HealthKurt = np.dot(((x_grid - HealthMean)/HealthStdev)**4, HealthDstn)
                this_line = str(s) + '\t' + str(age) + '\t'
                for z in range(T):
                    this_line += str(seq[z]) + '\t'
                for k in range(report_type_count):
                    this_line += str(TypePrbs[k]) + '\t'
                this_line += str(HealthMean) + '\t' + str(HealthStdev) + '\t' + str(HealthSkew) + '\t' + str(HealthKurt)
                
                # Add this line to the output string
                output += this_line + '\n'
    
    # Write the output to disk
    with open(output_name, 'w') as f:
        f.write(output)
        f.close()
    t1 = time()
        
    # Describe the specification used, printing to screen
    print('Wrote conditional distributions of latent health to ' + output_name + ' in ' + mystr(t1-t0) + ' seconds.')
    print('Latent health is conditioned on up to ' + str(T) + ' observations of SRHS from the ' + source_name + '.')
    print('The process is based on the parameters in the specification called ' + spec_name + '.')
    print('It discretizes latent health with ' + str(x_count_cond) + ' nodes equally spaced between ' + str(x_min) + ' and ' + str(x_max) + '.')
    print('There are ' + str(age_count_A) + ' ages from ' + str(age_min) + ' to ' + str(age_max) + ' and ' + str(report_type_count) + ' reporting types.')
    for k in range(report_type_count):
        this_line = 'Reporting type ' + str(k+1) + ' ('
        this_line += "{:.2%}".format(my_dict['TypePrbs'][k])
        this_line += ') has a reporting error standard deviation of '
        this_line += mystr(my_dict['ReportStds'][k]) + '.'
        print(this_line)
                
                