import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import sys
import os
from ortools.linear_solver import pywraplp
import random
import copy

from urllib.error import URLError


def file_selector(folder_path='testset_1/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox(
        '1. Select Input file from current directory', filenames)
    return os.path.join(folder_path, selected_filename)


def read_ints(s):
    return [int(i) for i in s.split(' ')]


def read_input_IP(input_filepath):
    with open(input_filepath, 'r') as f:
        input_file = f.read().split('\n')
    nl, mt, ns, nt = read_ints(input_file[0])
    orgs, dests, wght, time, pps = [], [], [], [], []
    for i in range(ns):
        l = read_ints(input_file[1 + i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = [], [], [], [], [], []
    for i in range(nt):
        l = read_ints(input_file[1+ns+i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route = np.zeros((nt, nl, nl), int)
    route = route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]] = 1

    tim = np.zeros((nt, mt, mt), int)
    tim = tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]] = 1
    return nl, mt, ns, nt, orgs, dests, wght, time, pps, route, tim, ppkg, mw


def read_input_IP_Manual(nl, mt, ns, nt, shipmentsArray, tripsArray):
    orgs, dests, wght, time, pps = [], [], [], [], []
    for i in range(len(shipmentsArray)):
        l = read_ints(shipmentsArray[i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = [], [], [], [], [], []
    for i in range(nt):
        l = read_ints(tripsArray[i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route = np.zeros((nt, nl, nl), int)
    route = route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]] = 1

    tim = np.zeros((nt, mt, mt), int)
    tim = tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]] = 1
    return nl, mt, ns, nt, orgs, dests, wght, time, pps, route, tim, ppkg, mw


def read_input_Greedy(input_filepath):
    with open(input_filepath, 'r') as f:
        input_file = f.read().split('\n')
    nl, mt, ns, nt = read_ints(input_file[0])
    orgs, dests, wght, time, pps = [], [], [], [], []
    for i in range(ns):
        l = read_ints(input_file[1 + i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = [], [], [], [], [], []
    for i in range(nt):
        l = read_ints(input_file[1+ns+i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route = np.zeros((nt, nl, nl), int)
    route = route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]] = 1

    tim = np.zeros((nt, mt, mt), int)
    tim = tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]] = 1
    return nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw


def read_input_Greedy_Manual(nl, mt, ns, nt, shipmentsArray, tripsArray):
    orgs, dests, wght, time, pps = [], [], [], [], []
    for i in range(ns):
        l = read_ints(shipmentsArray[i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = [], [], [], [], [], []
    for i in range(nt):
        l = read_ints(tripsArray[i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route = np.zeros((nt, nl, nl), int)
    route = route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]] = 1

    tim = np.zeros((nt, mt, mt), int)
    tim = tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]] = 1
    return nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw


def ip(ns, nt, nl, mt, ppkg, mw, route, tim, orgs, dests, wght, time, pps):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x_st = []
    y_s = []
    f_sil = []
    objective = solver.Objective()
    for s in range(ns):
        y_s.append(solver.BoolVar('Shipment'+str(s)))
        objective.SetCoefficient(y_s[s], 1)
        temparr = []
        for t in range(nt):
            temparr.append(solver.BoolVar(f'Shipment_{s}_Trip_{t}'))
        x_st.append(temparr)
        temparr = []
        for i in range(nl):
            temparr2 = []
            for l in range(mt):
                temparr2.append(solver.BoolVar(
                    f'Shipment_{s}_loc_{i}_time_{l}'))
            temparr.append(temparr2)
        f_sil.append(temparr)
    objective.SetMaximization()

    # (2) Respect stated price by customer
    for s in range(ns):
        solver.Add(solver.Sum([x_st[s][t]*ppkg[t]*wght[s]
                   for t in range(nt)]) <= pps[s]*y_s[s])

    # (3) Respect weight per trip
    for t in range(nt):
        solver.Add(solver.Sum([x_st[s][t]*wght[s]
                   for s in range(ns)]) <= mw[t])

    # (4) Packages are at their origin initialy
    for s in range(ns):
        for i in range(nl):
            solver.Add(f_sil[s][orgs[s]][0] == 1)

    # (5) f_sil
    for s in range(ns):
        for i in range(nl):
            for l in range(1, mt):
                solver.Add(f_sil[s][i][l] == f_sil[s][i][l-1]-solver.Sum([x_st[s][t]*route[t][i][j]*tim[t][l][e] for j in range(nl) for e in range(mt)
                           for t in range(nt)])+solver.Sum([x_st[s][t]*route[t][j][i]*tim[t][b][l] for j in range(nl) for b in range(mt) for t in range(nt)]))

    # (6) Leave only Once
    for s in range(ns):
        for i in range(nl):
            solver.Add(solver.Sum([x_st[s][t]*route[t][i][j]
                       for t in range(nt) for j in range(nl)]) <= 1)

    # (7) Max one place per time
    for s in range(ns):
        for l in range(mt):
            solver.Add(solver.Sum([f_sil[s][i][l] for i in range(nl)]) <= 1)

    # (8) Shipments cannot leave final dest
    for s in range(ns):
        solver.Add(solver.Sum([x_st[s][t]*route[t][dests[s]][j]
                   for j in range(nl) for t in range(nt)]) == 0)

    # (9) Taken when delivered
    for s in range(ns):
        solver.Add(f_sil[s][dests[s]][time[s]] == y_s[s])

    # (10) Shipments stop when no
    # for s in range(ns):
    #     solver.Add(solver.Sum([x_st[s][t] for t in range(nt)])<=nt*y_s[s])

    status = solver.Solve()
    if status == solver.OPTIMAL:
        returnedArray = []
        for s in range(ns):
            returnedArrayTemp = []
            # print(y_s[s],y_s[s].solution_value())
            for t in range(nt):
                if x_st[s][t].solution_value() == 1:
                    returnedArrayTemp.append(t)
            returnedArray.append(returnedArrayTemp)
            # print(x_st[s][t],x_st[s][t].solution_value())
            # for i in range(nl):
            #     for l in range(mt):
            #         if f_sil[s][i][l].solution_value()==1:
            #             print(f_sil[s][i][l],f_sil[s][i][l].solution_value())
        return round(solver.Objective().Value()), returnedArray


def greedy(ns, nt, nl, mt, ppkg, mw, startTripLoc, endTripLoc, startTime, endTime, orgs, dests, wght, time, pps):
    change = True
    shipmentTimes = np.zeros(ns)
    res = []
    deliveredNum = 0
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
                    # print("Here")
                    pps[s] -= tripPpkg*shipWght
                    mw[t] -= shipWght
                    orgs[s] = tripDest
                    shipmentTimes[s] = tripEndTim
                    change = True
                    changeShip = True
                    res[s].append(t)
                    deliveredNum += 1
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
                        # print("Here2")
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
    return deliveredNum, res


# Dynamic Programming Solution
def fixArray(array1):
    array2 = []
    temp = []
    for elem in array1:
        if elem == -1:
            array2.append(temp)
            temp = []
        else:
            if elem != -2:
                temp.append(elem)
    return array2


memo = {}
numberOfRuns = 0


def dp(ns, nt, ppkg, mw, startTripLoc, endTripLoc, startTime, endTime, orgs, dests, wght, time, pps, shipmentTimes):
    global numberOfRuns
    numberOfRuns += 1

    mwString = ""

    for digit in mw:
        mwString += str(digit)+","
    # base Case
    if ns <= 0:
        return 0, []
    shipOrg = orgs[0]
    # print(orgs)
    shipDest = dests[0]
    shipCurTime = shipmentTimes[0]
    shipMaxTime = time[0]
    shipPps = pps[0]
    shipWght = wght[0]

    # subproblem already solved
    if (ns, mwString, orgs[0], shipmentTimes[0]) in memo:
        return memo[(ns, mwString, orgs[0], shipmentTimes[0])]
    # go look for trip
    maxDelNum = 0
    endOfShip = False
    theTrip = -1
    theArray = []
    for t in range(nt):
        tripOrg = startTripLoc[t]
        tripDest = endTripLoc[t]
        tripStartTim = startTime[t]
        tripEndTim = endTime[t]
        tripPpkg = ppkg[t]
        tripWght = mw[t]
        if shipOrg == tripOrg and shipCurTime <= tripStartTim and shipMaxTime >= tripEndTim and shipPps >= tripPpkg*shipWght and tripWght >= shipWght:
            if shipDest == tripDest:
                mwclone = mw[:]
                mwclone[t] -= shipWght
                deliveredNum, returnedArray = dp(ns-1, nt, ppkg, mwclone, startTripLoc, endTripLoc,
                                                 startTime, endTime, orgs[1:], dests[1:], wght[1:], time[1:], pps[1:], shipmentTimes[1:])
                deliveredNum += 1
                if deliveredNum > maxDelNum:
                    theArray = returnedArray
                    maxDelNum = deliveredNum
                    endOfShip = True
                    theTrip = t
            else:
                ppsclone = pps[:]
                ppsclone[0] -= tripPpkg*shipWght
                mwclone = mw[:]
                mwclone[t] -= shipWght
                orgsclone = orgs[:]
                orgsclone[0] = tripDest
                shipmentTimesclone = shipmentTimes[:]
                shipmentTimesclone[0] = tripEndTim
                deliveredNum, returnedArray = dp(ns, nt, ppkg, mwclone, startTripLoc, endTripLoc,
                                                 startTime, endTime, orgsclone, dests, wght, time, ppsclone, shipmentTimesclone)
                if deliveredNum > maxDelNum:
                    theArray = returnedArray
                    maxDelNum = deliveredNum
                    endOfShip = False
                    theTrip = t
        else:
            deliveredNum, returnedArray = dp(ns-1, nt, ppkg, mw, startTripLoc, endTripLoc, startTime,
                                             endTime, orgs[1:], dests[1:], wght[1:], time[1:], pps[1:], shipmentTimes[1:])
            if deliveredNum > maxDelNum:
                theArray = returnedArray
                maxDelNum = deliveredNum
                endOfShip = True
                theTrip = -2
        deliveredNum, returnedArray = dp(ns-1, nt, ppkg, mw, startTripLoc, endTripLoc, startTime,
                                         endTime, orgs[1:], dests[1:], wght[1:], time[1:], pps[1:], shipmentTimes[1:])
        if deliveredNum > maxDelNum:
            theArray = returnedArray
            maxDelNum = deliveredNum
            endOfShip = True
            theTrip = -2
    # add to memo

    if endOfShip:
        memo[(ns, mwString, orgs[0], shipmentTimes[0])
             ] = maxDelNum, [theTrip, -1]+theArray
        return maxDelNum, [theTrip, -1]+theArray
    else:
        memo[(ns, mwString, orgs[0], shipmentTimes[0])
             ] = maxDelNum, [theTrip]+theArray
        return maxDelNum, [theTrip]+theArray

#==========================================================================================#
# Genetic is coming


def run(ns, nt, nl, mt, ppkg, mw, startTripLoc, endTripLoc, startTime, endTime, orgs, dests, wght, time, pps):

    change = True
    shipmentTimes = np.zeros(ns)
    res = []
    for i in range(ns):
        res.append([])
#    print(pps, mw, orgs, dests, shipmentTimes)
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
#            if there is a trip that dirctly delevers the shipments from the
#            current location directly take that trip
            for t in range(nt):
                tripOrg = startTripLoc[t]
                tripDest = endTripLoc[t]
                tripStartTim = startTime[t]
                tripEndTim = endTime[t]
                tripPpkg = ppkg[t]
                tripWght = mw[t]
                #print(shipMaxTime, tripEndTim)
                if shipOrg == tripOrg and shipDest == tripDest and shipCurTime <= tripStartTim and shipMaxTime >= tripEndTim and shipPps >= tripPpkg*shipWght and tripWght >= shipWght:
                    # print("Here")
                    pps[s] -= tripPpkg*shipWght
                    mw[t] -= shipWght
                    orgs[s] = tripDest
                    shipmentTimes[s] = tripEndTim
                    change = True
                    changeShip = True
                    res[s].append(t)
                    break
            if not changeShip and shipOrg != shipDest:
                randomized = []
#                check all possible trips that can be choosen for the current shipment
#                and collect a random trip from the pool of trips
                for t in range(nt):
                    tripOrg = startTripLoc[t]
                    tripDest = endTripLoc[t]
                    tripStartTim = startTime[t]
                    tripEndTim = endTime[t]
                    tripPpkg = ppkg[t]
                    tripWght = mw[t]
                    if shipOrg == tripOrg and shipCurTime <= tripStartTim and shipMaxTime >= tripEndTim and shipPps >= tripPpkg*shipWght and tripWght >= shipWght:
                        # print("Here2")
                        randomized.append(t)

                randInd = random.randint(0, len(randomized))
                if randInd != 0:
                    randInd -= 1
#                print(randInd, randomized, s)
                if len(randomized) != 0:
                    randT = randomized[randInd]
                    pps[s] -= ppkg[randT]*shipWght
                    mw[randT] -= shipWght
                    orgs[s] = endTripLoc[randT]
                    shipmentTimes[s] = endTime[randT]
                    res[s].append(randT)
                    change = True
#    remove the packages that where not deleverd correctly
#   side note the prices where not reset so they still contributed in the trip
#   so other trips may not collect the right ship because it has full capacity.
#   however this is greedy

    for s in range(ns):
        if orgs[s] != dests[s]:
            res[s] = []
#    print(pps, mw, orgs, dests, shipmentTimes)

    return res


def array2d_to_string(array):
    result = ""
    for i in range(len(array)):
        for j in range(len(array[i])):
            result += str(array[i][j])+','
        result += ";"
    return result[:-1]


def dict_to_population(dic):
    result = []
    for key in dic:
        shipments = key.split(';')
        ship = []
        for str_trip in shipments:
            if str_trip != []:
                trips = str_trip.split(',')
                trips = [int(x) for x in trips if x != '']
            ship.append(trips)

        result.append(ship)
    return result


counter = 0


def create_population(population):
    global counter

    current_population = 0
    while(True):
        if counter == 2000:
            print("Could only find: ", current_population)
            break
        random_shipment_indices = random.sample(range(ns), ns)
        counter += 1
        orgs_random = np.zeros(ns)
        dests_random = np.zeros(ns)
        wght_random = np.zeros(ns)
        time_random = np.zeros(ns)
        pps_random = np.zeros(ns)
        i = 0
        for index in random_shipment_indices:
            orgs_random[i] = orgs[index]
            dests_random[i] = dests[index]
            wght_random[i] = wght[index]
            time_random[i] = time[index]
            pps_random[i] = pps[index]
            i += 1

        random_trip_indices = random.sample(range(nt), nt)

        startTripLoc_random = np.zeros(nt)
        endTripLoc_random = np.zeros(nt)
        startTime_random = np.zeros(nt)
        endTime_random = np.zeros(nt)
        ppkg_random = np.zeros(nt)
        mw_random = np.zeros(nt)

        i = 0
        for index in random_trip_indices:
            startTripLoc_random[i] = startTripLoc[index]
            endTripLoc_random[i] = endTripLoc[index]
            startTime_random[i] = startTime[index]
            endTime_random[i] = endTime[index]
            ppkg_random[i] = ppkg[index]
            mw_random[i] = mw[index]
            i += 1

        res = run(ns, nt, nl, mt, ppkg_random, mw_random, startTripLoc_random, endTripLoc_random,
                  startTime_random, endTime_random, orgs_random, dests_random, wght_random, time_random, pps_random)

        i = 0
        res_org = copy.deepcopy(res)

        for index in random_shipment_indices:
            res_org[index] = res[i][:]
            i += 1

        dict_r = {}
        i = 0
        for index in random_trip_indices:
            dict_r[i] = index
            i += 1
        for i in range(ns):
            for j in range(len(res_org[i])):
                res_org[i][j] = dict_r[res_org[i][j]]

        key = array2d_to_string(res_org)
        if key in dict_sol:
            continue
        else:
            dict_sol[key] = 1
            current_population += 1
        if current_population == population:
            break


def crossover(x, y):
    randomgene = random.sample(range(ns), ns)
    childx = []
    childy = []
    for i in range(ns):
        if randomgene[i] > ns/2:
            childx.append(x[i])
            childy.append(y[i])
        else:
            childx.append(y[i])
            childy.append(x[i])

    return childx, childy


def validate(solution):

    trip_taken = np.zeros(nt)

    for i in range(ns):
        for j in range(len(solution[i])):
            trip_taken[solution[i][j]] += wght[i]

    for i in range(len(trip_taken)):
        if (trip_taken[i] > mw[i]):
            return False

    return True


def calculate_fitness(solution):
    score = 0
    for arr in solution:
        if arr != []:
            score += 1

    return score


def GA():
    global population
    for i in range(gen):

        # calculate fitness score
        score_population = []
        for result in population:
            fitness = calculate_fitness(result)
            score_population.append(fitness)

        zipped_scores = zip(score_population, population)
        sorted_scores_lists = sorted(zipped_scores)
        population = [element for _, element in sorted_scores_lists]

        fittest_pop = population[:]

        for j in range(len(fittest_pop)):
            for k in range(j+1, len(fittest_pop)):
                parent_x = fittest_pop[j]
                parent_y = fittest_pop[k]
                childx, childy = crossover(parent_x, parent_y)

                least_fittest = sorted_scores_lists[0][0]
                fitnessx = -1
                fitnessy = -1
                if validate(childx):
                    mutation = random.randint(0, 200)
                    if mutation < 3:
                        shipment_mutated = random.randint(0, ns-1)
                        childx[shipment_mutated] = []
                    fitnessx = calculate_fitness(childx)

                if validate(childy):
                    mutation = random.randint(0, 200)
                    if mutation < 3:
                        shipment_mutated = random.randint(0, ns-1)
                        childy[shipment_mutated] = []
                    fitnessy = calculate_fitness(childy)

                if fitnessx != -1:
                    if fitnessy != -1:
                        if fitnessx > fitnessy:
                            if fitnessx > least_fittest:
                                population = population[1:]
                                population.append(childx)
                                sorted_scores_lists = sorted_scores_lists[1:]
                                sorted_scores_lists.append((fitnessx, childx))
                                least_fittest = sorted_scores_lists[0][0]
                                if fitnessy > least_fittest:
                                    population = population[1:]
                                    population.append(childy)
                                    sorted_scores_lists = sorted_scores_lists[1:]
                                    sorted_scores_lists.append(
                                        (fitnessy, childy))
                        else:
                            if fitnessy > least_fittest:
                                population = population[1:]
                                population.append(childy)
                                sorted_scores_lists = sorted_scores_lists[1:]
                                sorted_scores_lists.append((fitnessy, childy))
                                least_fittest = sorted_scores_lists[0][0]
                                if fitnessx > least_fittest:
                                    population = population[1:]
                                    population.append(childx)
                                    sorted_scores_lists = sorted_scores_lists[1:]
                                    sorted_scores_lists.append(
                                        (fitnessx, childx))
                    else:
                        if fitnessx > least_fittest:
                            population = population[1:]
                            population.append(childx)
                            sorted_scores_lists = sorted_scores_lists[1:]
                            sorted_scores_lists.append((fitnessx, childx))
                else:
                    if fitnessy > least_fittest:
                        population = population[1:]
                        population.append(childy)
                        sorted_scores_lists = sorted_scores_lists[1:]
                        sorted_scores_lists.append((fitnessy, childy))

    return population[-1]


# Streamlit web app
st.write("""
# Ship it

Send your packages all over the world with the best prices!
""")

inputType = st.selectbox(
    '1. Upload an input file or input required fields manually', ["Upload a file", "Input manually"])

inputAlgo = st.selectbox(
    '2. Select an Algorithm', ["IP", "DP", "Greedy", "Genetic"])

if inputType == "Input manually":
    nl = st.text_input('Number of locations', '6', key='0')
    mt = st.text_input('Maximum time allowed', '10', key='1')
    ns = st.text_input('Number of Shipments', '4', key='2')
    nt = st.text_input('Number of locations', '6', key='3')

with st.form("second_form"):
    if inputType == "Upload a file":
        filename = file_selector()
        st.write('You selected `%s`' % filename)
    else:
        shipmentsArray = [0] * int(ns)
        tripsArray = [0] * int(nt)
        for i in range(int(ns)):
            shipmentsArray[i] = st.text_input(
                'orgs,dests,wght,time,pps', '0 1 10 5 40', key=str(i+100000))
            # shipmentNumber = 'Shipment ' + str(i) + ': '
            # st.write(shipmentNumber, shipmentsArray[i])

        for i in range(int(nt)):
            tripsArray[i] = st.text_input(
                'startTripLoc,endTripLoc,startTime,endTime,ppkg,mw', '3 5 5 6 3 30', key=str(i+200000))
            # tripNumber = 'Trip ' + str(i) + ': '
            # st.write(tripNumber, tripsArray[i])

    if(inputAlgo == 'Genetic'):
        max_population = st.text_input(
            'Max Population: ', '12', key='563453332')
        max_population = int(max_population)

        # max iterations
        gen = st.text_input('Number of generations: ',
                            '100', key='563453315332')
        gen = int(gen)

    st.write('You selected `%s`' % inputAlgo)
    runned = st.form_submit_button("Run")
    if runned:
        if(inputAlgo == "IP"):
            if (inputType == "Upload a file"):
                nl, mt, ns, nt, orgs, dests, wght, time, pps, route, tim, ppkg, mw = read_input_IP(
                    filename)
                st.write("Running input file", filename,
                         "using", inputAlgo, "Algorithm")
            else:
                nl, mt, ns, nt, orgs, dests, wght, time, pps, route, tim, ppkg, mw = read_input_IP_Manual(
                    int(nl), int(mt), int(ns), int(nt), shipmentsArray, tripsArray)

                # for i in range(int(ns)):
                #     shipmentNumber = 'Shipment ' + str(i) + ': '
                #     st.write(shipmentNumber, shipmentsArray[i])

                # for i in range(int(nt)):
                #     tripNumber = 'Trip ' + str(i) + ': '
                #     st.write(tripNumber, tripsArray[i])

                indexMe = ['Shipment'] * ns
                arrayDF = ['Shipment'] * ns
                # st.write(shipmentsArray[0].split(','))

                for i in range(ns):
                    indexMe[i] = 'Shipment ' + str(i)
                    arrayDF[i] = shipmentsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['orgs', 'dests', 'wght', 'time', 'pps'], index=indexMe)
                st.write('Inputed shipments: ')
                st.dataframe(dfObj)

                indexTrips = ['Trips'] * nt
                arrayDF = ['Trips'] * nt
                for i in range(nt):
                    indexTrips[i] = 'Trip ' + str(i)
                    arrayDF[i] = tripsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['startTripLoc', 'endTripLoc', 'startTime', 'endTime', 'ppkg', 'mw'], index=indexTrips)
                st.write('Inputed Trips: ')
                st.dataframe(dfObj)

            st.write('Inputed number of locations: ', nl)
            st.write('Inputed maximum time allowed: ', mt)
            st.write('Inputed number of Shipments: ', ns)
            st.write('Inputed number of trips: ', nt)

            shipmentDelivered, returnedArray = ip(ns, nt, nl, mt, ppkg, mw, route,
                                                  tim, orgs, dests, wght, time, pps)

            # df = pd.DataFrame(returnedArray)
            # st.dataframe(df)
            # st.write("Output: ", returnedArray)
            st.write("Output: ")
            st.write("Number of shipments delivered: ", shipmentDelivered)
            indexMe = ['Shipment'] * ns
            isSent = ['Shipment'] * ns
            arrayDF = ['Shipment'] * ns
            for i in range(ns):
                indexMe[i] = 'Shipment ' + str(i)
                if(len(returnedArray[i]) != 0):
                    isSent[i] = True
                else:
                    isSent[i] = False
                arrayDF[i] = [isSent[i], returnedArray[i]]
            dfObj = pd.DataFrame(arrayDF, columns=[
                'isDelievered', 'Path'], index=indexMe)
            st.dataframe(dfObj)

        elif(inputAlgo == "DP"):
            if (inputType == "Upload a file"):
                nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input_Greedy(
                    filename)
                st.write("Running input file", filename,
                         "using", inputAlgo, "Algorithm")
            else:
                nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input_Greedy_Manual(
                    int(nl), int(mt), int(ns), int(nt), shipmentsArray, tripsArray)
                # for i in range(int(ns)):
                #     shipmentNumber = 'Shipment ' + str(i) + ': '
                #     st.write(shipmentNumber, shipmentsArray[i])

                # for i in range(int(nt)):
                #     tripNumber = 'Trip ' + str(i) + ': '
                #     st.write(tripNumber, tripsArray[i])

                indexMe = ['Shipment'] * ns
                arrayDF = ['Shipment'] * ns
                # st.write(shipmentsArray[0].split(','))

                for i in range(ns):
                    indexMe[i] = 'Shipment ' + str(i)
                    arrayDF[i] = shipmentsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['orgs', 'dests', 'wght', 'time', 'pps'], index=indexMe)
                st.write('Inputed shipments: ')
                st.dataframe(dfObj)

                indexTrips = ['Trips'] * nt
                arrayDF = ['Trips'] * nt
                for i in range(nt):
                    indexTrips[i] = 'Trip ' + str(i)
                    arrayDF[i] = tripsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['startTripLoc', 'endTripLoc', 'startTime', 'endTime', 'ppkg', 'mw'], index=indexTrips)
                st.write('Inputed Trips: ')
                st.dataframe(dfObj)

                # st.write(nl, mt, ns, nt, orgs, dests, wght, time, pps,
                #          startTripLoc, endTripLoc, startTime, endTime, ppkg, mw)
            st.write('Inputed number of locations: ', nl)
            st.write('Inputed maximum time allowed: ', mt)
            st.write('Inputed number of Shipments: ', ns)
            st.write('Inputed number of trips: ', nt)

            shipmentTimes = [0]*int(ns)
            num, array = dp(ns, nt, ppkg, mw, startTripLoc, endTripLoc,
                            startTime, endTime, orgs, dests, wght, time, pps, shipmentTimes)

            st.write("Output: ")
            st.write('Number of shipments delievered', num)
            st.write('Number of runs are: ', numberOfRuns)
            indexMe = ['Shipment'] * ns
            isSent = ['Shipment'] * ns
            arrayDF = ['Shipment'] * ns
            # st.write(array)
            # st.write(fixArray(array))
            for i in range(ns):
                indexMe[i] = 'Shipment ' + str(i)
                if(len(fixArray(array)[i]) != 0):
                    isSent[i] = True
                else:
                    isSent[i] = False
                arrayDF[i] = [isSent[i], fixArray(array)[i]]
            dfObj = pd.DataFrame(arrayDF, columns=[
                'isDelievered', 'Path'], index=indexMe)
            st.dataframe(dfObj)

        elif(inputAlgo == "Genetic"):
            if (inputType == "Upload a file"):
                nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input_Greedy(
                    filename)
                # max_population = 12
                # gen = 100
                # st.write(nl, mt, ns, nt, orgs, dests, wght, time, pps,
                #          startTripLoc, endTripLoc, startTime, endTime, ppkg, mw)
                st.write("Running input file", filename,
                         "using", inputAlgo, "Algorithm")
            else:
                nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input_Greedy_Manual(
                    int(nl), int(mt), int(ns), int(nt), shipmentsArray, tripsArray)

                indexMe = ['Shipment'] * ns
                arrayDF = ['Shipment'] * ns
                # st.write(shipmentsArray[0].split(','))

                for i in range(ns):
                    indexMe[i] = 'Shipment ' + str(i)
                    arrayDF[i] = shipmentsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['orgs', 'dests', 'wght', 'time', 'pps'], index=indexMe)
                st.write('Inputed shipments: ')
                st.dataframe(dfObj)

                indexTrips = ['Trips'] * nt
                arrayDF = ['Trips'] * nt
                for i in range(nt):
                    indexTrips[i] = 'Trip ' + str(i)
                    arrayDF[i] = tripsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['startTripLoc', 'endTripLoc', 'startTime', 'endTime', 'ppkg', 'mw'], index=indexTrips)
                st.write('Inputed Trips: ')
                st.dataframe(dfObj)

            st.write('Inputed number of locations: ', nl)
            st.write('Inputed maximum time allowed: ', mt)
            st.write('Inputed number of Shipments: ', ns)
            st.write('Inputed number of trips: ', nt)

            dict_sol = {}

            create_population(max_population)

            initial_population = dict_to_population(dict_sol)

            population = copy.deepcopy(initial_population)

            result = GA()
            # st.write(result)
            # st.write(max_population)
            # st.write(gen)
            count = 0
            for res in result:
                if len(res) > 0:
                    count += 1
            # st.write("Number of shipments delivered: ", count)
            # st.write("Output: ", result)

            st.write("Output: ")
            st.write("counter: ", counter)
            st.write('Number of shipments delievered', count)
            st.write('Number of runs are: ', numberOfRuns)
            indexMe = ['Shipment'] * ns
            isSent = ['Shipment'] * ns
            arrayDF = ['Shipment'] * ns
            for i in range(ns):
                indexMe[i] = 'Shipment ' + str(i)
                if(len(result[i]) != 0):
                    isSent[i] = True
                else:
                    isSent[i] = False
                arrayDF[i] = [isSent[i], result[i]]
            dfObj = pd.DataFrame(arrayDF, columns=[
                'isDelievered', 'Path'], index=indexMe)
            st.dataframe(dfObj)

        elif(inputAlgo == "Greedy"):
            if (inputType == "Upload a file"):
                nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input_Greedy(
                    filename)
                # st.write(nl, mt, ns, nt, orgs, dests, wght, time, pps,
                #          startTripLoc, endTripLoc, startTime, endTime, ppkg, mw)
                st.write("Running input file", filename,
                         "using", inputAlgo, "Algorithm")
            else:
                nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input_Greedy_Manual(
                    int(nl), int(mt), int(ns), int(nt), shipmentsArray, tripsArray)
                # for i in range(int(ns)):
                #     shipmentNumber = 'Shipment ' + str(i) + ': '
                #     st.write(shipmentNumber, shipmentsArray[i])

                # for i in range(int(nt)):
                #     tripNumber = 'Trip ' + str(i) + ': '
                #     st.write(tripNumber, tripsArray[i])

                indexMe = ['Shipment'] * ns
                arrayDF = ['Shipment'] * ns
                # st.write(shipmentsArray[0].split(','))

                for i in range(ns):
                    indexMe[i] = 'Shipment ' + str(i)
                    arrayDF[i] = shipmentsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['orgs', 'dests', 'wght', 'time', 'pps'], index=indexMe)
                st.write('Inputed shipments: ')
                st.dataframe(dfObj)

                indexTrips = ['Trips'] * nt
                arrayDF = ['Trips'] * nt
                for i in range(nt):
                    indexTrips[i] = 'Trip ' + str(i)
                    arrayDF[i] = tripsArray[i].split(' ')

                dfObj = pd.DataFrame(
                    arrayDF, columns=['startTripLoc', 'endTripLoc', 'startTime', 'endTime', 'ppkg', 'mw'], index=indexTrips)
                st.write('Inputed Trips: ')
                st.dataframe(dfObj)

            st.write('Inputed number of locations: ', nl)
            st.write('Inputed maximum time allowed: ', mt)
            st.write('Inputed number of Shipments: ', ns)
            st.write('Inputed number of trips: ', nt)

            shipmentTimes = [0]*int(ns)
            st.write("output: ")
            deliveredNum, res = greedy(ns, nt, nl, mt, ppkg, mw, startTripLoc, endTripLoc,
                                       startTime, endTime, orgs, dests, wght, time, pps)

            st.write("Output: ")
            st.write("counter: ", counter)
            st.write('Number of shipments delievered', deliveredNum)
            st.write('Number of runs are: ', numberOfRuns)
            indexMe = ['Shipment'] * ns
            isSent = ['Shipment'] * ns
            arrayDF = ['Shipment'] * ns
            for i in range(ns):
                indexMe[i] = 'Shipment ' + str(i)
                if(len(res[i]) != 0):
                    isSent[i] = True
                else:
                    isSent[i] = False
                arrayDF[i] = [isSent[i], res[i]]
            dfObj = pd.DataFrame(arrayDF, columns=[
                'isDelievered', 'Path'], index=indexMe)
            st.dataframe(dfObj)
