#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 6 19:05:20 2022

@author: Ezra
"""
import json
import pandas as pd
import sys
#benchmarkfile = input("Enter json file name: ")
#lockedkey = input("Enter name of locked key: ")
#csvname = input("Enter the name of the csv to which you would like to write to: ")
#benchmarkfile = 
#lockedkey = 
#csvname = 

#im not sure what order you run these commands in so you can change the argv indexes as needed
benchmarkfile = sys.argv[1] #circuit graph json file
lockedgate = sys.argv[2] #locked PO
csvname = sys.argv[3] #csv to write to


file = open(benchmarkfile)
graph = json.load(file)

bck = graph["bck_gates"]
same = []
name = ""
uploading = []
sharedcount = 0
lockedcount = 0
faninforlocked = []
sharing = 0
#counts back gates for locked gate and appends them to a list
for i in bck[lockedgate]:
    lockedcount += 1
    faninforlocked.append(i)
#loops through each gate in back gates, checks against locked gate list
for i,j in bck.items():
    name = i
    for k in j:
        if k in faninforlocked:
            sharedcount += 1
    percent = (sharedcount / lockedcount) * 100
    if sharedcount > 0:
        sharing = 1
    else:
        sharing = 0
    same = [name, sharing, sharedcount, percent] 
    uploading.append(same)
    same = []
    sharedcount = 0
    percent = 0

#sorts csv in descending order based on shared gates, can be deleted
uploading = sorted(uploading, key=lambda x: x[3], reverse=True)

circuit = pd.DataFrame(uploading, columns=['Circuit', 'Sharing', 'Number of gates shared with locked key', 'percentage shared'])
#circuit is the dataframe
new_column_names = ['Circuit', 'Sharing', 'Number of Gates Shared with Locked Gate', 'Percentage Shared with Locked Gate']
circuit.to_csv(csvname, index=False, header=new_column_names)

file.close()
    
    
    
    


