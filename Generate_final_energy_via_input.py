#Four important input file of vasp files.
#POTCAR POSCAR INCAR KPOINT

"""
from VASP I/O files of graphene primitive cell with strain -2%, -1% 0, 1% 2%,
read all required information and extract the final energy for each calculation
"""

import pymatgen as mg

#from pymatgen.io.vasp.inputs import Poscar, Incar, Kpoints, Potcar

from pymatgen.io.vasp.outputs import Vasprun

import os

vasp_1=Vasprun('./strain/strain/_1/vasprun.xml')
vasp_2=Vasprun('./strain/strain/_2/vasprun.xml')
vasp0=Vasprun('./strain/strain/0/vasprun.xml')
vasp1=Vasprun('./strain/strain/1/vasprun.xml')
vasp2=Vasprun('./strain/strain/2/vasprun.xml')

print('The final energy under strain -1:',vasp_1.final_energy)
print('The final energy under strain -2:',vasp_2.final_energy)
print('The final energy under strain 0:',vasp0.final_energy)
print('The final energy under strain 1:',vasp1.final_energy)
print('The final energy under strain 2:',vasp2.final_energy)

openfile=open('final_energy_under_different_strain.csv','wt')
openfile.write('strain,final_energy\n')
openfile.write('-1,'+str(vasp_1.final_energy)+'\n')
openfile.write('-2,'+str(vasp_2.final_energy)+'\n')
openfile.write('0,'+str(vasp0.final_energy)+'\n')
openfile.write('1,'+str(vasp1.final_energy)+'\n')
openfile.write('2,'+str(vasp2.final_energy)+'\n')
openfile.close()