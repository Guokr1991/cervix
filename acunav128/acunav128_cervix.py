"""
acunav128_cervix.py - setup sge scripts to launch sims on the cluster
"""

__author__ = 'Mark Palmeri'
__date__ = '2012-05-22'

import os

# Run sims of the AcuNav128 that have different stiffnesses, focal depths and attenuations (cervix).

# define some stuff
#run = 'local'
run = 'sge'
YM = [1,5,10,15,20,25]
Freq = [6.00,9.00,12.00]
#Freq = [6.00,7.00,8.00,9.00,10.00,11.00,12.00]
Fnum = [0.1,1.0,2.0]
FD = [0.005,0.006,0.007,0.008,0.009,0.010]
#FD = [0.005,0.006,0.007,0.008,0.009,0.010,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.020]
alpha = [1.3,1.7,2.0]

root = '/radforce/fem/cervix/acunav128'
a128dyn='acunav128_cervix.dyn'
SGE_FILENAME = 'acunav128_cervix.sge'

for i in range(len(Freq)):
    for j in range(len(Fnum)):
        for k in range(len(FD)):
            for l in range(len(alpha)):
                for m in range(len(YM)):

                    field_path = '%s/field/dyna-I-f%.2f-F%.1f-FD%.3f-a%.1f.mat' % (root,Freq[i],Fnum[j],FD[k],alpha[l])

                    if os.path.exists(field_path):

                        sim_path = '%s/E%.1fkPa/%.2fMHz/F%.1f/FD%.3fcm/a%.1f/' % (root,YM[m],Freq[i],Fnum[j],FD[k],alpha[l]) 

                        if not os.path.exists(sim_path):
                            os.makedirs(sim_path)

                        os.chdir(sim_path)
                        print(os.getcwd())

                        terminal_file = 'res_sim.mat'
                        if not os.path.exists(terminal_file):
                            os.system('cp %s/%s .' % (root,a128dyn))
                            os.system("sed -i -e 's/YM/%.1f/' %s" % (YM[m]*10000.0,a128dyn))
                            os.system("sed -i -e 's/FREQ/%.2f/' %s" % (Freq[i],a128dyn))
                            os.system("sed -i -e 's/FNUM/%.1f/' %s" % (Fnum[j],a128dyn))
                            os.system("sed -i -e 's/FOCDEPTH/%.3f/' %s" % (FD[k],a128dyn))
                            os.system("sed -i -e 's/ALPHA/%.1f/' %s" % (alpha[l],a128dyn))
                            os.system("sed -i -e 's/TOFF1/%.1f/' %s" % (400/Freq[i],a128dyn))
                            os.system("sed -i -e 's/TOFF2/%.1f/' %s" % ((400/Freq[i])+1,a128dyn))

                            if run == 'sge':
                                # create sge output file
                                SGE_FILE = open('%s' % SGE_FILENAME,'w')
                                SGE_FILE.write('#$ -l mem_free=6.5G\n')
                                #SGE_FILE.write('#$ -pe smp 4\n')
                                #SGE_FILE.write('#$ -l hostname=clawhammer\n')
                                #SGE_FILE.write('#$ -R y\n')
                                
                                SGE_FILE.write('date\n')
                                SGE_FILE.write('hostname\n')

                                SGE_FILE.write('export DISPLAY=\n')
                                #SGE_FILE.write('ls-dyna-s ncpu=$NSLOTS i=%s\n' % (a128dyn))
                                SGE_FILE.write('ls-dyna-d i=%s\n' % (a128dyn))
                                SGE_FILE.write('rm d3*\n')
                                SGE_FILE.write('gzip -f nodout\n')
                                SGE_FILE.write('python /radforce/mlp6/fem/trunk/post/create_disp_vel_dat.py --disp\n')
                                SGE_FILE.write('python /radforce/mlp6/fem/trunk/post/create_disp_vel_dat.py --vel\n')
                                SGE_FILE.write('python /radforce/mlp6/fem/trunk/post/create_res_sim_mat.py --dynadeck %s --nodedyn /radforce/fem/cervix/mesh/nodes.dyn\n' % (a128dyn))
                                #SGE_FILE.write('if [ -e d3dump01 ]; then /radforce/mlp6/fem/trunk/post/StructPost %s %s/mesh/nodes.asc; fi\n' % (a128dyn,root))
                                #SGE_FILE.write('if [ -e res_sim.mat ]; then rm d3*; fi\n')
                                #SGE_FILE.write('if [ -e res_sim.mat ]; then rm disk8*; fi\n')
                                #SGE_FILE.write('if [ -e disp.dat ]; then xz -f disp.dat; fi\n')
                                SGE_FILE.close()

                                os.system('qsub_bash %s' % (SGE_FILENAME))
                            else:
                                #os.system('ls-dyna-s ncpu=7 i=gaussian.dyn')
                                os.system('if [ -e d3dump01 ]; then /radforce/mlp6/fem/trunk/post/StructPost %s %s/mesh/nodes.asc; fi' % (a128dyn,root))
                                os.system('if [ -e res_sim.mat ]; then rm d3*; fi');
                                os.system('if [ -e res_sim.mat ]; then rm disk8*; fi')
                                os.system('if [ -e disp.dat ]; then xz -f disp.dat; fi')
                        else:
                            print('\t%s already exists' % terminal_file)
