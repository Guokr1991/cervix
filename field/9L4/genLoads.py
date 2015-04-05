"""
genLoads.py

Generate ARF excitation field for different focal depths and attenuations.

Mark Palmeri
mlp6@duke.edu
2015-04-05
"""

import os
import shutil

# define some stuff
Freq = [6.13]
Fnum = [1.5]
FD = [0.030]
alpha = [0.5]

root = '/crabtree/mlp6/cervix/field/9L4'

SGE_TEMPLATE = 'genLoadsSGE.py'

for i in range(len(Freq)):
    for j in range(len(Fnum)):
        for k in range(len(FD)):
            for l in range(len(alpha)):
                datafile = '%s/dyna-I-f%.2f-F%.1f-FD%.3f-a%.2f.mat' % \
                           (root, Freq[i], Fnum[j], FD[k], alpha[l])
                if not os.path.exists(datafile):
                    SGE_FILENAME = datafile.replace('dyna-I-', 'field_')
                    SGE_FILENAME = SGE_FILENAME.replace('.mat', '_SGE.py')
                    print SGE_FILENAME
                    shutil.copy(SGE_TEMPLATE, SGE_FILENAME)
                    PARAM_STRING = '%.1f, %.3f, %.2f, %.2f' % \
                                   (Fnum[j], FD[k], Freq[i], alpha[l])
                    os.system('sed -i -e "s/PARAM_STRING/%s/" %s' %
                              (PARAM_STRING, SGE_FILENAME))
                    os.system('qsub --python %s' % (SGE_FILENAME))
                else:
                    print('%s ALREADY EXISTS!!' % datafile)
