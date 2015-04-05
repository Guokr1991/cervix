function genLoads(FNUM, FOCDEPTH, FREQ, ALPHA)
% function genLoads(FNUM, FOCDEPTH, FREQ, ALPHA)
%
% Call FEM/field Field II functions to generate ARF loads.
%
% Mark Palmeri
% mlp6@duke.edu
% 2015-04-05

FDmm = FOCDEPTH * 1000;

nodeFile = sprintf('../../mesh/nodes.dyn', FDmm);

inputIntensityFile = field2dyna(nodeFile, ALPHA, FNUM, [0 0 FOCDEPTH], FREQ, ...
                                'l94', 'gaussian');

normIntensityFile = 'dyna-I-f6.15-F1.5-FD0.050-a0.50.mat';

makeLoadsTemps(inputIntensityFile, normIntensityFile, 1000, 500, 2.0, 0.01^3, 'q', 1);

% generate VTU files for paraview
system(sprintf('python ~/git/fem/mesh/create_pointloads_vtk.py --loadfile PointLoads-f6.15-F%.1f-FD0.0%i-a0.50.dyn --loadout nodeLoadsFoc%immF%.1f', FNUM, FDmm, FDmm, FNUM));

quit
