import sys
import os
import random
import json
import math

# function start
#inputted = input("Enter benchmark file name here: ")
#outputted = input("Enter the name of the output json file: ")
inputted = "s27bench.txt"
outputted = "1stS27.json"
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
fanin3 = [] #for sequential bck gates
fanout3 = [] #for sequential for gates
FFout = ""
FFout1 = []
FFin = []
checkFF = False

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
        #print(name)
        #print('1')
        fanin.append((name,[]))
        fanin3.append((name,[]))
        typeof.append((name,"PI"))
        func.append((name,""))


    elif "=" in benchfile[i]: 
        # name, type, func
        benchfile[i] = benchfile[i].replace(' ','')
        end = benchfile[i].find('=') #possible issue, benchmarks dont have spaces
        name = benchfile[i][:end]
        names.append((name,""))
        names2.append(name)
        if "DFF" in benchfile[i]: ##take care of FF out /// here
            FFout = name            ##FF out is treated like an input
            FFout1.append(name)     #FFout1 is a list that stores names
            #names.append((FFout,""))
            #names2.append(FFout)
            inputs.append(FFout)  #appended to inputs
            typeof.append((FFout,"FF_out"))
            func.append((FFout,"DFF"))
            start = benchfile[i].find("(")
            end = benchfile[i].find(")")
            numbers = benchfile[i][start+1:end]
            numberslist = numbers.split(",")
            FFin += numberslist
            fanin.append((FFout,numberslist)) #this is new/ changed this instead of FF, []
            fanin2.append((FFout,numberslist))
            fanin3.append((FFout,[]))
            continue            ##edited on 7/11 5:26   ///  here
        if name in FFin:
            typeof.append((name,"FF_In"))
            checkFF = True
            start = benchfile[i].find("(")
            end = benchfile[i].find(")")
            numbers = benchfile[i][start+1:end] 
            numberslist = numbers.split(",")

        else:
            checkFF = False
        if (name not in outputs) and (checkFF != True):
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
        #print(name)
        #print('4')
        fanin.append((name,numberslist))
        fanin2.append([name,numberslist])
        fanin3.append((name,numberslist))

    else:
        continue
#finding fan out
#print(fanin)


fanout = []

for i in names2:
    fanoutlist = []
    for j in fanin2:
        for k in j[1]:
            if i == k:
                fanoutlist.append(j[0])
    fanout.append((i,fanoutlist))


#print(fanout) #fanout is where they go
#print(FFin)
#print(fanout)
#finding bck gates
#every input that feeds into a a PO
#only need to loop through outputs, then fan in
#print(fanout)

names = dict(names)
typeof = dict(typeof)
func = dict(func)
fanin = dict(fanin)
fanin3 = dict(fanin3)
fanout = dict(fanout)
bckgates = []

for i,j in fanout.items():
    if (i in FFin):
        fanout3.append((i,[]))
    else:
        fanout3.append((i,j))
fanout3 = dict(fanout3)

visited = set() # Set to keep track of visited nodes of graph.

def dfs(visited, graph, node):  #function for dfs
    if node not in visited:
        #print (node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

# Driver Code
fwdgates = []
#inputs += internals 
fwdlist = inputs + internals #FFout is already appended to inputs
for i in fwdlist:
    visited = set()
    dfs(visited, fanout3, i)
    visited.remove(i)
    visited = list(visited)
    fwdgates.append((i,visited))


visited = set()




newlist = internals + outputs + FFin
for i in newlist:
    visited = set()
    dfs(visited, fanin3, i)
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
