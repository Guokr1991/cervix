function run_makeLoadsTemps(InputFile)

addpath('/home/mlp6/fem/trunk/field/');

%dynaFiles = dir('dyna*.mat');
%for i=1:length(dynaFiles),
%    InputFile = dynaFiles(i).name;
    makeLoadsTemps(InputFile,'dyna-I-f6.00-F2.0-FD0.025-a1.7.mat',100,100,2.0,0.01^3,'q',1);
%end;
