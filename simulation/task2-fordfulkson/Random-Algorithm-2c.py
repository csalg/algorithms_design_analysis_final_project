#
# Ford and Fulkerson Algorithm implemented in Python.
#
import csv
import random

def select_bus_randomly(d):
    remain_per_bus = {}
    remain_total = 0
    for k,v in buslines.items():
        if d in v:
            remain_per_bus[k] = remain_bus[k]
            remain_total+=remain_bus[k]
    random_select_list = []
    for k,v in remain_per_bus.items():
        for i in range(v):
            random_select_list.append(k)
    if len(random_select_list) == 0:
        return False
    else:
        return random_select_list[random.randint(0,len(random_select_list)-1)]


K = 35
buslines = {}
csv_r = csv.reader(open("buslines.csv","r"))
for line in csv_r:
    k = line[0]
    v = []
    for i in range(1,len(line)):
        v.append(int(line[i]))
    buslines[k] = v

#print(buslines)
remain_bus = {}
bus_cap = {}
for k,v in buslines.items():
    bus_cap[k] = K
    remain_bus[k] = bus_cap[k]


accepted = 0
for i in range(350):
    d = random.randint(1,30)
    out1 = "** the "+str(i)+" passenger want to go to station "+str(d)
    print(out1)
    b = select_bus_randomly(d)
    if b == False:
        print("-> not accepte")
        continue
    else:
        remain_bus[b]-=1
        accepted+=1
        out2 = "-> the bus "+b+" accepts the passenger and the bus still have "+str(remain_bus[b])+" seats left"
        print(out2)


out3 = str(accepted)+" passengers accepted in total"
print(out3)
