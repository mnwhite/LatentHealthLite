* This script provides example code for merging a latent health "filter file" produced
* by MakeLatentHealthFile.py into panel data. It should be easy for anyone familiar
* with Stata to adapt it for their own purposes.

* Load in the tab-delimited text file; change the filename below as appropriate.
clear all
insheet using ConditionalHealthDstn.txt

* Rename variables for convenience of tying. If you used more or fewer lookback
* periods, add or remove lines here as appropriate.
rename srhst xt
rename srhstm1 xtm1
rename srhstm2 xtm2

* The data should already be sorted when loaded into memory, but it needs to be
* formally sorted in Stata in order to perform a merge.
sort sex age xtm2 xtm1 xt

* Merge a panel dataset into this dataset. The dataset to be merged should have
* variables called sex (0 female, 1 male), age (in years), xt, xtm1, xtm2...
* The data file to be merged should be pre-sorted in the same manner as above.
* Make sure that sex, age, and the xt variables are defined for *all* respondents
* in the data to be merged-- no missing values. If SRHS values are missing for
* some respondents, code those missing values as -1. This includes respondents
* who have not yet been in the data for T lookback waves-- their SRHS is "missing"
* because it was never asked. Change filename below as appropriate.
merge 1:m sex age xtm2 xtm1 xt using DataFileToBeMerged.dta

* After merging, we want to discard any entries from the filter that weren't paired
* with any actual panel data respondents. The tabulation of merge should *only*
* have the value 3 in it-- all observations matched. If there are any values of 2,
* representing "using only" observations, then the dataset to be merged was not
* formatted properly. See comment block above.
drop if _merge == 1
tab _merge
drop _merge

* Reorder the variables so that the latent health distribution appears last.
order typeprob1 typeprob2 typeprob3 healthmean healthstdev healthskew healthkurt, last

* Save the data to disk, choosing your file name below.
save YourNewFileName.dta, replace
