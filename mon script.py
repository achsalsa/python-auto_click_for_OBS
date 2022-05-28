import glob
import json
from pathlib import Path
import re
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
import time
import csv

import numpy as np
import pandas as pd
import os
import requests

# creation du dossier qui vas contenir nos fichiers excel
dateTimeObj = datetime.now()
directory = dateTimeObj.strftime("%d_%b_%Y_%H%M%S%f")
parent_dir="C:\\Users\\JRSZ9280\\Desktop\\Tracking automation"
path = os.path.join(parent_dir, directory)
os.mkdir(path)

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.

dateTimeObj = datetime.now()


mypath = 'C:\\Users\\JRSZ9280\\Desktop\\Tracking automation\\chromedriver'

# activate log web driver

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(desired_capabilities=d)

# opening the CSV file
with open('./ensembles des sites2.csv', mode ='r', encoding="utf8")as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)
  
  # displaying the contents of the CSV file
  linenumber=0
  for lines in csvFile:
    
    dateTimeObj = datetime.now()
    timestampStr2 = dateTimeObj.strftime("%d_%b_%Y_%H_%M%S%f")
    
    linenumber+=1
    print(lines[0])
    driver = webdriver.Chrome(mypath)
    chemin=lines[0]
    chemin=chemin.strip()
    go_for_url="no"
    try:
        r = requests.get(chemin)
        go_for_url="yes"
    except requests.exceptions.ConnectionError:
        pass
    
    if(r.status_code!=404 and r.status_code!=500 and r.status_code!=504  and r.status_code!=503 and go_for_url=="yes"):
        driver.get(chemin)
        print(driver.title)
        
        time.sleep(2)   
        driver.execute_script(open("C:\\Users\\JRSZ9280\\Desktop\\Tracking automation\\auto_tracking_click.js").read())
        driver.execute_script(open("C:\\Users\\JRSZ9280\\Desktop\\Tracking automation\\a_exe_apres_chargement.js").read())
        disctvalList={'type_element':[], 'url_site':[], 'track_nom':[], 'track_zone':[], 'track_cible':[]}
        for entry in driver.get_log('browser'):
            machaine = re.sub("console-api ([0-9]*):([0-9]*) ","",entry['message'])
            machaine = machaine.replace("\\","")
            machaine = machaine[:-1]
            machaine = machaine[1:]
            machaine = machaine[:-1]
            machaine = machaine[1:]
            
            dictval={"type_element" : "" ,"url_site" : "", "track_nom": "", "track_zone": "", "track_cible": ""}
            machaine_list=re.findall(r'"(.*?)"', machaine)
            for ele in machaine_list:
                if machaine_list.index(ele)==1:
                    dictval['type_element']=ele
                
                elif machaine_list.index(ele)==3:
                    dictval['url_site']=ele
                    
                elif machaine_list.index(ele)==5:
                    dictval['track_nom']=ele
                
                elif machaine_list.index(ele)==7:
                    dictval['track_zone']=ele
                
                elif machaine_list.index(ele)==9:
                    dictval['track_cible']=ele
            if(dictval['type_element']!="" and disctvalList["url_site"]!=""):
                disctvalList["type_element"].append(dictval['type_element'])
                disctvalList["url_site"].append(dictval['url_site'])
                disctvalList["track_nom"].append(dictval['track_nom'])
                disctvalList["track_zone"].append(dictval['track_zone'])
                disctvalList["track_cible"].append(dictval['track_cible'])
            
        
        df=pd.DataFrame(disctvalList)
        
        chemin=chemin.replace('https://','')
        chemin=chemin.replace('.','_')
        chemin=chemin.replace('/','')
        df.to_excel(path+'\\'+timestampStr2+"_"+chemin+".xlsx")            
        # Finally, close the Excel file
        # via the close() method.
        time.sleep(10)
        # time.sleep(600)
        driver.quit()

# enregistrement des fichiers dans un seul et meme fichier
location= parent_dir+'\\'+directory

# csv files in the path
file_list = glob.glob(location + "/*.xlsx")
 
# list of excel files we want to merge.
# pd.read_excel(file_path) reads the excel
# data into pandas dataframe.
excl_list = []
 
for file in file_list:
    excl_list.append(pd.read_excel(file))
 
# create a new dataframe to store the
# merged excel file.
excl_merged = pd.DataFrame()
 
for excl_file in excl_list:
     
    # appends the data into the excl_merged
    # dataframe.
    excl_merged = excl_merged.append(
      excl_file, ignore_index=True)
 
# exports the dataframe into excel file with
# specified name.
excl_merged.to_excel(location+'/'+'merged.xlsx', index=False)