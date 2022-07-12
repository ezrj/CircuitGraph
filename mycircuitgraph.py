#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 1 23:45:41 2022

@author: Ezra
"""
import sys
import os
import random
import json
import math

# function start
#inputted = input("Enter benchmark file name here: ")
#outputted = input("Enter the name of the output json file: ")
#inputted = 
#outputted = 
inputted = sys.argv[1]
outputted = sys.argv[2]
outfile = str(outputted)
inputt = str(inputted)
bench = open(inputt,'r')
benchfile = bench.readlines()
length = len(benchfile)

names = [] # will be converted to dictionary
names2 = [] 
outputs = []
inputs = []
internals = []
typeof = []
func = []
name = ""
fanin = []
fanin2 = []

for i in range(length):
    if "OUTPUT" in benchfile[i]:    
        #populates names, outputs, and types 
        start = benchfile[i].find('(')
        end = benchfile[i].find(')')
        name = benchfile[i][start+1:end] 
        names2.append(name) 
        outputs.append(name)
        names.append((name,""))
        typeof.append((name,"PO"))
        


    elif "INPUT" in benchfile[i]:
        #populates name, inputs, type, and gets first fan in
        start = benchfile[i].find('(')
        end = benchfile[i].find(')')
        name = benchfile[i][start+1:end]
        names.append((name,""))
        names2.append(name)
        inputs.append(name)
        fanin.append((name,[]))
        typeof.append((name,"PI"))
        func.append((name,""))



    elif "=" in benchfile[i]: 
        # name, type, func
        benchfile[i] = benchfile[i].replace(' ','')
        end = benchfile[i].find('=') 
        name = benchfile[i][:end]
        names.append((name,""))
        names2.append(name)
        if name not in outputs:
            typeof.append((name,"Internal"))
            internals.append(name)

        nextstart = benchfile[i].find("=")
        nextend = benchfile[i].find("(") 
        gatetype = benchfile[i][nextstart+1:nextend]
        func.append((name,gatetype))
        #finding fan in
        

        start = benchfile[i].find("(")
        end = benchfile[i].find(")")
        numbers = benchfile[i][start+1:end]
        numberslist = numbers.split(",")
        fanin.append((name,numberslist))
        fanin2.append([name,numberslist])

    else:
        continue



fanout = []

for i in names2:
    fanoutlist = []
    for j in fanin2:
        for k in j[1]:
            if i == k:
                fanoutlist.append(j[0])
    fanout.append((i,fanoutlist))

#finding bck gates

names = dict(names)
typeof = dict(typeof)
func = dict(func)
fanin = dict(fanin)
fanout = dict(fanout)
bckgates = []


visited = set() # Set to keep track of visited nodes of graph.

def dfs(visited, graph, node):  #function for dfs
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

# Driver Code
fwdgates = []
inputs += internals
for i in inputs:
    visited = set()
    dfs(visited, fanout, i)
    visited.remove(i)
    visited = list(visited)
    fwdgates.append((i,visited))


visited = set()

newlist = internals + outputs
for i in newlist:
    visited = set()
    dfs(visited, fanin, i)
    visited.remove(i)
    visited = list(visited)
    bckgates.append((i,visited))

bckgates = dict(bckgates)
fwdgates = dict(fwdgates)




dict1 = {"names":names, "type":typeof, "func":func, "fan in":fanin, "fan out":fanout, "bck_gates":bckgates, "forward gates:":fwdgates}

out_file = open(outfile, "w")
  
json.dump(dict1, out_file, indent = 6)
  
out_file.close()
bench.close()


        




        



    







