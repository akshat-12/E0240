import csv
import os
import re
import subprocess

import matplotlib.pyplot as plt


INJECTION_RATES = [rate / 100 for rate in range(1, 11)]
LATENCY_PATTERN = re.compile(
    r"Packet latency average\s*=\s*([0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?)"
)
INJECTION_RATE_PATTERN = re.compile(
    r"^(\s*injection_rate\s*=\s*)[^;\n]+(;?.*)$", re.MULTILINE
)


def run_simulations():
    project_directory = os.path.dirname(os.path.abspath(__file__))
    booksim_directory = os.path.join(project_directory, "booksim", "src")
    config_path = os.path.join(booksim_directory, "examples", "torus88")
    executable_path = os.path.join(booksim_directory, "booksim")
    results_path = os.path.join(project_directory, "torus88_packet_latency.csv")
    plot_path = os.path.join(project_directory, "torus88_packet_latency.png")

    with open(config_path, "r") as config_file:
        config_template = config_file.read()

    if INJECTION_RATE_PATTERN.search(config_template) is None:
        raise RuntimeError(f"injection_rate setting not found in {config_path}")

    if os.path.exists(results_path):
        os.remove(results_path)

    injection_rates = []
    average_latencies = []

    with open(results_path, "a", newline="") as results_file:
        writer = csv.writer(results_file)
        writer.writerow(["injection_rate", "average_packet_latency"])
        results_file.flush()

        for injection_rate in INJECTION_RATES:
            config_contents = INJECTION_RATE_PATTERN.sub(
                rf"\g<1>{injection_rate}\g<2>", config_template, count=1
            )
            with open(config_path, "w") as config_file:
                config_file.write(config_contents)

            print(f"Running BookSim for injection rate: {injection_rate}")
            result = subprocess.run(
                [executable_path, "examples/torus88"],
                cwd=booksim_directory,
                capture_output=True,
                text=True,
                check=False,
            )
            print(result.stdout, end="", flush=True)
            if result.stderr:
                print(result.stderr, end="", flush=True)

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
                    f"Average packet latency was not found for injection rate "
                    f"{injection_rate}"
                )

            latency = float(match.group(1))
            injection_rates.append(injection_rate)
            average_latencies.append(latency)
            writer.writerow([injection_rate, latency])
            results_file.flush()
            print(f"Average packet latency: {latency}")

    figure, axes = plt.subplots()
    axes.plot(injection_rates, average_latencies, "o-", linewidth=2)
    axes.set_xlabel("Injection Rate (packets/cycle)")
    axes.set_ylabel("Average Packet Latency (cycles)")
    axes.set_title("Torus88 Average Packet Latency vs Injection Rate")
    axes.grid(True)
    figure.tight_layout()
    figure.savefig(plot_path)
    print(f"Latency data written to {results_path}")
    print(f"Plot written to {plot_path}")
    plt.show()


if __name__ == "__main__":
    run_simulations()
