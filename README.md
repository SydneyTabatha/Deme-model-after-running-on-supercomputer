So here is how I do it. Let’s forget running things in parallel for a moment. Consider one program that you run. The way you have done it so far is that you run it and determine the number of mutants at the specified population size N. Now within that same program, you can perform this in a loop. Every time it reaches population size N, I write into a file the number of mutants for that run. Then I start the next iteration of the loop, again initializing all populations and starting a second, independent run. When this reaches size N, I again output the number of mutants into the file. Then you start the next iteration of the loop and perform the third run, and so on. Once you have done M runs, you end the program. M should be chosen such that M runs can be completed within a reasonable period of time. This is how long your processes will run.

As. a result of this, you will have a file that looks like this

23
34
68
765
1
343
35
etc

this would be the number of mutants at population size N for each iteration of the loop.

Now, let’s go back to parallel

let’s say your loop makes M=100 iterations

Now if you run 1024 instances of this program in parallel on the cluster, then at the end of this, you will have 1024 different files each containing the number of mutants for 100 runs. So you have 100x1024 runs altogether = 102400 iterations.

The important part is that each instance of the program that you start with slurm must write its results to a different file, which you can call e.g. x1.dat, x2.dat, x3.dat, x1024.dat

This can be achieved as follows. Your program should be able to take a command line argument when you start it. With me, my compiled program is called a.out. So when I start the program on the linux command line, I can intitiate it as ./a.out x1.dat

In the program you need to take that command line argument “x1.dat” as a string and open a file that is called that.

This will initiate the first instance of the program, which writes the results into x1.dat

The second instance will be ./a.out x2.dat

the third instance ./a.out x3.dat, and so on.

In python, you don’ have executables (a.out), but there must be something similar.

Then you can write a slurm script, which starts 1024 instances, each instance writing to its unique file.

Once everyting is complete, you can write a simple script to read in all the data from all the files and calculate the average

If during any iteration of the loop within a program, something goes extinct, you simply stop this iteration of the loop with no output and start the next iteration.

#!/bin/bash
#SBATCH --job-name=my_parallel_job   # Name of the job
#SBATCH --output=output_%A_%a.outt   # Output file (%A = job ID, %a = array index)
#SBATCH --error=error_%A_%a.err    # Error file (%A = job ID, %a = array index)
#SBATCH --array=1-1024         # Array range (1 to 600)
#SBATCH --ntasks=1           # Each task runs one instance of the program
#SBATCH --cpus-per-task=1       # Each task uses 1 CPU core
# Output file pattern
OUTPUT_FILE=“x${SLURM_ARRAY_TASK_ID}.dat”
DELAY=$(echo “${SLURM_ARRAY_TASK_ID} * 0.01" | bc -l) # 10 ms increments
sleep ${DELAY}
# Run the program and write results to the corresponding output file
./zomb1.out ${OUTPUT_FILE}

This is the slurm script that I use

The executable here is no called a.out, but zomb1.out

The line: OUTPUT_FILE=“x${SLURM_ARRAY_TASK_ID}.dat”     defines the output files. x1.dat, x2.dat, x3,dat…. x1024.dat

./zomb1.out ${OUTPUT_FILE}.   initiates each instance of the program, taking its unique file name as a command line argument.

you start this script by running: sbatch run-x-1024.sbatch, where run-x-1024.sbatch is the file with the slurm script

if you want to force quite what is running, then enter the command scancel -u username
