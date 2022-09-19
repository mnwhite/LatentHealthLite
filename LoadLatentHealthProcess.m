% This file loads a discretized latent health process that has been saved to disk
% with the script MakeLatentHealthFile.py. For use cases where multiple discre-
% tizations are needed for the same project, the code below can easily be adapted
% into a function that returns the arrays.
% 
% To use, first create a discretized health process with MakeLatentHealthFile.py,
% using the "process" option; see documentation in that file. Make sure the output
% that it created is in the directory for the project of interest, set the filename
% below, and run this file. The following arrays and values will be created, as
% global variables, which can then be imported into the project environment by
% declaring them as globals in another file. Alternatively, simply execute this
% file from within the project environment.
% 
% node_count : int
%     Number of nodes in the discretized grid of latent health levels.
% age_count : int
%     Number of discrete ages loaded in the data.
% report_count : int
%     Number of different SRHS reporting categories (e.g. poor, fair, good, etc).
% type_count : int
%     Number of reporting types in this specification. Type determines only the
%     standard deviation of SRHS reporting errors.
% HealthGrid : array
%     Array of shape (node_count,1) with the discretized latent health grid.
% LivPrbArray : array
%     Array of shape (2, age_count, node_count) with survival probabilities by sex-age-health.
% TransPrbArray : array
%     Array of shape (2, age_count, node_count, node_count) with transition probabilities
%     among discretized health states by age-sex-health_now-health_next.
% ReportPrbArray : array
%     Array of shape (type_count, report_count, node_count) with the probability of reporting
%     each categorical SRHS by latent health.
% InitialHealthDstn : array
%     Array of shape (2, age_count, node_count) with the unconditional distribution
%     of discretized latent health (conditional on survival) by age-sex.
global node_count age_count report_count type_count HealthGrid LivPrbArray TransPrbArray ReportPrbArray InitialHealthDstn;

% Name the file to be loaded here
discretization_file = 'MainResults.dat';

% Open the file and unpack dimension sizes
myfile = fopen(discretization_file);
node_count = fread(myfile,1);
age_count = fread(myfile,1);
report_count = fread(myfile,1);
type_count = fread(myfile,1);

% Initialize the arrays to be read from file
HealthGrid = zeros(node_count,1);
LivPrbArray = zeros(2, age_count, node_count);
TransPrbArray = zeros(2, age_count, node_count, node_count);
ReportPrbArray = zeros(type_count, report_count, node_count);
InitialHealthDstn = zeros(2, age_count, node_count);

% Read survival probabilities one by one from the file
for h = 1:node_count
    temp = fread(myfile,1,'float64','b');
    HealthGrid(h) = temp;
end

% Read survival probabilities from the file
for s = 1:2
    for j = 1:age_count
        for h = 1:node_count
            temp = fread(myfile,1,'float64','b');
            LivPrbArray(s,j,h) = temp;
        end
    end
end

% Read transition probabilities from the file
for s = 1:2
    for j = 1:age_count
        for i = 1:node_count
            for h = 1:node_count
                temp = fread(myfile,1,'float64','b');
                TransPrbArray(s,j,i,h) = temp;
            end
        end
    end
end

% Read SRHS reporting probabilities from the file
for k = 1:type_count
    for x = 1:report_count
        for h = 1:node_count
            temp = fread(myfile,1,'float64','b');
            ReportPrbArray(k,x,h) = temp;
        end
    end
end

% Read initial health distributions from the file
for s = 1:2
    for j = 1:age_count
        for h = 1:node_count
            temp = fread(myfile,1,'float64','b');
            InitialHealthDstn(s,j,h) = temp;
        end
    end
end

% Close the data file
fclose(myfile);
