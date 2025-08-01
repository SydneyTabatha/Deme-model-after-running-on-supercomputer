from math import sin
from numpy import array, arange, zeros
from pylab import plot, xlabel, show, legend, yscale, figure, ylabel
import numpy as np
import random
import numpy as np
import random
import math
import time
import sys
import os 

# REMEMBER TO DELETE DIRECTORY BEFORE EVERY RUN 

def run_simulation(seed):
    try:
    
        random.seed(seed)
        np.random.seed(seed)            
              
        
        growth_law = 'saturated'
        
        # Initialize parameters
        num_wt = 1
        threshold = 50000# CHANGE BACK
        n = 100 #number of patches
        r = 0.5   
        r2 = 0.49  
        d = 0.05  
        d2 = d    
        mu = 5e-5 
        eta = 0.0001#0.0001 # migration rate something wrong here - eta and mu and m are being mixed up somewhere !!!!!!!!!!!!!!!!!!!!!!!!!!!!! TO FIX!!!!!!
        alpha = 0.5
        epsilon = 1.5
        K = 100
        
        # --------------------------------------------------------------&|
        ## functions ##
        
        # function 1 : calculate rates 
        
        def rate_calculator(wildtype, mutant, kpatch):
                    
                    growth_factor = max(0, 1 - ((wildtype+ mutant) / kpatch))
                    if growth_law == 'exponential':
                                growth_factor = 1
                    
                    # wildtype birth rate
                    g1 = (1 - mu) * r * wildtype * growth_factor
                    if g1<0:
                                g1 = 0
                    
                    # wildtype death rate
                    g2 = d * wildtype
                    
                    # mutant birth rate
                    g3 = r2 * mutant * growth_factor    
                    if g3<0:
                                g3=0
                    
                    # mutant death rate
                    g4 = d2 * mutant
                    
                    # wildtype emigration rate 
                    g5 = eta * wildtype
                    if n==1:
                                g5 =0
                    
                    # mutant emigration rate
                    g6 = eta * mutant
                    if n==1:
                                g6 = 0
                    
                    #  mutant birth rate due to mutation events
                    g7 = mu * r * wildtype * growth_factor       
                    if g7<0:
                                g7 = 0
                    
                    if growth_law == 'saturated': # the other rates may need to be calculated after this!
                                g = alpha*((epsilon*(wildtype+mutant)/kpatch)-1)
                                if g<0:
                                            g=0
                                g8 = g*(kpatch**(2/3))
                    else:
                                g8=0
                    
                    ss = g1 + g2 + g3 + g4 + g5 + g6 + g7+g8
                    
                    return [ss, g1, g2, g3, g4, g5, g6, g7, g8]
            
        
        ## functions ##
        # --------------------------------------------------------------&|
        
        
        # Random number generator initialization
        random.seed(time.time())  # Set random seed based on current time
        
        # Initialize arrays (2D grid for patches)
        x = np.zeros(n)  # Wild type population in each patch, no history  
        x[0] = num_wt
        y = np.zeros(n)  # Mutant population in each patch 
        k = np.zeros(n) 
        for i in range(len(k)):
                    k[i] = K#100
        
        
        # Simulation variables
        xtime = 0.0
        count = 0
        
        
        list_sumx = [] # store history of total number of wt over time, no individual patch information stored 
        list_sumy = [] # store history of total number of mutants over time, no individual patch information stored 
        time_list = []
        
        #growth_law = 'saturated'
        xtime = 0
        # Time loop for simulation 
        while True:
        #while xtime < 900: #900
                    
                    count += 1
        
            
                    # Calculate total event rate across all patches
                    sum_events = 0 # total rate sum of rate sums across patches
                    for i in range(n):
                                wildtype = x[i]
                                mutant = y[i]
                                kpatch = k[i]
                                ss = rate_calculator(wildtype, mutant, kpatch)[0] # calculating rate sum for a given patch
                                sum_events += ss # add rate some for a given patch to total
        
                    if sum_events == 0:
                                return None 
                        
                    # Calculate the time increment based on the sum of all events across demes
                    xran = random.random()
                    tincr = (-math.log(xran)) / sum_events # draw time increment from an exponential distribution based on the total rate
                    xtime += tincr # add time incriment to the total amount of time that has passed 
        
                    # Output the time series every 100 updates 
                    if count == 10000: # 100
                                count = 0
                                sumx = np.sum(x) # We are summing across all the patches to get the total numebr of wildtypes
                                sumy = np.sum(y)# we are summing across all the patches to get the total number of mutants
                                #print('time, total wildtype num across patches, total mutant num across patches = ', f"{xtime:20.10f}   {sumx:10.2f}   {sumy:10.2f}")
                                
                                current_size = sumx+sumy
                                
                                #output_file.write(f"{xtime:.5f}\t{int(sumx)}\t{int(sumy)}\t{int(current_size)}\n") 
                                
                    ########################################################################################################
                    # idk if i have to repeat this????????????
                    # Find a patch to update based on the number of events in each patch 
                    total_events = np.zeros(n) # cumulative propensities of patches
                    sum_ss = 0
                    for i in range(n): # for each patch calculate the total event rate for that patch 
                                wildtype = x[i]
                                mutant = y[i]
                                kpatch  = k[i]
                                ss = rate_calculator(wildtype, mutant, kpatch)[0] # calculating rates for every patch                
                                sum_ss += ss
                    
                                total_events[i] = sum_ss # stores all events up to and including patch k # cummulative - like a roulette wheel - the bigger the interval the more likely you are to land on it 
        
        
                    # Select the patch based on the cumulative sum of events
                    xran = random.random()
                    locator = xran * sum_ss # a random number from [0, total propensity]"locator picks a random number on the intervaled spectrum and total_events provides the intervals... the patch with the largest interval is more likely to be the one that the random number falls between."
                    selected_patch_index = np.searchsorted(total_events, locator) # gives which patch the locator land in 
                    i = selected_patch_index 
                    #print('patch chosen is',i)
                    
                    ########################################################################################################
                    # now that we have selected our patch based on the propensities in each patch we can run the gillespie algorithm on the selected patch 
                    # Gillespie algorithm to update the selected patch
                
                    # so here x[i,j] is the number of wildtypes in our chosen patch we calculated it before as part of the total rate but didnt store it so we have to calculate again 
                    wildtype = x[i]
                    mutant = y[i]
                    kpatch = k[i]
                    result = rate_calculator(wildtype, mutant, kpatch)
                    ss = result[0] # probably don't need to call this again
                    g1 = result[1]
                    g2 = result[2]
                    g3 = result[3]
                    g4 = result[4]
                    g5 = result[5]
                    g6 = result[6]
                    g7 = result[7]
                    g8 = result[8]
                    
                    # Generate probabilities for the events - make them fall between 0 and 1 
                    aa = g1 / ss
                    bb = g2 / ss
                    cc = g3 / ss
                    dd = g4 / ss
                    ee = g5 / ss
                    ff = g6 / ss
                    gg = g7 / ss
                    hh = g8/ss
                
                    # Now that we're in a patch, and we calculated the rates for this patch, we can choose an event randomly
                    xran = random.uniform(0,1) 
                    
                    
                    
                    # mutant and wildtype birth and death events
                    if xran < aa: 
                                x[i] += 1 # wt birth event
                    elif xran < aa + bb:
                                x[i] -= 1 # wt decay event
                    elif xran < aa + bb + cc:
                                y[i] += 1 # mutant birth event
                    elif xran < aa + bb + cc + dd:
                                y[i] -= 1 # mutant decay event 
                        
                    # emigration (and immigration for another patch)
                    elif xran < aa + bb + cc + dd + ee: # -------------------------------------------------------------------------| 
                                while True:
                                            ipos = random.randint(0, n - 1)
                                            if ipos != i and (x[ipos]+y[ipos]  < k[ipos]):
                                                        break
                        
                                x[i] -= 1 # take from current patch 
                                x[ipos] += 1 # and add to new patch  IMMIGRATION
                        
                    elif xran < aa + bb + cc + dd + ee + ff:
                                while True:
                                            ipos = random.randint(0, n - 1)
                                            if ipos != i and (x[ipos]+y[ipos]  < k[ipos]):
                                                        break        
                                y[i] -= 1
                                y[ipos] += 1 # repeated exactly what we did with wildtypes for mutants # ---------------------------------------------------------------| 
                        
                    # mutantion
                    elif xran < aa + bb + cc + dd + ee + ff + gg: 
                                y[i] += 1 # wt to mutant gain event 
                    
        
                    
                    # update carrying capacity if saturated growth 
                    elif xran<aa + bb + cc + dd + ee + ff + gg+hh: 
                                # increase carrying capacity
                                k[i]+=1
                    
        
            
                    # Sum populations across all patches
                    sumx = np.sum(x)
                    sumy = np.sum(y)
                    
                    # keep track 
                    list_sumx.append(sumx)
                    list_sumy.append(sumy)
                    
                    time_list.append(xtime)
                
                    # ncomment to stop when population reaches a SIZE threshold
                    
                    totalpop = sumx + sumy
                    print(totalpop)
                    if  sumx + sumy >= threshold: # should be 8000 equilibirum around, 7200 works
                                print(f"Threshold reached. There are: {sumy} mutants at {totalpop}")
                                break 
                    
        print(f"Simulation {seed} complete.")
        return sumy              
        
    except Exception as e:
        print(f"[ERROR] Simulation failed for seed {seed}: {e}")
        return None
    
## NEW #################################

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python multi_patch_july_11.py output_filename")
        sys.exit(1)

    output_filename = sys.argv[1]
    target_successful_replicates = 100
    successful_replicates = 0
    base_seed = 1000 * int(os.path.splitext(os.path.basename(output_filename))[0].lstrip('m'))


    with open(output_filename, "w") as f:
        f.write("final_mutants\n")  # You can customize what to store

        attempt = 0
        while successful_replicates < target_successful_replicates:
            current_seed = base_seed + attempt
            result = run_simulation(current_seed)

            if result is not None:
                f.write(f"{result}\n")
                successful_replicates += 1

            attempt += 1
