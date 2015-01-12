"""
ve_phantom.py - setup sge scripts to launch sims on the cluster

Guassian excitation sims for UWM for soft, VE phantoms and processing phase
velocity information.
"""

__author__ = 'Mark Palmeri'
__date__ = '2014-10-16'

import os

# define some stuff
G0 = [10.0]  # kPa
GI = [1.0]  # kPa
ETA = [0.01, 1.0, 3.0, 6.0, 9.0]
GAUSS = [0.1]  # sigma [cm^-1]
EXC_DUR = range(100, 300, 400)  # us

root = '/pisgah/mlp6/scratch/ve_phantom'
femgit = '/home/mlp6/git/fem'
swdyn = 've_phantom.dyn'
SGE_FILENAME = 've_phantom.sge'

for i in range(len(G0)):
    for ii in range(len(GI)):
        for iii in range(len(ETA)):
            for j in range(len(GAUSS)):
                for k in range(len(EXC_DUR)):

                    # compute BETA from the user-defined variables
                    BETA = (G0[i] * 1e4 - GI[ii] * 1e4) / ETA[iii]

                    # negative BETA is not physically realistic
                    if BETA < 0:
                        break

                    sim_path = '%s/G0%.1fkPa/GI%.1fkPa/BETA%.1f/GAUSS_%.2f_%.2f/EXCDUR_%ius/' % (root, G0[i], GI[ii], BETA, GAUSS[j], GAUSS[j], EXC_DUR[k])

                    if not os.path.exists(sim_path):
                        os.makedirs(sim_path)

                    os.chdir(sim_path)
                    print(os.getcwd())

                    if not os.path.exists('res_sim.mat'):
                        os.system('cp %s/%s .' % (root, swdyn))
                        os.system("sed -i -e 's/G0/%.1f/' %s" %
                                (G0[i] * 10000.0, swdyn))
                        os.system("sed -i -e 's/GI/%.1f/' %s" %
                                (GI[ii] * 10000.0, swdyn))
                        os.system("sed -i -e 's/BETA/%.1f/' %s" %
                                (BETA, swdyn))
                        os.system("sed -i -e 's/TOFF1/%.1f/' %s" %
                                (EXC_DUR[k], swdyn))
                        os.system("sed -i -e 's/TOFF2/%.1f/' %s" %
                                (EXC_DUR[k] + 1, swdyn))

                        # create link to loads.dyn based on Guassian width
                        os.system("ln -fs %s/gauss/gauss_exc_sigma_%.3f_%.3f_"
                                  "1.000_center_0.000_0.000_-3.000_amp_1.000_"
                                  "amp_cut_0.050_qsym.dyn loads.dyn" %
                                  (root, GAUSS[j], GAUSS[j]))
                        os.system("ln -fs %s/mesh/nodes.dyn" % root)
                        os.system("ln -fs %s/mesh/elems.dyn" % root)
                        os.system("ln -fs %s/mesh/bc.dyn" % root)
                        #os.system("cp %s/amanda_exclude ./.exclude" % root)

                        # create sge output file
                        SGE = open('%s' % SGE_FILENAME, 'w')
                        SGE.write('#!/bin/bash\n')
                        SGE.write('#$ -q high.q\n')
                        #SGE.write('#$ -l num_proc=24\n')
                        SGE.write('#$ -l mem_free=1G\n')
                        SGE.write('#$ -pe smp 12\n')

                        SGE.write('date\n')
                        SGE.write('hostname\n')

                        SGE.write('export DISPLAY=\n')
                        SGE.write('ls-dyna-d ncpu=$NSLOTS i=%s\n' % (swdyn))
                        SGE.write('rm d3*\n')
                        SGE.write('python %s/post/create_disp_dat.py '
                                  '--nodout nodout\n' % (femgit))
                        SGE.write('python %s/post/create_res_sim_mat.py '
                                  '--dynadeck %s \n' % (femgit, swdyn))
                        SGE.write('if [ -e disp.dat ]; '
                                  'then rm nodout; fi\n')
                        SGE.write('gzip -v disp.dat\n')
                        SGE.close()

                        os.system('qsub --bash %s' % (SGE_FILENAME))
                    else:
                        print('res_sim.mat already exists')
