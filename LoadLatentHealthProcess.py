'''
This file loads a discretized latent health process that has been saved to disk
with the script MakeLatentHealthFile.py. For use cases where multiple discre-
tizations are needed for the same project, the code below can easily be adapted
into a function that returns the arrays.

To use, first create a discretized health process with MakeLatentHealthFile.py,
using the "process" option; see documentation in that file. Make sure the output
that it created is in the directory for the project of interest, set the filename
below, and run this file. The following arrays and values will be created, which
can then be imported into the project environment as normal:

node_count : int
    Number of nodes in the discretized grid of latent health levels.
age_count : int
    Number of discrete ages loaded in the data.
report_count : int
    Number of different SRHS reporting categories (e.g. poor, fair, good, etc).
type_count : int
    Number of reporting types in this specification. Type determines only the
    standard deviation of SRHS reporting errors.
HealthGrid : np.array
    Array of size node_count with the discretized latent health grid.
LivPrbArray : np.array
    Array of shape (2, age_count, node_count) with survival probabilities by sex-age-health.
TransPrbArray : np.array
    Array of shape (2, age_count, node_count, node_count) with transition probabilities
    among discretized health states by age-sex-health_now-health_next.
ReportPrbArray : np.array
    Array of shape (type_count, report_count, node_count) with the probability of reporting
    each categorical SRHS by latent health.
InitialHealthDstn : np.array
    Array of shape (2, age_count, nodecount) with the unconditional distribution
    of discretized latent health (conditional on survival) by age-sex.
'''
import numpy as np
from struct import unpack

discretization_file = 'MainResults.dat'

with open(discretization_file, 'rb') as f:
    
    # Write grid sizes to file
    node_count = int.from_bytes(f.read(1), 'little')
    age_count = int.from_bytes(f.read(1), 'little')
    report_count = int.from_bytes(f.read(1), 'little')
    type_count = int.from_bytes(f.read(1), 'little')
    
    # Read the latent health grid from the file
    HealthGrid = np.zeros(node_count)
    for h in range(node_count):
        HealthGrid[h] = unpack('>d', f.read(8))[0]
        
    # Read survival probabilities from the file
    LivPrbArray = np.zeros((2, age_count, node_count))
    for s in range(2):
        for j in range(age_count):
            for h in range(node_count):
                LivPrbArray[s,j,h] = unpack('>d', f.read(8))[0]
                
    # Read transition probabilities from the file
    TransPrbArray = np.zeros((2, age_count, node_count, node_count))
    for s in range(2):
        for j in range(age_count):
            for i in range(node_count):
                for h in range(node_count):
                    TransPrbArray[s,j,i,h] = unpack('>d', f.read(8))[0]
                    
    # Read SRHS reporting probabilities from the file
    ReportPrbArray = np.zeros((type_count, report_count, node_count))
    for k in range(type_count):
        for x in range(report_count):
            for h in range(node_count):
                ReportPrbArray[k,x,h] = unpack('>d', f.read(8))[0]
                
    # Read initial health distributions from the file
    InitialHealthDstn = np.zeros((2, age_count, node_count))
    for s in range(2):
        for j in range(age_count):
            for h in range(node_count):
                InitialHealthDstn[s,j,h] = unpack('>d', f.read(8))[0]
    
    f.close()