function run_makeLoadsTemps(InputFile)

addpath('/radforce/mlp6/fem/trunk/field/');

%dynaFiles = dir('dyna*.mat');
dynaFiles = dir('dyna-I-f9*.mat');
for i=1:length(dynaFiles),
    InputFile = dynaFiles(i).name;
    makeLoadsTemps(InputFile,'dyna-I-f7.00-F2.0-FD0.010-a1.3.mat',100,100,2.0,0.01^3,'q',1);
end;
