#!/usr/bin/python
# python run_booksim.py <directory to injection file>


import os, re, glob, sys, math

# Extract command line arguments
# trace_file_dir = sys.argv[1] #directory name
# mesh_size = sys.argv[2] #mesh_size
# israndom_trace = sys.argv[3] #is random trace
# israndom_trace = int(israndom_trace) 


# Initialize dictionary to hold latency values
area_dict = dict()
power_dict = dict()

# Get a list of all files in directory
#files = glob.glob(trace_file_dir + '/*txt')

# Initialize file counter
file_counter = 0

# Create directory to store config files
os.system('mkdir -p ./logs/configs')

mesh_size = [2, 4, 6, 8, 10, 12, 14, 18, 20, 22, 24, 26, 28, 30]
#mesh_size = [2, 4, 6]

# Iterate over all files
for size in mesh_size :

    # Increment file counter
    file_counter += 1

    #print('[ INFO] Processing file ' + file + ' ...')

    # Extract file name without extension and absolute path from filename
    run_name = str(size)
    
    # Extract first line of file
    #line1 = os.popen('head -1 ' + file).read()

    # Extract size of mesh
    #line1  = line1.strip()
    #values = line1.split()
    #size   = int(math.sqrt(len(values)))
    
    # Open read file handle of config file
    fp = open('./mesh_config_dummy', 'r')

    # Set path to config file
    config_file = './logs/configs/' + run_name + '_mesh_config'

    # Open write file handle for config file
    outfile = open(config_file, 'w')

    # Iterate over file and set size of mesh in config file
    for line in fp :
        
        line = line.strip()
        
        # Search for pattern
        matchobj = re.match(r'^k=', line)

        # Set size of mesh if line in file corresponds to mesh size
        if matchobj :
            line = 'k=' + str(size) + ';'

        # Write config to file
        outfile.write(line + '\n')

    # Close file handles
    fp.close()
    outfile.close()

    # Set path to log file
    log_file = './logs/' + run_name + '.log'

    # Copy injection rate matrix file
    #os.system('cp ' + file + ' ./trace_file.txt')

    # Run Booksim with config file and save log
    booksim_command = './booksim ' + config_file + ' > ' + log_file
    os.system(booksim_command)

    # Grep for packet latency average from log file
    #latency = os.popen('grep "Packet latency average" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()
    #latency = os.popen('grep "Trace is finished in" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()
    power = os.popen('grep "Total Power" ' + log_file + ' | tail -1 | awk \'{print $4}\'').read().strip()

    print('[ INFO] Power: ' + power +'\n')

    # Add key, value to dictionary
    power_dict[run_name] = power

    area = os.popen('grep "Total Area" ' + log_file + ' | tail -1 | awk \'{print $4}\'').read().strip()

    print('[ INFO] Area: ' + area +'\n')

    # Add key, value to dictionary
    area_dict[run_name] = area
    # Stop if 3 files are read
    #if file_counter == 3:
    #    break

# Open output file handle
outfile_area = open('./logs/area_mesh.csv', 'w')
outfile_power = open('./logs/power_mesh.csv', 'w')


# Write latencies to CSV
for size in mesh_size :
    run_name = str(size)
    outfile_area.write(area_dict[run_name] + '\n')
    outfile_power.write(power_dict[run_name] + '\n')

outfile_area.close()
outfile_power.close()
