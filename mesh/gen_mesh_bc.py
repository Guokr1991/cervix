"""
gen_mesh_bc.py

Generate meshes and PML boundary conditions for cervix SWEI simulations.

Mark Palmeri
mlp6@duke.edu
2015-04-05
"""

import os

FEMGIT = '/home/mlp6/git/fem'

# all units are CGS
nodeSpacing = 0.01
elevCM = 0.6
latCM = 1.5
axialCM = 5.0

os.system('python %s/mesh/GenMesh.py '
          '--xyz -%.1f 0.0 0.0 %.1f -%.1f 0.0 '
          '--numElem %i %i %i' %
          (FEMGIT, elevCM, latCM, axialCM, elevCM/nodeSpacing,
           latCM/nodeSpacing, axialCM/nodeSpacing)
          )

os.system('python %s/mesh/bc.py --pml' % (FEMGIT))
