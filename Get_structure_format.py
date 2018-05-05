#first load needed packages

"""
This script extracts the POSCAR files (containing atomic structure information) 
for materials that contain the element "Si", 
have a "band gap" > 1 eV, and "Energy Above Hull / Atom" = 0 eV
from Material Projects https://materialsproject.org/
"""

import re
import json
import requests
import pprint

from math import sin, cos, radians

from pymatgen import MPRester

from decimal import Decimal

import io


#first to query needed data from Materials Project website
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

r = requests.post('https://materialsproject.org/rest/v2/query',
                 headers={'X-API-KEY': 'YOUR_KEY_HERE'},
                 data={k: json.dumps(v) for k,v in data.items()})
response_content = r.json() # a dict
list_res=response_content['response']

#put my API key from https://materialsproject.org/ in the mpr
API_key="YOUR_KEY_HERE"
mpr = MPRester(API_key)

#get the material id and store them in a list
id_list=[]
for ind in range(len(list_res)):
    id_list.append(list_res[ind]['material_id'])

#define a function to generate a matrix that shows 
#the lattice structure in a Cartesian coordinate
def get_matrix_by_mid(material_id):
    doc_of_material=mpr.get_doc(material_id)
    cif_of_material=doc_of_material['cif']
    split_cif=cif_of_material.split('\n')
    
    length_list=[]
    angle_list=[]

    for item in split_cif:
        if item[:12]=='_cell_length':
            length_list.append(item)
        elif item[:11]=='_cell_angle':
            angle_list.append(item)
    
    #assigning values to length a,b,c and and angle alpha, beta and gamma
    space_index_a=length_list[0].index('   ')
    len_a=float(length_list[0][space_index_a+3:])
    #print(len_a)
    space_index_b=length_list[1].index('   ')
    len_b=float(length_list[1][space_index_b+3:])
    #print(len_b)
    space_index_c=length_list[2].index('   ')
    len_c=float(length_list[2][space_index_c+3:])
    #print(len_c)
    space_index_alpha=angle_list[0].index('   ')
    alpha=float(angle_list[0][space_index_alpha+3:])
    alpha=radians(alpha)
    #print(alpha)
    space_index_beta=angle_list[1].index('   ')
    beta=float(angle_list[1][space_index_beta+3:])
    beta=radians(beta)
    #print(beta)
    space_index_gamma=angle_list[2].index('   ')
    gamma=float(angle_list[2][space_index_gamma+3:])
    gamma=radians(gamma)
    #print(gamma)

    #convert the fractional coordinates to Cartesian coordinates
    #the conversion relationship between two coordinates can refer to
    # https://en.wikipedia.org/wiki/Fractional_coordinates
    omega=len_a*len_b*len_c*(1-(cos(alpha))**2-(cos(beta))**2-(cos(gamma))**2+2*cos(alpha)*cos(beta)*cos(gamma))**0.5
    num_1_1=len_a*sin(beta)
    num_1_1=Decimal(num_1_1).quantize(Decimal('0.000000'))
    num_1_2=Decimal(0).quantize(Decimal('0.000000'))
    num_1_3=len_a*cos(beta)
    num_1_3=Decimal(num_1_3).quantize(Decimal('0.000000'))

    num_2_1=len_b*(cos(gamma)-cos(alpha)*cos(beta))/sin(beta)
    num_2_1=Decimal(num_2_1).quantize(Decimal('0.000000'))
    num_2_2=omega/len_a/len_c/sin(beta)
    num_2_2=Decimal(num_2_2).quantize(Decimal('0.000000'))
    num_2_3=len_b*cos(alpha)
    num_2_3=Decimal(num_2_3).quantize(Decimal('0.000000'))

    num_3_1=Decimal(0).quantize(Decimal('0.000000'))
    num_3_2=Decimal(0).quantize(Decimal('0.000000'))
    num_3_3=Decimal(len_c).quantize(Decimal('0.000000'))

    out_matrix=str(num_1_1)+' '+str(num_1_2)+' '+str(num_1_3)+'\n'\
    +str(num_2_1)+' '+str(num_2_2)+' '+str(num_2_3)+'\n'+str(num_3_1)+\
    ' '+str(num_3_2)+' '+str(num_3_3)
    #return the matrix that uses the Cartesian coordinate
    return out_matrix

def get_POSCAR_title(material_id):
    """
    the function takes the material id as input and returns a string
    of the first line of the POSCAR file
    """
    doc=mpr.get_doc(material_id)
    com_for=doc['snl']
    formu=com_for['formula']
    return formu

def generate_cell_formula(material_id):
    """
    the function takes the return document(apr) from the above function
    as input, and returns the needed unit cell formula
    """
    doc=mpr.get_doc(material_id)
    cell_for=doc['unit_cell_formula']
    return cell_for

#define a function that gets the ordered string of elements
def generate_order_element(cell_for,formu):
    """
    the function takes the revise_dos and ordered_list as input,
    and generates a list of elements that are in the correct order
    the POSCAR file needs
    """
    num_list=['0','1','2','3','4','5','6','7','8','9']
    formu_list=[]
    for char in range(len(formu)):
        formu_list.append(formu[char])
    new_formu_list=[]
    for character in formu_list:
        if character not in num_list:
            new_formu_list.append(character)
    str_element=''
    for string in new_formu_list:
        str_element+=string
    element_list=str_element.split(' ')
    ele_num_list=[]
    for element in element_list:
        ele_num_list.append(cell_for[element])
    ele_num_str=''
    for number in ele_num_list:
        int_num=int(number)
        ele_num_str=ele_num_str+str(int_num)+' '
    ele_num_str=ele_num_str[:-1]
    final_string=str_element+'\n'+ele_num_str
    return final_string

#define a function to return the formatted structure of certain 
#material and the input is material_id
def get_structure_by_mid(material_id,final_string):
    doc_of_material=mpr.get_doc(material_id)
    cif_of_material=doc_of_material['cif']
    split_cif=cif_of_material.split('\n')
    
    if ' _atom_site_occupancy' in split_cif:
        atom_index=split_cif.index(' _atom_site_occupancy')
        atom_struc_list=split_cif[atom_index+1:-1]
    elif '  _atom_site_occupancy' in split_cif:
        atom_index=split_cif.index('  _atom_site_occupancy')
        atom_struc_list=split_cif[atom_index+1:-1]
    
    atom_new_list=[]

    if atom_struc_list[0][0:3]!='   ':
        for stuff in atom_struc_list:
            stuff=stuff[2:]
            split_stf=stuff.split('  ')
            atom_new_list.append(split_stf)
    elif atom_struc_list[0][0:3]=='   ':
        for stuff in atom_struc_list:
            stuff=stuff[3:]
            split_stf=stuff.split('  ')
            atom_new_list.append(split_stf)
    #print(atom_new_list)

    element_list=final_string.split('\n')
    element_list1=element_list[0].split(' ')
    structure_string=''
    for idx1 in range(len(element_list1)):
        for idx2 in range(len(atom_new_list)):
            if atom_new_list[idx2][0]==element_list1[idx1]:
                structure_string=structure_string+str(atom_new_list[idx2][3])+' '+str(atom_new_list[idx2][4])\
                +' '+str(atom_new_list[idx2][5])+' '+str(atom_new_list[idx2][0])+'\n'
    structure_string=structure_string[:-1]
    return structure_string

#define a function that writes out all the needed strings into a file
def generate_POSCAR(formu,out_matrix,final_string,structure_string,material_id):
    """
    The function takes several outputs from the above functions and 
    write out a POSCAR file in the required format to a desitination
    directory. And this function does not have a return.
    """
    out_name='POSCAR.'+material_id+'_'+formu
    out_name='POSCAR_files/'+out_name.replace(' ','')
    print(out_name)
    openfile = open(out_name,'wt')
    openfile.write(formu+'\n')
    openfile.write('1.0'+'\n')
    openfile.write(out_matrix+'\n')
    openfile.write(final_string+'\n')
    openfile.write('direct'+'\n')
    openfile.write(structure_string+'\n')
    openfile.close()

#define a function to combine all the above steps together
#and then writes out the file to a desinated directory.
def generate_file(material_id):
    """
    the function takes material_id as input, and applies
    the above self-defined functions, to generate the needed
    POSCAR file for each material_id.
    """
    formu=get_POSCAR_title(material_id)
    out_matrix=get_matrix_by_mid(material_id)
    cell_for=generate_cell_formula(material_id)
    final_string=generate_order_element(cell_for,formu)
    structure_string=get_structure_by_mid(material_id,final_string)
    generate_POSCAR(formu,out_matrix,final_string,structure_string,material_id)

print("running----------------------------------")
for material_id in id_list:
    generate_file(material_id)
    print(material_id)