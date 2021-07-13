import random
import os

maxTime=10
numOfLocations=6
numOfShipments=7
numOfTrips=40
maxWeightPerShip=20
maxWeightPerTrip=100
maxPricePerShip=200
maxPricePertrip=15

filename=os.path.join("testset_1","test_"+str(1)+".in")
f = open(filename, "w")
f.writelines(str(numOfLocations)+" "+str(maxTime)+" "+ str(numOfShipments)+" "+str(numOfTrips)+"\n")

for i in range(numOfShipments):
    orgs=random.randint(0,numOfLocations-1)
    dests=random.randint(0,numOfLocations-1)
    while(orgs==dests):
        dests=random.randint(0,numOfLocations-1)
    wght=random.randint(1,maxWeightPerShip)
    time=random.randint(maxTime//2,maxTime-1)
    pps=random.randint(15,maxPricePerShip)
    f.writelines(str(orgs)+" "+str(dests)+" "+ str(wght)+" "+str(time)+" "+str(pps)+"\n")

for t in range(numOfTrips):
    startTripLoc=random.randint(0,numOfLocations-1)
    endTripLoc=random.randint(0,numOfLocations-1)
    while(startTripLoc==endTripLoc):
        endTripLoc=random.randint(0,numOfLocations-1)
    startTime=random.randint(1,maxTime//2)
    endTime=random.randint(startTime+1,maxTime-1)
    ppkg=random.randint(1,maxPricePertrip)
    mw=random.randint(5,maxWeightPerTrip)
    f.writelines(str(startTripLoc)+" "+str(endTripLoc)+" "+ str(startTime)+" "+str(endTime)+" "+str(ppkg)+" "+str(mw)+"\n")

# nl,mt,ns,nt
# ns lines of: orgs,dests,wght,time,pps 
# nt lines of: startTripLoc,endTripLoc,startTime,endTime,ppkg,mw

# orgs= [ 0, 1, 0, 0]
# dests=[ 1, 2, 3, 5]
# wght= [10,10, 7, 5]
# time= [ 5, 3, 5, 6]
# pps=  [40,40,40,50]

# startTripLoc=[ 0, 0, 0, 0, 0, 3]
# endTripLoc=  [ 1, 1, 1, 1, 3, 5]
# startTime=   [ 1, 1, 1, 1, 1, 5]
# endTime=     [ 4, 4, 3, 3, 4, 6]
# ppkg=        [ 1, 2, 3, 4, 5, 3]
# mw=          [20,15,20,50,30,30]

