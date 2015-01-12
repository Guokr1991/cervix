function run(FNUM,FOCDEPTH,FREQ,ALPHA)
addpath('/radforce/mlp6/fem/field/');
field2dyna('/radforce/fem/cervix/mesh/nodes.asc',ALPHA,FNUM,[0 0 FOCDEPTH],FREQ,'l94','gaussian');
%makeLoadsTemps(,'dyna-I-f2.00-F2.5-FD0.05-a0.55.mat',650,182,2.0,0.02^3,'q',1);
