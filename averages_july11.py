


import glob
import numpy as np

all_values = []

for file in glob.glob("x*.dat"):
    with open(file) as f:
        next(f)  # skip header line
        values = [int(line.strip()) for line in f]
        all_values.extend(values)

all_values = np.array(all_values)
print(f"Total replicates: {len(all_values)}")
print(f"Mean: {np.mean(all_values)}, Std: {np.std(all_values)}")


# in each .dat file there are 100 replicates each just one number - the number of mutants at the end of the simulation

print('#------------------------------------------------------%|')

all_values_multi = []

for file in glob.glob("m*.dat"):
    with open(file) as f:
        next(f)  # skip header line
        values = [float(line.strip()) for line in f]
        all_values_multi.extend(values)

all_values_multi = np.array(all_values_multi)
print(f"Total replicates or multipatch simulation: {len(all_values_multi)}")
print(f"Mean: {np.mean(all_values_multi)}, Std: {np.std(all_values_multi)}")
















'''
import glob
import os
import numpy as np

def average_list():
    file_list = sorted(glob.glob("replicate_*.txt"))
    wt_list, mut_list, size_list, time_list = [], [], [], []

    for filename in file_list:
        if os.path.getsize(filename) == 0:
            print(f"Skipping empty file: {filename}")
            continue
        data = np.loadtxt(filename, skiprows=1)
        time = data[:, 0]
        wt = data[:, 1]
        mut = data[:, 2]
        size = data[:, 3]
        time_list.append(time)
        wt_list.append(wt)
        mut_list.append(mut)
        size_list.append(size)

    min_length = min(len(t) for t in time_list)
    wt_array = np.array([w[:min_length] for w in wt_list])
    mut_array = np.array([m[:min_length] for m in mut_list])
    size_array = np.array([s[:min_length] for s in size_list])
    time_array = np.array([t[:min_length] for t in time_list])

    avg_wt = np.mean(wt_array, axis=0)
    avg_mut = np.mean(mut_array, axis=0)
    avg_size = np.mean(size_array, axis=0)
    avg_time = np.mean(time_array, axis=0)

    sd_avg_wt = np.std(wt_array, axis=0, ddof=1)
    sd_avg_mut = np.std(mut_array, axis=0, ddof=1)

    se_avg_wt = sd_avg_wt / np.sqrt(mut_array.shape[0])
    se_avg_mut = sd_avg_mut / np.sqrt(mut_array.shape[0])

    with open("summary_results.txt", "w") as f:
        f.write("time\tavg_wt\tstderr_wt\tavg_mut\tstderr_mut\tavg_size\n")
        for i in range(min_length):
            f.write(f"{avg_time[i]:.5f}\t{avg_wt[i]:.5f}\t{se_avg_wt[i]:.5f}\t{avg_mut[i]:.5f}\t{se_avg_mut[i]:.5f}\t{avg_size[i]:.5f}\n")

    print("✅ Summary written to summary_results.txt")

if __name__ == "__main__":
    average_list()
'''
