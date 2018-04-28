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
import wget
import pprint

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
        'task_id',
        'material_id'
    ]
}
r = requests.post('https://materialsproject.org/rest/v2/query',
                 headers={'X-API-KEY': 'YOUR_API_KEY_HERE'},
                 data={k: json.dumps(v) for k,v in data.items()})
response_content = r.json() # a dict
list_res=response_content['response']
print(len(list_res))
#print(list_res)

#put my API key from https://materialsproject.org/ in the mpr
API_key='YOUR_API_KEY_HERE'
mpr = MPRester(API_key)

#get the material id and store them in a list
id_list=[]
for ind in range(len(list_res)):
    id_list.append(list_res[ind]['material_id'])

#get updated_id_list
# updated_id_list=[]
# for inde in id_list:
#     updated_ind=mpr.get_materials_id_from_task_id(inde)
#     updated_id_list.append(updated_ind)
    
#print(id_list)
#print(updated_id_list)
#print(id_list)

# test_id_list=id_list[:10]
# print(test_id_list)


#delete some outliers
#the_index=id_list.index('mp-1370')
#id_list.pop(the_index)
print(id_list)
# sec_index=id_list.index('mp-27532')
# sec_id_list=id_list[sec_index+1:]

# trd_index=sec_id_list.index('mp-29834')
# trd_id_list=sec_id_list[trd_index+1:]

# four_index=trd_id_list.index('mp-637251')
# four_id_list=trd_id_list[four_index+1:]

# fif_index=four_id_list.index('mp-4047')
# fif_id_list=four_id_list[fif_index+1:]

# six_index=fif_id_list.index('mp-18928')
# six_id_list=fif_id_list[six_index+1:]

# sev_index=six_id_list.index('mp-29549')
# sev_id_list=six_id_list[sev_index+1:]

# eig_index=sev_id_list.index('mp-768813')
# eig_id_list=sev_id_list[eig_index+1:]

# nin_index=eig_id_list.index('mp-771255')
# nin_id_list=eig_id_list[nin_index+1:]

# ten_index=nin_id_list.index('mvc-13163')
# ten_id_list=nin_id_list[ten_index+1:]

# ele_index=ten_id_list.index('mvc-6876')
# ele_id_list=ten_id_list[ele_index+1:]

# #list=['mvc-16173', 'mvc-14977', 'mvc-3925']
# twe_id_list=ele_id_list[3:]

# thr_index=twe_id_list.index('mp-567043')
# thr_id_list=twe_id_list[thr_index+1:]

# fou_index=thr_id_list.index('mp-707304')
# fou_id_list=thr_id_list[fou_index+1:]

# #mp-559237
# fiften_id_list=fou_id_list[2:]

# sixt_index=fiften_id_list.index('mp-555696')
# sixt_id_list=fiften_id_list[sixt_index+1:]

# sevt_index=sixt_id_list.index('mp-680314')
# sevt_id_list=sixt_id_list[sevt_index+1:]

# eigt_index=sevt_id_list.index('mp-861606')
# eigt_id_list=sevt_id_list[eigt_index+1:]

# nint_index=eig_id_list.index('mp-866314')
# nin_id_list=eigt_id_list[nint_index+1:]

# twent_index=nin_id_list.index('mp-556013')
# twent_id_list=nin_id_list[twent_index+1:]

# twe1_index=twent_id_list.index('mp-556177')
# twe1_id_list=twent_id_list[twe1_index+1:]

# ind_22=twe1_id_list.index('mp-680437')
# id_list_22=twe1_id_list[ind_22+1:]

# ind_23=id_list_22.index('mp-19203')
# id_list_23=id_list_22[ind_23+1:]

# ind_24=id_list_23.index('mp-861513')
# id_list_24=id_list_23[ind_24+1:]

# ind_25=id_list_24.index('mp-16972')
# id_list_25=id_list_24[ind_25+1:]

# ind_26=id_list_25.index('mp-558426')
# id_list_26=id_list_25[ind_26+1:]

# ind_27=id_list_26.index('mp-1021497')
# id_list_27=id_list_26[ind_27+1:]


# ind_28=id_list_27.index('mp-542686')
# id_list_28=id_list_27[ind_28+1:]


# ind_29=id_list_28.index('mp-6532')
# id_list_29=id_list_28[ind_29+1:]


# ind_30=id_list_29.index('mp-985697')
# id_list_30=id_list_29[ind_30+1:]

# ind_31=id_list_30.index('mp-867322')
# id_list_31=id_list_30[ind_31+1:]

# ind_32=id_list_31.index('mp-867929')
# id_list_32=id_list_31[ind_32+1:]

# ind_33=id_list_32.index('mp-560618')
# id_list_33=id_list_32[ind_33+1:]

# ind_34=id_list_33.index('mvc-9528')
# id_list_34=id_list_33[ind_34+1:]

# ind_35=id_list_34.index('mp-705177')
# id_list_35=id_list_34[ind_35+1:]

# ind_36=id_list_35.index('mp-560564')
# id_list_36=id_list_35[ind_36+1:]

# ind_37=id_list_36.index('mp-23149')
# id_list_37=id_list_36[ind_37+1:]

# ind_38=id_list_37.index('mp-850230')
# id_list_38=id_list_37[ind_38+1:]

# ind_39=id_list_38.index('mp-25024')
# id_list_39=id_list_38[ind_39+1:]

# ind_40=id_list_39.index('mp-705484')
# id_list_40=id_list_39[ind_40+1:]

# ind_41=id_list_40.index('mp-866662')
# id_list_41=id_list_40[ind_41+1:]

# ind_42=id_list_41.index('mp-684467')
# id_list_42=id_list_41[ind_42+1:]

# ind_43=id_list_42.index('mp-706243')
# id_list_43=id_list_42[ind_43+1:]

# ind_44=id_list_43.index('mp-25022')
# id_list_44=id_list_43[ind_44+1:]

# ind_45=id_list_44.index('mp-565677')
# id_list_45=id_list_44[ind_45+1:]

# ind_46=id_list_45.index('mp-23655')
# id_list_46=id_list_45[ind_46+1:]

# ind_47=id_list_46.index('mp-40226')
# id_list_47=id_list_46[ind_47+1:]

# ind_48=id_list_47.index('mp-744746')
# id_list_48=id_list_47[ind_48+1:]

# ind_49=id_list_48.index('mp-772986')
# id_list_49=id_list_48[ind_49+1:]

# ind_50=id_list_49.index('mp-605935')
# id_list_50=id_list_49[ind_50+1:]

# ind_51=id_list_50.index('mp-744654')
# id_list_51=id_list_50[ind_51+1:]

# ind_52=id_list_51.index('mp-704630')
# id_list_52=id_list_51[ind_52+1:]

# ind_53=id_list_52.index('mp-534870')
# id_list_53=id_list_52[ind_53+1:]

# ind_54=id_list_53.index('mp-706336')
# id_list_54=id_list_53[ind_54+1:]

# ind_55=id_list_54.index('mp-24308')
# id_list_55=id_list_54[ind_55+1:]

# ind_56=id_list_55.index('mp-721011')
# id_list_56=id_list_55[ind_56+1:]

# ind_57=id_list_56.index('mp-542926')
# id_list_57=id_list_56[ind_57+1:]

# ind_58=id_list_57.index('mp-720410')
# id_list_58=id_list_57[ind_58+1:]
new_id_list=['mp-641919', 'mp-6903']
print(len(new_id_list))

#define a function that gets document from MP
def get_doc_from_MP(mp_id):
    """
    the function takes material_id as input and returns the generated document from MP
    """
    apr=mpr.get_doc(mp_id)
    return apr

#define a function that generates matrix
def generate_matrix(doc):
    """
    the function takes the return document(apr) from the above function
    as input, and returns the needed matrix
    """
    bv_stru=doc['bv_structure']
    lattice=bv_stru['lattice']
    l_matrix=lattice['matrix']
    #manipulate over lattice matrix
    mat_list=[]
    for list_m in l_matrix:
        str_null=''
        for items in list_m:
            items=Decimal(items).quantize(Decimal('0.000000'))
            str_null=str_null+str(items)+' '
        str_null=str_null[:len(str_null)-1]
        mat_list.append(str_null)
    return mat_list

#define a function that gets the title of POSCAR file
def POSCAR_title(doc):
    """
    the function takes the return document(apr) from the above function
    as input, and returns the needed title
    """
    com_for=doc['snl']
    formu=com_for['formula']
    return formu

#define a function that gets the unit_cell_formula
def generate_cell_formula(doc):
    """
    the function takes the return document(apr) from the above function
    as input, and returns the needed unit cell formula
    """
    cell_for=doc['unit_cell_formula']
    return cell_for

#define a function that gets dos document from MP
def generate_dos_str(material_id):
    """
    the function takes material_id as input and returns a string
    file that is transformed from a dos file
    and extract the needed content from the string
    """
    out=mpr.get_dos_by_material_id(material_id)
    str_output=str(out)
    split_dos=str_output.split('\n')
    #extract the needed content
    for line in split_dos:
        if line[0]=='-':
            splitting_index=split_dos.index(line)
            break
    needed_dos=split_dos[splitting_index+1:]
    return needed_dos

#define a function to transform the format into a proper format
#for a POSCAR file
def dos_into_string(needed_dos):
    """
    the function takes the returned value of the above function as input 
    and returns a string that is the correct format for POSCAR
    """
    revise_dos=[]
    for strings in needed_dos:
        new_string=strings[11:]
        new_string=new_string.split(' ')
        new_string_1=[]
        for strs in new_string:
            if strs!='':
                new_string_1.append(strs)
        empty_value=''
        for value in new_string_1:
            changed_value=Decimal(value).quantize(Decimal('.000001'))
            empty_value=empty_value+str(changed_value)+' '
        new_string_2=empty_value[:len(empty_value)-1]
        if strings[6]==' ':
            string_element=strings[5]
        elif strings[7]==' ':
            string_element=strings[5:7]
        elif strings[8]==' ':
            string_element=strings[5:8]
        else:
            string_element=strings[5:9]
        new_string_2=new_string_2+'  '+string_element
        new_string_2=new_string_2.replace('  ',' ')
        revise_dos.append(new_string_2)
    return revise_dos

#define a function that loops over the revise_dos list to get an ordered_element_list
def generate_ordered_list(revise_dos):
    """
    the function takes the returned value(revise_dos) string as input,
    and then generate a ordered list of elements. The ordered list of 
    elements is prepared for later processing.
    """
    ordered_list=[]
    for lines in revise_dos:
        split_lines=lines.split(' ')
        element=split_lines[-1]
        if element not in ordered_list:
            ordered_list.append(element)
    return ordered_list

#define a function that gets the ordered string of 
#elements based on the ordered_list
def generate_ordered_elements(revise_dos,ordered_list):
    """
    the function takes the revise_dos and ordered_list as input,
    and generates a list of elements that are in the correct order
    the POSCAR file needs
    """
    my_ordered_elements=''
    for key in ordered_list:
        my_ordered_elements=my_ordered_elements+key+' '
    my_ordered_elements=my_ordered_elements[:len(my_ordered_elements)-1]
    return my_ordered_elements

#define a function that gets the ordered string of 
#numbers based on the ordered_list
def generate_ordered_numbers(revise_dos,ordered_list,cell_for):
    """
    the function takes the revise_dos and ordered_list and the 
    cell_for as input, and generates a list of numbers that are 
    in the correct order the POSCAR file needs
    """
    my_ordered_numbers=''
    for key in ordered_list:
        my_ordered_numbers=my_ordered_numbers+str(int(cell_for[key]))+' '
    my_ordered_numbers=my_ordered_numbers[:len(my_ordered_numbers)-1]
    return my_ordered_numbers

#define a function that writes out all the needed strings into a file
def generate_POSCAR(formu,mat_list,my_ordered_elements,my_ordered_numbers,revise_dos):
    """
    The function takes five output from the above functions and 
    write out a POSCAR file in the required format to a desitination
    directory. And this function does not have a return.
    """
    out_name='POSCAR.'+formu
    out_name='POSCAR_files/'+out_name.replace(' ','')
    openfile = open(out_name,'wt')
    openfile.write(formu+'\n')
    openfile.write(str(1.0)+'\n')
    for str_lines in mat_list:
        openfile.write(str_lines+'\n')
    openfile.write(my_ordered_elements+'\n')
    openfile.write(my_ordered_numbers+'\n')
    openfile.write('direct'+'\n')
    for string_lines in revise_dos:
        openfile.write(string_lines+'\n')
    openfile.close()

#define a function to combine all the above steps together
#and then writes out the file to a desinated directory.
def generate_file(material_id):
    """
    the function takes material_id as input, and applies
    the above self-defined functions, to generate the needed
    POSCAR file for each material_id.
    """
    apr=get_doc_from_MP(material_id)
    mat_list=generate_matrix(apr)
    formu=POSCAR_title(apr)
    cell_for=generate_cell_formula(apr)
    needed_dos=generate_dos_str(material_id)
    revise_dos=dos_into_string(needed_dos)
    ordered_list=generate_ordered_list(revise_dos)
    my_ordered_elements=generate_ordered_elements(revise_dos,ordered_list)
    my_ordered_numbers=generate_ordered_numbers(revise_dos,ordered_list,cell_for)
    generate_POSCAR(formu,mat_list,my_ordered_elements,my_ordered_numbers,revise_dos)

#finally, write a loop to extract all the needed files
print("running----------------------------------")
for material_id in new_id_list:
    generate_file(material_id)
    print(material_id)
