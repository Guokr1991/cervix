"""
field.py - setup sge scripts to launch field sims on the cluster
"""

__author__ = 'Mark Palmeri'
__date__ = '2012-05-22'

import os

# Run sims of the AcuNav128 that have different stiffnesses, focal depths and attenuations (cervix).

# define some stuff
#Freq = [6.00,7.00,8.00,9.00,10.00,11.00,12.00]
Freq = [4.00,5.00]
#Fnum = [0.1,1.0,2.0]
Fnum = [0.1]
FD = [0.005,0.006,0.007,0.008,0.009,0.010,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.020]
alpha = [1.3,1.7,2.0]

for i in range(len(Freq)):
    for j in range(len(Fnum)):
        for k in range(len(FD)):
            for l in range(len(alpha)):
                        SGE_FILENAME = 'field_f%.2f-F%.1f-FD%.3f-a%.1f.sge' % (Freq[i],Fnum[j],FD[k],alpha[l])
                        SGE_FILE = open('%s' % SGE_FILENAME,'w')
                        SGE_FILE.write('#!/bin/bash\n')
                        SGE_FILE.write('#$ -S /bin/bash\n')
                        SGE_FILE.write('#$ -o sgetmp\n')
                        SGE_FILE.write('#$ -e sgetmp\n')
                        SGE_FILE.write('#$ -V\n')
                        SGE_FILE.write('#$ -cwd\n')
                        SGE_FILE.write('#$ -l mem_free=1.5G\n')
                        #SGE_FILE.write('#$ -l num_proc=24\n')
                        
                        SGE_FILE.write('date\n')
                        SGE_FILE.write('hostname\n')

                        SGE_FILE.write('export DISPLAY=\n')
                        SGE_FILE.write('export MATLAB=\n')
                        if (Fnum[j] == 0.1): # 0.1 represent the full aperture flag for the acunav128
                            SGE_FILE.write('/usr/local/matlab2010b/bin/matlab -nodesktop -nosplash -r "run_fullap(%.1f,%.3f,%.2f,%.1f)"' % (Fnum[j],FD[k],Freq[i],alpha[l]))
                        else:
                            SGE_FILE.write('/usr/local/matlab2010b/bin/matlab -nodesktop -nosplash -r "run(%.1f,%.3f,%.2f,%.1f)"' % (Fnum[j],FD[k],Freq[i],alpha[l]))
                        SGE_FILE.close()

                        os.system('qsub --bash %s' % (SGE_FILENAME))
