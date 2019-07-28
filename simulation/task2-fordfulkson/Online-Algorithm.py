#
# Ford and Fulkerson Algorithm implemented in Python.
#
import csv
import random
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
remain = {}
remain_ = {} #record the remain's initial value
bus_cap = {} #record how many sets remained for real
for k,v in buslines.items():
    remain[k] = K/len(v)
    remain_[k] = K/len(v)
    bus_cap[k] = K

accepted = 0
for i in range(600):
    d = random.randint(1,30)
    out1 = "** the "+str(i)+" passenger want to go to station "+str(d)
    print(out1)
    candidate = {}
    for k,v in buslines.items():
        if d in v:
            candidate[k]=remain[k]
    t = sorted(candidate.items(),key = lambda item:item[1], reverse = True)
    if bus_cap[t[0][0]]<=0:
        print("-> not accepte")
        continue
    else:
        remain[t[0][0]]-=1
        bus_cap[t[0][0]]-=1
        accepted+=1
        out2 = "-> the bus "+str(t[0][0])+" accepts the passenger and the bus still have "+str(bus_cap[t[0][0]])+" seats left"
        print(out2)

    for k,v in remain.items():
        if remain[k] <=0 and bus_cap[k]>0:
            remain[k] = remain_[k]

out3 = str(accepted)+" passengers accepted in total"
print(out3)
