#Four important input file of vasp files.
#POTCAR POSCAR INCAR KPOINT

"""
from VASP I/O files of graphene primitive cell with strain -2%, -1% 0, 1% 2%,
read all required information and extract the final energy for each calculation.
To determine whether the structure has reached its required accuracy.
"""

import pymatgen as mg

#from pymatgen.io.vasp.inputs import Poscar, Incar, Kpoints, Potcar

from pymatgen.io.vasp.outputs import Vasprun

import os

dirname='./strain/strain/'

vaspname=[]
vaspenergy=[]
for file in os.listdir(dirname):
	vasp_name='strain='+str(file)
	run_path=dirname+str(file)+'/vasprun.xml'
	vasp_run=Vasprun(run_path)
	log_path=dirname+str(file)+'/log'
	openfile=open(log_path,'rt')
	read_text=openfile.read()
	#check whether the material has reached its required accuracy
	if 'reached required accuracy' in read_text:
		vaspname.append(vasp_name)
		vaspenergy.append(vasp_run.final_energy)

#print the results to the screen
for idx in range(len(vaspname)):
	print(str(vaspname[idx])+' has final energy: '+str(vaspenergy[idx]))


#write the results to a csv file
opencsv=open('final_energy_with_strain.csv','wt')
opencsv.write('strain,final_energy\n')
if len(vaspname)==len(vaspenergy):
	for idx in range(len(vaspname)):
		writestring=str(vaspname[idx])+','+str(vaspenergy[idx])+'\n'
		opencsv.write(writestring)
	opencsv.close()
