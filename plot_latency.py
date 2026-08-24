import csv
import os

import matplotlib.pyplot as plt


def plot_latencies():
    project_directory = os.path.dirname(os.path.abspath(__file__))
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


if __name__ == "__main__":
    plot_latencies()