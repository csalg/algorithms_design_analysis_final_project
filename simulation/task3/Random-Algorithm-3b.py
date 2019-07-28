#
# Ford and Fulkerson Algorithm implemented in Python.
#
import csv
import random
import math
import time
from Generate_orders import generate_buslines, generate_orders

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame,Series

def psi(bus,remain_per_bus,bus_cap,lowbound,upbound):
    z = float(remain_per_bus[bus])/bus_cap[bus]
    #print(remain_per_bus[bus],bus_cap[bus])
    #print(z)
    #print((pow((upbound*math.e/lowbound),z))*(lowbound/math.e))
    return (pow((upbound*math.e/lowbound),z))*(lowbound/math.e)

def select_bus_randomly(bus_candi,remain_per_bus):
    remain = {}
    for i in bus_candi:
        remain[i] = remain_per_bus[i]
    random_select_list = []
    for k,v in remain.items():
        for i in range(v):
            random_select_list.append(k)
    if len(random_select_list) == 0:
        return False
    else:
        return random_select_list[random.randint(0,len(random_select_list)-1)]

def stimulation(low,up,bus_num_expected,passenger_num_expected):
    bus_num_expected = 15
    passenger_num_expected = 700
    lowbound = 1
    upbound = up
    bus, bus_cap, bus_line, bus_time = generate_buslines(bus_num_expected,passenger_num_expected)
    orders = generate_orders(bus, bus_cap, bus_line, bus_time, lowbound, upbound)


    remain_per_bus = {}
    for k,v in bus_cap.items():
        remain_per_bus[k] = v
    priority_take = 0
    priority_total = 0
    passenger_take = 0
    passenger_total = 0

    for order in orders:
        index = order[0]
        t = order[1]
        c = order[2]
        d = order[3]
        p = order[4]
        priority_total+=p
        passenger_total+=c

        bus_candi = []
        for k,v in bus_line.items():
            if d not in v:
                continue
            if t>bus_time[k]:
                continue
            if c>remain_per_bus[k]:
                continue
            #print(p,psi(k))
            if p<psi(k,remain_per_bus,bus_cap,lowbound,upbound):
                continue
            bus_candi.append(k)
        bus_take = select_bus_randomly(bus_candi,remain_per_bus)
        if bus_take == False:
            continue
        else:
            remain_per_bus[bus_take]-=c
            priority_take+=p
            passenger_take+=c

    #print("priority total:",priority_total)
    #print("priority take:",priority_take)
    #print("passenger total:",passenger_total)
    #print("passenger take:",passenger_take)

    return float(priority_take)/priority_total

mean = 0
for x in range(100):
    mean+=stimulation(1,10,15,700)
print(mean/100)

data = []
for i in range(100):
    data.append([])

for u in range(2,21):
    for x in range(100):
        data[x].append(stimulation(1,u,15,700))


d = np.array(data)
#print(d)
#print(np.random.randn(10, 2))
df = DataFrame(d, columns=['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'])
boxplot=df.boxplot()
plt.xlabel('upbound of priority')
plt.ylabel("ratio")
plt.show()
