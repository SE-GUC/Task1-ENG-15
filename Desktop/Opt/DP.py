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


def fixArray(array1):
    array2=[]
    temp=[]
    for elem in array1:
        if elem==-1:
            array2.append(temp)
            temp=[]
        else:
            if elem!=-2:
                temp.append(elem)
    return array2
memo = {}
numberOfRuns=0

def run(ns,nt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs,dests,wght,time,pps,shipmentTimes):
    global numberOfRuns
    numberOfRuns+=1
    
    mwString = ""

    for digit in mw:
        mwString += str(digit)+","
    #base Case
    if ns <= 0:
        return 0,[]
    shipOrg = orgs[0]
    #print(orgs)
    shipDest = dests[0]
    shipCurTime = shipmentTimes[0]
    shipMaxTime = time[0]
    shipPps = pps[0]
    shipWght = wght[0]
    
    #subproblem already solved
    if (ns,mwString,orgs[0],shipmentTimes[0]) in memo:
        return memo[(ns,mwString,orgs[0],shipmentTimes[0])]
    #go look for trip
    maxDelNum = 0
    endOfShip=False
    theTrip=-1
    theArray=[]
    for t in range(nt):
        tripOrg = startTripLoc[t]
        tripDest = endTripLoc[t]
        tripStartTim = startTime[t]
        tripEndTim = endTime[t]
        tripPpkg = ppkg[t]
        tripWght = mw[t]
        if shipOrg == tripOrg and shipCurTime <= tripStartTim and shipMaxTime >= tripEndTim and shipPps >= tripPpkg*shipWght and tripWght >= shipWght:
            if shipDest == tripDest:
                mwclone=mw[:]
                mwclone[t] -= shipWght
                deliveredNum,returnedArray = run(ns-1,nt,ppkg,mwclone,startTripLoc,endTripLoc,startTime,endTime,orgs[1:],dests[1:],wght[1:],time[1:],pps[1:],shipmentTimes[1:])
                deliveredNum+=1
                if deliveredNum>maxDelNum:
                    theArray=returnedArray
                    maxDelNum=deliveredNum
                    endOfShip=True
                    theTrip=t
            else:
                ppsclone=pps[:]
                ppsclone[0] -= tripPpkg*shipWght
                mwclone=mw[:]
                mwclone[t] -= shipWght
                orgsclone=orgs[:]
                orgsclone[0] = tripDest
                shipmentTimesclone=shipmentTimes[:]
                shipmentTimesclone[0] = tripEndTim
                deliveredNum,returnedArray = run(ns,nt,ppkg,mwclone,startTripLoc,endTripLoc,startTime,endTime,orgsclone,dests,wght,time,ppsclone,shipmentTimesclone)
                if deliveredNum>maxDelNum:
                    theArray=returnedArray
                    maxDelNum=deliveredNum
                    endOfShip=False
                    theTrip=t
        else:
            deliveredNum,returnedArray = run(ns-1,nt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs[1:],dests[1:],wght[1:],time[1:],pps[1:],shipmentTimes[1:])
            if deliveredNum>maxDelNum:
                theArray=returnedArray
                maxDelNum=deliveredNum
                endOfShip=True
                theTrip=-2
        deliveredNum,returnedArray = run(ns-1,nt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs[1:],dests[1:],wght[1:],time[1:],pps[1:],shipmentTimes[1:])
        if deliveredNum>maxDelNum:
            theArray=returnedArray
            maxDelNum=deliveredNum
            endOfShip=True
            theTrip=-2
    #add to memo

    if endOfShip:
        memo[(ns,mwString,orgs[0],shipmentTimes[0])]=maxDelNum,[theTrip,-1]+theArray
        return maxDelNum,[theTrip,-1]+theArray
    else:
        memo[(ns,mwString,orgs[0],shipmentTimes[0])]=maxDelNum,[theTrip]+theArray
        return maxDelNum,[theTrip]+theArray

nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw=read_input("testset_1/test_0.in")
shipmentTimes = [0]*ns
num,array=run(ns,nt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs,dests,wght,time,pps,shipmentTimes)
print(num,fixArray(array))
print(numberOfRuns)


