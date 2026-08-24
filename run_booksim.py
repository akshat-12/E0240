import csv
import os
import re
import shutil
import subprocess


NUM_RUNS = 1


def collect_latencies():
    project_directory = os.path.dirname(os.path.abspath(__file__))
    booksim_directory = os.path.join(project_directory, "booksim", "src")
    trace_destination = os.path.join(booksim_directory, "trace_file.txt")
    booksim_executable = os.path.join(booksim_directory, "booksim")
    config_file = "mesh_config_trace_based"
    injection_rates = [0.2]
    latency_pattern = re.compile(
        r"Packet latency average\s*=\s*([0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?)"
    )
    results_file = os.path.join(project_directory, "q3_packet_latency.csv")

    file_is_empty = not os.path.exists(results_file) or os.path.getsize(results_file) == 0
    with open(results_file, "a", newline="") as output:
        writer = csv.writer(output)
        if file_is_empty:
            writer.writerow(["injection_rate", "average_packet_latency"])
            output.flush()

        for run_number in range(1, NUM_RUNS + 1):
            print(f"Starting BookSim run {run_number}/{NUM_RUNS}")
            for rate in injection_rates:
                trace_file = os.path.join(project_directory, f"traces/trace_{rate}.txt")
                shutil.copyfile(trace_file, trace_destination)
                print(f"Running BookSim for injection rate: {rate}")
                result = subprocess.run(
                    [booksim_executable, config_file],
                    cwd=booksim_directory,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(result.stdout, end="", flush=True)

                if result.returncode not in (-1, 255):
                    raise subprocess.CalledProcessError(
                        result.returncode,
                        result.args,
                        output=result.stdout,
                        stderr=result.stderr,
                    )

                match = latency_pattern.search(result.stdout)
                if match is None:
                    raise RuntimeError(
                        f"Numeric packet latency was not found for injection rate {rate}"
                    )

                latency = float(match.group(1))
                writer.writerow([rate, latency])
                output.flush()
                print(f"Injection rate: {rate}, average packet latency: {latency}")

    print(f"Latency data written to {results_file}")


if __name__ == "__main__":
    collect_latencies()