#$ -t 1-240

import os
import glob

SGE_TASK_ID = int(os.environ['SGE_TASK_ID'])

os.system('date')
os.system('hostname')

InputFiles = glob.glob('dyna*.mat')
print(InputFiles[SGE_TASK_ID])
os.system('matlab -nodesktop -nosplash -r "run_makeLoadsTemps(\'%s\')"' % InputFiles[SGE_TASK_ID])
