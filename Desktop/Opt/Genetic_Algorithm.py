import numpy as np
import random
import copy


def read_ints(s):
    return [int(i) for i in s.split(' ')]


def read_input(input_filepath):
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


if __name__ == "__main__":

    nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = read_input(
        "testset_1/test_1.in")
    dict_sol = {}

    max_population = 20
#    max iterations
    gen = 100

    create_population(max_population)
    initial_population = dict_to_population(dict_sol)
    print(counter)
    population = copy.deepcopy(initial_population)

    result = GA()

    # print(result, max_population, gen)
    count = 0
    for res in result:
        if len(res) > 0:
            count += 1
    print(count, result)


# =============================================================================
#     randomgene = random.sample(range(ns),ns)
# if randomgene[i] > ns/2 :
# If randomgene[i] > ns//2:
# #take parent1
# else:
# #take parent2
# =============================================================================
