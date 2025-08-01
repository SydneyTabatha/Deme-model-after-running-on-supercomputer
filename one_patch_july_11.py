"""
Goal of the simulation:
Stochastically simulate the ODEs using a Gillespie algorithm:

dx/dt = rx(1 - (x + y)/k)
dy/dt = urx(1 - (x + y)/k)
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import math
import os
import traceback

def run_simulation(seed):
    try:
        print(f"[{seed}] Simulation started.", flush=True)

        random.seed(seed)
        np.random.seed(seed)

        # Initialization
        x, y, t = 1, 0, 0
        X, Y, T, S = [x], [y], [t], [x + y]
        Patches = 100
        tend = 50
        k = 10000
        r1, r2, u, d = 0.5, 0.49, 5e-5, 0.05
        alpha, epsilon = 0.5, 1.5
        count = 0
        growth_law = 'saturated'
        threshold = 50000

        #while t < tend:
        while True:
            count += 1

            growth_factor = max(0, 1 - ((x + y) / k))

            if growth_law == 'saturated':
                g = alpha * ((epsilon * (x + y) / k) - 1)
                g = max(0, g * Patches**(1 / 3))
                rates = [
                    r1 * x * growth_factor * (1 - u),
                    d * x,
                    u * r1 * x * growth_factor + r2 * y * growth_factor,
                    d * y,
                    g * (k**(2 / 3))
                ]
            elif growth_law == 'logistic':
                rates = [
                    r1 * x * growth_factor * (1 - u),
                    d * x,
                    u * r1 * x * growth_factor + r2 * y * growth_factor,
                    d * y,
                    0
                ]
            else:  # Exponential
                rates = [
                    r1 * x * (1 - u),
                    d * x,
                    u * r1 * x + r2 * y,
                    d * y,
                    0
                ]

            rate_sum = sum(rates)
            if rate_sum == 0:
                print(f"[{seed}] Population crashed. Ending early.", flush=True)
                print("Population crashed")          
                return None

            tau = -math.log(random.random()) / rate_sum
            t += tau
            rand = random.uniform(0, 1) * rate_sum

            if rand <= rates[0]:
                x += 1
            elif rand <= rates[0] + rates[1]:
                x -= 1
            elif rand <= sum(rates[:3]):
                y += 1
            elif rand <= sum(rates[:4]):
                y -= 1
            else:
                k += 1  # carrying capacity increases

            current_size = x + y
            if count == 10000:
                #output_file.write(f"{t:.5f}\t{x}\t{y}\t{current_size}\n")
                X.append(x)
                Y.append(y)
                T.append(t)
                S.append(current_size)
                count = 0

            if  current_size >= threshold: # should be 8000 equilibirum around, 7200 works
                
                break                 

        print(f"[{seed}] Simulation complete. Final mutants: {y}", flush=True)
        return y
    
    except Exception as e:
            print(f"[ERROR] Simulation failed for seed {seed}: {e}", flush=True)
            traceback.print_exc()
            return None    







if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python one_patch_july_11.py output_filename")
        sys.exit(1)

    output_filename = sys.argv[1]
    target_successful_replicates = 100
    successful_replicates = 0
    base_seed = 1000 * int(os.path.splitext(os.path.basename(output_filename))[0].lstrip('x'))


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
