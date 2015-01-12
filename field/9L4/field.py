# Run sims of the 9L4 that have different stiffnesses, focal depths and attenuations (cervix).

__author__ = 'Mark Palmeri'
__date__ = '2012-12-13'

import os

# define some stuff
Freq = [4.00,5.00,6.00,7.00]
Fnum = [1.0,1.5,2.0]
FD = [0.015,0.020,0.025,0.030]
alpha = [0.5,0.9,1.3,1.7,2.0]

root = '/radforce/fem/cervix/field/9L4'

for i in range(len(Freq)):
    for j in range(len(Fnum)):
        for k in range(len(FD)):
            for l in range(len(alpha)):
                datafile = '%s/dyna-I-f%.2f-F%.1f-FD%.3f-a%.1f.mat' % (root,Freq[i],Fnum[j],FD[k],alpha[l])
                if not os.path.exists(datafile):
                    SGE_FILENAME = 'field_9l4_f%.2f-F%.1f-FD%.3f-a%.1f.sge' % (Freq[i],Fnum[j],FD[k],alpha[l])
                    SGE_FILE = open('%s' % SGE_FILENAME,'w')
                    SGE_FILE.write('#$ -l mem_free=1.5G\n')
                    SGE_FILE.write('import os\n')
                    SGE_FILE.write('os.system("date")\n')
                    SGE_FILE.write('os.system("hostname")\n')
                    SGE_FILE.write('os.environ.pop("DISPLAY")\n')
                    #SGE_FILE.write('os.environ.pop("MATLAB")\n')
                    SGE_FILE.write('os.system("/usr/local/matlab2010b/bin/matlab -nodesktop -nosplash -r \'run(%.1f,%.3f,%.2f,%.1f)\'")\n' % (Fnum[j],FD[k],Freq[i],alpha[l]))
                    SGE_FILE.close()

                    os.system('qsub %s' % (SGE_FILENAME))
                else:
                    print('%s ALREADY EXISTS!!' % datafile)
