import os
import random

def trace_generator(simulation_length, injection_rate, file_name):
    parent_directory = os.path.dirname(file_name)
    if parent_directory:
        os.makedirs(parent_directory, exist_ok=True)

    with open(file_name, "w") as f:
        for cycle in range(simulation_length):
            if random.random() <= injection_rate:
                f.write(f"0 1 {cycle}\n")

def generate_traces():
    simulation_length = 100000
    injection_rate = [rate / 10 for rate in range(1, 11, 1)]

    for rate in injection_rate:
        file_name = f"traces/trace_{rate}.txt"
        print(f"Generating trace for injection rate: {rate}")
        print(f"Trace file: {file_name}")
        trace_generator(simulation_length, rate, file_name)

if __name__ == "__main__":
    generate_traces()