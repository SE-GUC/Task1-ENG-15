import numpy as np

def read_ints(s):
    return [int(i) for i in s.split(' ')]
def read_input(input_filepath):
    with open(input_filepath, 'r') as f:
        input_file = f.read().split('\n')
    nl,mt,ns,nt = read_ints(input_file[0])
    orgs, dests, wght, time,pps = [], [], [], [], []
    for i in range(ns):
        l = read_ints(input_file[1 + i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc,endTripLoc,startTime,endTime,ppkg,mw=[],[],[],[],[],[]
    for i in range(nt):
        l = read_ints(input_file[1+ns+i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route=np.zeros((nt,nl,nl),int)
    route=route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]]=1

    tim=np.zeros((nt,mt,mt),int)
    tim=tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]]=1
    return nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw

def run(ns,nt,nl,mt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs,dests,wght,time,pps):
    change = True
    shipmentTimes = np.zeros(ns)
    res = []
    deliveredNum=0
    for i in range(ns):
        res.append([])
    # print(pps, mw, orgs, dests, shipmentTimes)
    while(change):
        change = False
        for s in range(ns):
            shipOrg = orgs[s]
            shipDest = dests[s]
            shipCurTime = shipmentTimes[s]
            shipMaxTime = time[s]
            shipPps = pps[s]
            shipWght = wght[s]
            changeShip = False
            for t in range(nt):
                tripOrg = startTripLoc[t]
                tripDest = endTripLoc[t]
                tripStartTim = startTime[t]
                tripEndTim = endTime[t]
                tripPpkg = ppkg[t]
                tripWght = mw[t]
                #print(shipMaxTime, tripEndTim)
                if shipOrg == tripOrg and shipDest == tripDest and shipCurTime <= tripStartTim and shipMaxTime >= tripEndTim and shipPps >= tripPpkg*shipWght and tripWght >= shipWght:
                    #print("Here")
                    pps[s] -= tripPpkg*shipWght
                    mw[t] -= shipWght
                    orgs[s] = tripDest
                    shipmentTimes[s] = tripEndTim
                    change = True
                    changeShip = True
                    res[s].append(t)
                    deliveredNum+=1
                    break
            if not changeShip:
                minCost = 1e9
                minIndex = -1
                for t in range(nt):
                    tripOrg = startTripLoc[t]
                    tripDest = endTripLoc[t]
                    tripStartTim = startTime[t]
                    tripEndTim = endTime[t]
                    tripPpkg = ppkg[t]
                    tripWght = mw[t]
                    if shipOrg == tripOrg and shipCurTime <= tripStartTim and shipMaxTime >= tripEndTim and shipPps >= tripPpkg*shipWght and tripWght >= shipWght:
                        #print("Here2")
                        if minCost > tripPpkg*shipWght:
                            minCost = tripPpkg*shipWght
                            minIndex = t
                if minIndex != -1:
                    pps[s] -= ppkg[minIndex]*shipWght
                    mw[minIndex] -= shipWght
                    orgs[s] = endTripLoc[minIndex]
                    shipmentTimes[s] = endTime[minIndex]
                    res[s].append(minIndex)
                    change = True
    
    for s in range(ns):
        if orgs[s] != dests[s]:
            res[s] = []
    # print(pps, mw, orgs, dests, shipmentTimes)
    print(deliveredNum,res)
    return deliveredNum, res
                
                

nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw=read_input("testset_1/test_0.in")
run(ns,nt,nl,mt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs,dests,wght,time,pps)

