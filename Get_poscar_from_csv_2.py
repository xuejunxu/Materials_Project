"""
This script extracts the POSCAR files (containing atomic structure information) 
for materials from Material Projects https://materialsproject.org/, by material
ids, and the material ids are extracted from csv files
"""

#first load needed packages

from pymatgen import MPRester

import pandas as pd

material_data = pd.read_csv("Your file name here") #change filename here
material_data=pd.DataFrame(material_data)

mat_id=material_data['material_id']
mid_list=list(mat_id)
print(mid_list)

#put my API key from https://materialsproject.org/ in the mpr
API_key="YOUR_APT_KEY"
mpr = MPRester(API_key)


def get_poscar_file(material_id):
    structure=mpr.get_structure_by_material_id(material_id)
    file_name='POS_files/POSCAR.'+material_id
    pos_str=structure.to(fmt='poscar')
    openfile=open(file_name,'wt')
    openfile.write(pos_str)
    openfile.close()


print('running----------------------------')
for material_id in mid_list:
    get_poscar_file(material_id)
    print(material_id)