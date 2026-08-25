import csv
import os
import random
import re
import shutil
import subprocess

import matplotlib.pyplot as plt


NUM_RUNS = 1
SIMULATION_LENGTH = 10000
INJECTION_RATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
LATENCY_PATTERN = re.compile(
    r"Packet latency average\s*=\s*([0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?)"
)


def generate_trace(simulation_length, injection_rate, file_name):
    parent_directory = os.path.dirname(file_name)
    if parent_directory:
        os.makedirs(parent_directory, exist_ok=True)

    with open(file_name, "w") as output:
        for cycle in range(simulation_length):
            if random.random() <= injection_rate:
                output.write(f"0 1 {cycle}\n")


def generate_traces(project_directory):
    traces_directory = os.path.join(project_directory, "traces")
    for rate in INJECTION_RATES:
        trace_file = os.path.join(traces_directory, f"trace_{rate}.txt")
        print(f"Generating trace for injection rate: {rate}")
        print(f"Trace file: {trace_file}")
        generate_trace(SIMULATION_LENGTH, rate, trace_file)


def collect_latencies(project_directory):
    booksim_directory = os.path.join(project_directory, "booksim", "src")
    trace_destination = os.path.join(booksim_directory, "trace_file.txt")
    booksim_executable = os.path.join(booksim_directory, "booksim")
    results_file = os.path.join(project_directory, "q3_packet_latency.csv")

    if os.path.exists(results_file):
        os.remove(results_file)

    file_is_empty = not os.path.exists(results_file) or os.path.getsize(results_file) == 0
    if not file_is_empty:
        with open(results_file, "rb") as existing_output:
            existing_output.seek(-1, os.SEEK_END)
            if existing_output.read(1) != b"\n":
                with open(results_file, "a") as newline_output:
                    newline_output.write("\n")

    with open(results_file, "a", newline="") as output:
        writer = csv.writer(output)
        if file_is_empty:
            writer.writerow(["injection_rate", "average_packet_latency"])
            output.flush()

        for run_number in range(1, NUM_RUNS + 1):
            print(f"Starting BookSim run {run_number}/{NUM_RUNS}")
            for rate in INJECTION_RATES:
                trace_file = os.path.join(project_directory, f"traces/trace_{rate}.txt")
                shutil.copyfile(trace_file, trace_destination)
                print(f"Running BookSim for injection rate: {rate}")
                result = subprocess.run(
                    [booksim_executable, "mesh_config_trace_based"],
                    cwd=booksim_directory,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(result.stdout, end="", flush=True)

                if result.returncode not in (0, -1, 255):
                    raise subprocess.CalledProcessError(
                        result.returncode,
                        result.args,
                        output=result.stdout,
                        stderr=result.stderr,
                    )

                match = LATENCY_PATTERN.search(result.stdout)
                if match is None:
                    raise RuntimeError(
                        f"Numeric packet latency was not found for injection rate {rate}"
                    )

                latency = float(match.group(1))
                writer.writerow([rate, latency])
                output.flush()
                print(f"Injection rate: {rate}, average packet latency: {latency}")

    print(f"Latency data written to {results_file}")
    return results_file


def plot_latencies(project_directory):
    results_file = os.path.join(project_directory, "q3_packet_latency.csv")
    plot_file = os.path.join(project_directory, "q3_packet_latency.png")
    injection_rates = []
    average_latencies = []

    with open(results_file, newline="") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            injection_rates.append(float(row["injection_rate"]))
            average_latencies.append(float(row["average_packet_latency"]))

    figure, axes = plt.subplots()
    axes.plot(injection_rates, average_latencies, "o-", linewidth=2)
    axes.set_xlabel("Injection Rate (packets/cycle)")
    axes.set_ylabel("Average Packet Latency (cycles)")
    axes.set_title("Average Packet Latency vs Injection Rate")
    axes.grid(True)
    figure.tight_layout()
    figure.savefig(plot_file)
    print(f"Plot written to {plot_file}")
    plt.show()


def main():
    project_directory = os.path.dirname(os.path.abspath(__file__))
    generate_traces(project_directory)
    collect_latencies(project_directory)
    plot_latencies(project_directory)


if __name__ == "__main__":
    main()
