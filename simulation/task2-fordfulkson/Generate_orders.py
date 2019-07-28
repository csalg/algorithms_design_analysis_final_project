#Beijing Capital International Airport latitude 40.0799 longitude 116.6031
#the airport is the brgin spot and end spot
#30 destinaitons in Project01-data.csv

#there are m bus lines and they have all been determined
#so we should generate >300 passengers with their destinations
#and also should generate bus ilnes and capacity of bus

import csv
import math
import random

def Cal_distance(p1,p2):
    d = (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])
    return int(math.sqrt(d)*1000)

Airport = (116.6031, 40.0799)
Stations = {}
Stations[0] = Airport
csv_r = csv.reader(open("Project01-data.csv","r"))
for line in csv_r:
    if line[0] == "No.":
        continue
    Stations[int(line[0])] = (float(line[2]),float(line[3]))

print(Stations)

Ad_Matrix = []

for i in range(31):
    t = []
    for j in range(31):
        t.append(Cal_distance(Stations[i],Stations[j]))
    Ad_Matrix.append(t)

csv_w = csv.writer(open("matrix.csv","w"))
for i in Ad_Matrix:
    csv_w.writerow(i)

#--------generate bus lines---------------------------------
#m = 10 each bus get 4 stations [1,7] [8,15] [16,23] [24,30]
#and the capacity is both 35
buslines = {"b1":[1,9,18,24],
            "b2":[2,8,16,25],
            "b3":[3,10,17,22,26],
            "b4":[4,11,19,27],
            "b5":[5,12,20,28],
            "b6":[6,13,21,29],
            "b7":[7,14,22,24,30],
            "b8":[6,15,23,26],
            "b9":[3,11],
            "b10":[5,8,21,28]}
csv_w1 = csv.writer(open("buslines.csv","w"))
for k,v in buslines.items():
    t = [k]
    for i in v:
        t.append(i)
    csv_w1.writerow(t)

#-------generate 350 orders-----------------------------
#for each station how many passengers wanna go
amount = []
total = 0
for i in range(29):
    n = random.randint(0,20)
    amount.append(n)
    total+=n
amount.append(350-total)

csv_w2 = csv.writer(open("amount.csv","w"))
csv_w2.writerow(amount)
