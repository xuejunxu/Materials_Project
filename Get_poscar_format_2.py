"""
This script extracts the POSCAR files (containing atomic structure information) 
for materials that contain the element "Si", 
have a "band gap" > 1 eV, and "Energy Above Hull / Atom" = 0 eV
from Material Projects https://materialsproject.org/
"""

from pymatgen import MPRester

import requests

import json

data = {
    'criteria': {
        'elements': {'$in': ['Si']},
        'band_gap': {'$gt': 1},
        'e_above_hull':0
    },
    'properties': [
        'pretty_formula',
        'material_id',
    ]
}
#print(data.items())

r = requests.post('https://materialsproject.org/rest/v2/query',
                 headers={'X-API-KEY': 'YOUR_API_KEY'},
                 data={k: json.dumps(v) for k,v in data.items()})
response_content = r.json() # a dict
#print(response_content)
list_res=response_content['response']
#print(len(list_res))
#print(list_res)

#put my API key from https://materialsproject.org/ in the mpr
API_key="YOUR_API_KEY"
mpr = MPRester(API_key)

#get the material id and store them in a list
id_list=[]
for ind in range(len(list_res)):
    id_list.append(list_res[ind]['material_id'])


def get_poscar_file(material_id):
    structure=mpr.get_structure_by_material_id(material_id)
    file_name='POS_files/POSCAR.'+material_id
    pos_str=structure.to(fmt='poscar')
    openfile=open(file_name,'wt')
    openfile.write(pos_str)
    openfile.close()


print('running----------------------------')
for material_id in id_list:
    get_poscar_file(material_id)
    print(material_id)