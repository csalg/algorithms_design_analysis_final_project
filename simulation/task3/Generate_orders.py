#Beijing Capital International Airport latitude 40.0799 longitude 116.6031
#the airport is the brgin spot and end spot
#30 destinaitons in Project01-data.csv

#there are m bus lines and they have all been determined
#so we should generate >300 passengers with their destinations
#and also should generate bus ilnes and capacity of bus

import csv
import math
import random

c_candi = [1,1,1,1,2,2,3,4,5]
def generate_buslines(m,n):
    #the amount of buses is among $m$+-3
    #and ensure all the bus station is covered ["1",...,"30"]
    #and all the seats are more than or just equal to the amount of people $n$
    #and the time is between [0,1000]
    bus_amount = random.randint(m - 3,m + 3)
    bus_cap = {}
    bus_line = {}
    bus_time = {}
    bus = []

    for i in range(bus_amount):
        b = "b"+str(i)
        bus.append(b)
        bus_cap[b] = 0
        bus_line[b] = []
        bus_time[b] = random.randint(1,1000)

    l = (n/len(bus))*2/3
    u = (n/len(bus))*4/3
    for i in range(len(bus)):
        bus_cap[bus[i]] = random.randint(l,u)

    for i in range(len(bus)):
        cap = [2,3,5,6]
        s = cap[random.randint(0,3)]
        t = 30/s #[1,t][t+1,2t][2t+1,3t][3t+1,4t]
        for j in range(s):
            bus_line[bus[i]].append(random.randint(j*t+1,(j+1)*t))

    #for i in bus:
        #print(i)
        #print("capacity",bus_cap[i])
        #print("route",bus_line[i])
        #print("arrive time",bus_time[i])
    #print("bus amont:", len(bus))

    return bus, bus_cap, bus_line, bus_time

def generate_orders(bus, bus_cap, bus_line, bus_time, lowbound, upbound):
    #n is the amount of the orders we wanna generate
    #for each order there are time, c(capacity), d(destinaiton), p(priority between lowbound and upbound)
    #for the bus, the time is leave time, and for the order the time is arrive time
    order = []#(index,t,c,d,p)
    index = 0
    priority_total = 0
    for b in bus:
        t = bus_time[b]
        line = bus_line[b]
        cap = bus_cap[b]

        while(cap>0):
            c = c_candi[random.randint(0,len(c_candi)-1)]
            while(c>cap):
                c = c_candi[random.randint(0,len(c_candi)-1)]
            cap-=c
            #print("t=",t)
            time = random.randint(1,t)
            desti = line[random.randint(0,len(line)-1)]
            p = random.randint(lowbound,upbound)
            order.append([index,time,c,desti,p])
            index+=1
            priority_total+=p
    #print("order:",len(order))
    #print("priority_total=",priority_total)
    return order

#bus, bus_cap, bus_line, bus_time = generate_buslines(15,700)
#order = generate_orders(bus, bus_cap, bus_line, bus_time, 1, 10)
