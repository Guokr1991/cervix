function run(FNUM,FOCDEPTH,FREQ,ALPHA)
addpath('/home/mlp6/fem/trunk/field/');
field2dyna('/radforce/fem/cervix/mesh/nodes.dyn',ALPHA,FNUM,[0 0 FOCDEPTH],FREQ,'acunav128_fullap','gaussian');
%makeLoadsTemps(,'dyna-I-f2.00-F2.5-FD0.05-a0.55.mat',650,182,2.0,0.02^3,'q',1);
