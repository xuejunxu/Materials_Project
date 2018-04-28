
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

import re
import json
import requests
import pprint

from pymatgen import MPRester

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
                 headers={'X-API-KEY': 'M5T8ghdZsq6oSDOm'},
                 data={k: json.dumps(v) for k,v in data.items()})
response_content = r.json() # a dict
list_res=response_content['response']
print(len(list_res))
#print(list_res)

#get the material id and store them in a list
id_list=[]
for ind in range(len(list_res)):
    id_list.append(list_res[ind]['material_id'])

#define a function to select the POSCAR file
#from the drop-down menu

class dropDown():
    def test_dropDown(matetial_id):
        url = 'https://materialsproject.org/materials/'+matetial_id+'/'
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(2)
        ele_dropDown=driver.find_element_by_css_selector('select.multiselect')
        menu_select=Select(ele_dropDown)
        #option_selected=menu_select.select_by_visible_text('File Formats')
        #print(menu_select)
        option_selected=menu_select.select_by_visible_text('POSCAR')
        print(option_selected)
        #menu_select.click()
        time.sleep(3)
        #dropDownClass = "span4 downloads-dropdown"   
        # dropDownXpath=r"//*[contains(text(),'multiple')]"

        # dropDownElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(dropDownXpath))
        # time.sleep(3)
        # Select(dropDownElement).select_by_visible_text("POSCAR")
        # time.sleep(3)

        driver.find_element_by_id('download-files')
        #button_select=Select(next_button)

        # ele_select=driver.find_element_by_id('download-files')
        # #download_select=Select(ele_select)
        # ele_select.click()
        #submit_button.click()

        #driver.find_element_by_id('download-files').click()
        #next_select=Select(ele_download)
        #next_select.select_by_id('download-files')
        time.sleep(3)
        driver.quit()


for id in id_list:
    dd = dropDown()
    dd.test_dropDown(id)
