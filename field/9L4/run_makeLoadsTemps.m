function run_makeLoadsTemps(InputFile)

addpath('/home/mlp6/fem/trunk/field/');

%dynaFiles = dir('dyna*.mat');
%for i=1:length(dynaFiles),
%    InputFile = dynaFiles(i).name;
    makeLoadsTemps(InputFile,'dyna-I-f6.13-F1.5-FD0.030-a0.50.mat',100,100,2.0,0.01^3,'q',1);
%end;
