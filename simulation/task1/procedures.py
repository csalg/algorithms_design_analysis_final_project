import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import random

from disjointSetForests import *

def makeGeoDF():
    df = pd.read_csv('./data/data.csv', encoding='gbk')
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    crs ={'init': 'epsg:4326'}
    return(gpd.GeoDataFrame(df, geometry=geometry, crs=crs))

def clarkeWrightSolver(df, demand, k, delta=0):
    """
    An implementation of Clarke-Wright CVRP solver using disjoint random forests.
    It can be run in either deterministic or randomized modes.
    To run in randomised mode, provide a value for delta.
    In randomized mode, the algorithm will choose a savings candidate within the top 
    delta savings.
    Parameters: 
    df      a dataframe with longitude, latitude, and shapely.Point in cols 2,3,4
    demand  an array with demand for each destination
    k       maximum capacity per bus
    delta   choose among top delta candidates for savings
    """

    def getNext():
        if delta == 0:
            return savings_arr.pop(0)
        else:
            random_idx = random.randint(0,min(delta,len(savings_arr)-1))
            return savings_arr.pop(random_idx)

    savings_arr = []

    for i in range (0,31):
        for j in range(0,31):
            if (i >= j) or (i == 0 or j ==0):
                continue
            saving_ = df.iloc[0,4].distance(df.iloc[i,4]) + df.iloc[0,4].distance(df.iloc[j,4]) - df.iloc[i,4].distance(df.iloc[j,4])
            savings_arr.append((saving_,i,j))

    savings_arr = sorted(savings_arr,reverse=True,key=lambda tup:tup[0])

    cycles = {}
    for i in range(1,31):
        cycles[i]=(([i,],2*df.iloc[0,4].distance(df.iloc[i,4]),demand[i-1]))

    p = [0 for i in range(0,31)]
    r = [0 for i in range(0,31)]

    [makeSet(p,r,i) for i in range(1,31)]

    while bool(savings_arr):

        saving, i, j = getNext()

        if i == 0 or j == 0:
            continue

        i_parent = findSet(p,r,i)
        j_parent = findSet(p,r,j)

        if i_parent != j_parent: # Not already in cycle

            if cycles[i_parent][2] + cycles[j_parent][2] <= k: # Capacity bound
                
                i_parent_head = cycles[i_parent][0][0]
                i_parent_tail = cycles[i_parent][0][-1]
                j_parent_head = cycles[j_parent][0][0]
                j_parent_tail = cycles[j_parent][0][-1]

                is_i_exterior = i_parent_head == i or i_parent_tail == i
                is_j_exterior = j_parent_head == j or j_parent_tail == j
                
                if is_j_exterior and is_i_exterior: # Can only merge exterior locs.
                    
                    union(p,r,i,j)

                    # These if-statements join the two tours considering 
                    # all cases for i or j being at the head or tail.
                    if i_parent_tail == i and j_parent_head == j:
                        new_tour = cycles[i_parent][0] + cycles[j_parent][0]
                    if i_parent_head == i and j_parent_tail == j:
                        new_tour = cycles[j_parent][0] + cycles[i_parent][0]
                    if i_parent_tail == i and j_parent_tail == j: 
                        cycles[j_parent][0].reverse() 
                        new_tour = cycles[i_parent][0] + cycles[j_parent][0]
                    if i_parent_head == i and j_parent_head == j:
                        cycles[i_parent][0].reverse() 
                        new_tour = cycles[i_parent][0] + cycles[j_parent][0]

                    new_dist = cycles[i_parent][1] + cycles[j_parent][1] - saving

                    new_cap = cycles[i_parent][2] + cycles[j_parent][2]

                    if j in cycles:
                        cycles.pop(j)
                    if j_parent in cycles:
                        cycles.pop(j_parent)

                    cycles[i_parent] = (new_tour,new_dist,new_cap)

    cycles_ = []
    # Add depot at beginning and end of tours
    for cycle in cycles.values():
        tour = cycle[0]
        tour = [0,]+tour+[0,]
        # print(tour)
        cycles_.append((tour, cycle[1], cycle[2]))

    return(cycles_)

def plotBase(geo_df):
    """
    Plots the city
    """
    street_map =gpd.read_file("./shape/roads.shp")
    buildings =gpd.read_file("./shape/buildings.shp")
    fig,ax =plt.subplots(figsize=(50,50))
    street_map.plot(ax=ax, alpha=0.2, color="grey")
    buildings.plot(ax=ax, alpha=0.3, color="orange")
    geo_df.plot(ax=ax, markersize=400, color="blue")
    geo_df[geo_df["No."]==0].plot(ax=ax, markersize=400, color="red")
    return ax

def plotCycleArrows(geo_df,ax,cycle,color="k"):
    """
    Plots the tours on the map using arrows.
    """
    for idx in range(0,len(cycle)-1):
        i = cycle[idx]
        j = cycle[idx+1]
        base_x = geo_df.iloc[i,2]
        base_y = geo_df.iloc[i,3]
        dx = geo_df.iloc[j,2] - base_x
        dy = geo_df.iloc[j,3] - base_y
        ax.arrow(base_x, base_y, dx,dy,fc=color, ec=color)
    return(ax)

def calculateSolutionCost(sol):
    """
    Returns the cost of a set of tours.
    """
    cost = 0
    for cycle in sol:
        cost += cycle[1]
    return(cost)

def clarkeWrightSolverRandomized(df, demand, k, delta=10,iterations=100):
    """
    A wrapper for running CW-GRASP multiple times and returning 
    the best solution. It also calculates how much it improves on the 
    deterministic version of CW.
    """
    best_sol = clarkeWrightSolver(df, demand, k)
    original_cost = calculateSolutionCost(best_sol)
    best_cost = original_cost
    for iter in range(0,iterations):
        sol = clarkeWrightSolver(df, demand, k, delta=10)
        cost = calculateSolutionCost(sol)
        if cost<best_cost:
            best_cost = cost
            best_sol = sol
    improvement = (original_cost-best_cost)*100/original_cost
    return(improvement,best_sol)