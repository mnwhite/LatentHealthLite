# LatentHealthLite
 Lightweight software archive for "Self-Reported Health Status and Latent Health Dynamics"

## Basics

This repository contains a few small scripts that allow other researchers to quickly and
easily incorporate the results of the paper into their own work. The code can be downloaded
in a zip file by clicking the green **Code** button on the main repository page, then
unpacked into any working directory. There are two primary use cases for the code provided:

1. To construct a discretized latent health process that can be imported into a structural
model, possibly replacing SRHS as the representation of health.

2. To make a "filtration dataset" that can be merged into panel data, providing the model's
prediction of a respondent's latent health distribution and reporting type, conditional on
their sex, age, and reported sequence of SRHS.

Both of these tasks can be accomplished with the Python3 script MakeLatentHealthFile.py,
which can be run from the command line or from within a Python environment (with slight
edits to the code). The command line syntax for the file is given by:

    python MakeLatentHealthFile.py worktype spec_name output_name node_count health_min health_max Z_to_cond

The ordered inputs for this script are:

worktype    : The type of output to be produced, must be "filter" or "process".

spec_name   : The name of the specification file, with no .py file extension.

output_name : The name of the file to which to write the latent health process.

node_count  : The integer number of nodes in the latent health discretization.

health_min  : The minimum value of latent health in the discretization.

health_max  : The maximum value of latent health in the discretization.

Z_to_cond   : The number of survey waves on which to condition latent health (filter only).

Each section below provides instructions for common research tasks. A list of all provided
parameter specifications (in the /ParameterSpecs directory) follows further below, along
with formatting information for such files.


## Making a Discretized Latent Health Process

To construct a discretized latent health process for use in a structural model,
MakeLatentHealthFile.py should be run with "process" as its first argument (no quotes).

As an example, a coarse discretization based on the main parameter estimates, with 40 nodes
on the interval of latent health spanned by [-6, 22], can be created by:
    
    python MakeLatentHealthFile.py process TwoStudyAllOver23HeteroParams MainResults.dat 40 -6 22

A very coarse discretization using only 15 latent health nodes spanning [-6, 22], based on
parameters re-estimated with this very coarse grid, which are not reported in the paper
nor appendix, can be created by:

    python MakeLatentHealthFile.py process TwoStudyAllTinyParams TinyResults.dat 15 -6 22

Because those choices are what were actually used for the "tiny" estimation, that
command is functionally identical when the last three arguments are omitted entirely:

    python MakeLatentHealthFile.py process TwoStudyAllTinyParams TinyResults.dat

The files produced by the "process" script are binary data files and not human readable.


## Importing a Discretized Latent Health Process

Once a discretized latent health process file has been created with MakeLatentHealthFile.py,
it can be imported into the working environment for a structural model by reading the binary
data file. Code for this task has been provided for both Python3 (LoadLatentHealthProcess.py)
and Matlab (LoadLatentHealthProcess.m). In either case, the loading script should be put
in the project directory, along with the binary data file. The variable discretization_file
should be set to name the file to be read into memory; this is the only adjustment needed.

The following objects will be created, as numpy arrays or Matlab arrays:

node_count (int) : Number of nodes in the discretized grid of latent health levels.

age_count (int) : Number of discrete ages loaded in the data.

report_count (int) : Number of different SRHS reporting categories (e.g. poor, fair, good, etc).

type_count (int) : Number of reporting types in this specification. Type determines only the
standard deviation of SRHS reporting errors.

HealthGrid (array) : Array of size (node_count,) with the discretized latent health grid.

LivPrbArray (array) : Array of shape (2, age_count, node_count) with survival probabilities
by sex-age-health.

TransPrbArray (array) : Array of shape (2, age_count, node_count, node_count) with
transition probabilities among discretized health states by age-sex-health_now-health_next.

ReportPrbArray (array) : Array of shape (type_count, report_count, node_count) with the
probability of reporting each categorical SRHS by latent health.

InitialHealthDstn (array) : Array of shape (2, age_count, nodecount) with the unconditional
distribution of discretized latent health (conditional on survival) by age-sex.

In Python, these variables and arrays can be imported from LoadLatentHealthProcess.py. In
Matlab script, they are declared as global variables and can be accessed as such. The
user can also remove the global declaration and simply run LoadLatentHealthProcess.m from
within their project code.


## Making a Latent Health Filtration Dataset

To construct a dataset that can be merged into panel SRHS data to add the model's prection
of latent health and reporting type for each respondent, MakeLatentHealthFile.py should be
run with "filter" as its first argument (no quotes).

For example, a tab-delimited text file with summary statistics for the distribution of
latent health for any combination of sex, age, and observed sequence of SRHS (up to three
waves long), based on the main specification estimated in the paper, can be made by:
    
    python MakeLatentHealthFile.py filter TwoStudyAllOver23HeteroParams ConditionalHealthDstn.txt 120 -12 28 3

As the file is human-readable, its contents can be quickly verified. The number of waves
to "look back" can be set at any whole number, but the produced dataset grows exponentially
with the number of waves (as there are (H+1)^Z different SRHS sequences possible for each
age-sex pair). Missing SRHS observations are marked with a -1 in the produced file, and
"missing" observations includes the case where a respondent was not in the survey at all,
or not an appropriate age for inclusion in the model.

Lookback waves are interpreted from the perspective of the survey structure, so (e.g.) the
main specification (using the HRS and PSID) conditions on SRHS *two* periods back each time,
as the model was estimated at an annual frequency on biannual data.


## Merging a Latent Health Filtration Dataset

Example Stata code for merging a "filtration dataset" into panel data is provided in
MergeLatentHealthFilter.do. Instructions for (lightly) editing that script and preparing
the data to be merged are provided in the script and are mostly obvious for anyone who
is somewhat familiar with Stata. Generally: The dataset to be merged should have variables
called sex (0 female, 1 male), age (in years), xt, xtm1, xtm2... The data file to be merged
should be pre-sorted by sex age xtm2 xtm1 xt. Make sure that sex, age, and the xt variables
are defined for all respondents in the data to be merged-- no missing values. If SRHS values 
are missing for some respondents, code those missing values as -1. This includes respondents
who have not yet been in the data for T lookback waves-- their SRHS is "missing"because it
was never asked.


## List of Parameter Specifications

The directory /ParameterSpecs contains many parameter specification files. Each file represents
a version of the latent health model that was estimated for the project. Not all of the
specifications are reported in the paper or online appendix. A brief description of each
specification is as follows:

TwoStudyAllOver23HeteroParams.py : Both sexes specification reported in the paper: HRS & PSID.

TwoStudyMenOver23HeteroParams.py : Men-only specification reported in the paper: HRS & PSID.

TwoStudyWomenver23HeteroParams.py : Women-only specification reported in the paper: HRS & PSID.

TwoStudyAllOver23aParams.py : Both sexes specification reported in appendix: no heteroskedasticity nor skewed health shocks.

TwoStudyMenOver23aParams.py : Men-only specification reported in appendix: no heteroskedasticity nor skewed health shocks.

TwoStudyWomenver23aParams.py : Women-only specification reported in appendix: no heteroskedasticity nor skewed health shocks.

TwoStudyAllTinyParams.py : Very coarse latent health grid specification (N=15), mentioned in section 5 but not reported.

HRSallOver50HeteroParams.py : Both sexes, HRS only, heteroskedastic reporting errors and skewed health shocks.

HRSmenOver50HeteroParams.py : Men-only, HRS only, heteroskedastic reporting errors and skewed health shocks.

HRSwomenOver50HeteroParams.py : Women-only, HRS only, heteroskedastic reporting errors and skewed health shocks.

HRSmenOver50aParams.py : Men-only, HRS only, no heteroskedasticity and standard normal health shocks.

HRSwomenOver50aParams.py : Women-only, HRS only, no heteroskedasticity and standard normal health shocks.

PSIDallOver23HeteroParams.py : Both sexes, PSID only, heteroskedastic reporting errors and skewed health shocks.

PSIDmenOver23HeteroParams.py : Men-only, PSID only, heteroskedastic reporting errors and skewed health shocks.

PSIDwomenOver23HeteroParams.py : Women-only, PSID only, heteroskedastic reporting errors and skewed health shocks.

PSIDmenOver23aParams.py : Men-only, PSID only, no heteroskedasticity and standard normal health shocks.

PSIDwomenOver23aParams.py : Women-only, PSID only, no heteroskedasticity and standard normal health shocks.

MEPSallOver18HeteroParams.py : Both sexes, MEPS only, heteroskedastic reporting errors and skewed health shocks.

MEPSmenOver18HeteroParams.py : Men-only, MEPS only, heteroskedastic reporting errors and skewed health shocks.

MEPSwomenOver18HeteroParams.py : Women-only, MEPS only, heteroskedastic reporting errors and skewed health shocks.

MEPSmenOver18Params.py : Men-only, MEPS only, no heteroskedasticity and standard normal health shocks.

MEPSwomenOver18Params.py : Women-only, MEPS only, no heteroskedasticity and standard normal health shocks.


## Format of a Parameter Specification File

