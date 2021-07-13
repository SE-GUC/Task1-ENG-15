import numpy as np
from ortools.linear_solver import pywraplp


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
    return nl,mt,ns,nt,orgs,dests,wght,time,pps,route,tim,ppkg,mw


def run(ns,nt,nl,mt,ppkg,mw,route,tim,orgs,dests,wght,time,pps):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x_st=[]
    y_s=[]
    f_sil=[]
    objective = solver.Objective()
    for s in range(ns):
        y_s.append(solver.BoolVar('Shipment'+str(s)))
        objective.SetCoefficient(y_s[s], 1)
        temparr=[]
        for t in range(nt):
            temparr.append(solver.BoolVar(f'Shipment_{s}_Trip_{t}'))
        x_st.append(temparr)
        temparr=[]
        for i in range(nl):
            temparr2=[]
            for l in range(mt):
                temparr2.append(solver.BoolVar(f'Shipment_{s}_loc_{i}_time_{l}'))
            temparr.append(temparr2)
        f_sil.append(temparr)
    objective.SetMaximization()

    #(2) Respect stated price by customer
    for s in range(ns):
         solver.Add(solver.Sum([x_st[s][t]*ppkg[t]*wght[s] for t in range(nt)]) <= pps[s]*y_s[s])

    #(3) Respect weight per trip
    for t in range(nt):
        solver.Add(solver.Sum([x_st[s][t]*wght[s] for s in range(ns)])<=mw[t])

    #(4) Packages are at their origin initialy
    for s in range(ns):
        for i in range(nl):
            solver.Add(f_sil[s][orgs[s]][0]==1)

    #(5) f_sil
    for s in range(ns):
        for i in range(nl):
            for l in range(1,mt):
                solver.Add(f_sil[s][i][l]==f_sil[s][i][l-1]-solver.Sum([x_st[s][t]*route[t][i][j]*tim[t][l][e] for j in range(nl) for e in range(mt) for t in range(nt)])+solver.Sum([x_st[s][t]*route[t][j][i]*tim[t][b][l] for j in range(nl) for b in range(mt) for t in range(nt)]))

    #(6) Leave only Once
    for s in range(ns):
        for i in range(nl):
            solver.Add(solver.Sum([x_st[s][t]*route[t][i][j] for t in range(nt) for j in range(nl)]) <= 1)

    #(7) Max one place per time
    for s in range(ns):
        for l in range(mt):
            solver.Add(solver.Sum([f_sil[s][i][l] for i in range(nl)])<=1)

    #(8) Shipments cannot leave final dest
    for s in range(ns):
        solver.Add(solver.Sum([x_st[s][t]*route[t][dests[s]][j] for j in range(nl) for t in range(nt)])==0)    

    #(9) Taken when delivered
    for s in range(ns):
        solver.Add(f_sil[s][dests[s]][time[s]]==y_s[s])     

    #(10) Shipments stop when no
    # for s in range(ns):
    #     solver.Add(solver.Sum([x_st[s][t] for t in range(nt)])<=nt*y_s[s])

    status = solver.Solve()
    if status == solver.OPTIMAL:
        returnedArray=[]
        for s in range(ns):
            returnedArrayTemp=[]
            # print(y_s[s],y_s[s].solution_value())
            for t in range(nt):
                if x_st[s][t].solution_value()==1:
                    returnedArrayTemp.append(t)
            returnedArray.append(returnedArrayTemp)
                # print(x_st[s][t],x_st[s][t].solution_value())
            # for i in range(nl):
            #     for l in range(mt):
            #         if f_sil[s][i][l].solution_value()==1:
            #             print(f_sil[s][i][l],f_sil[s][i][l].solution_value())
        return round(solver.Objective().Value()), returnedArray


nl,mt,ns,nt,orgs,dests,wght,time,pps,route,tim,ppkg,mw=read_input("testset_1/test_0.in")
print(run(ns,nt,nl,mt,ppkg,mw,route,tim,orgs,dests,wght,time,pps))