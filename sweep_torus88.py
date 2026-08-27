#!/usr/bin/env python3
import csv
import os
import re
import subprocess

# Configuration
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKSIM_SRC = os.path.join(PROJECT_DIR, "booksim", "src")
BOOKSIM_EXE = os.path.join(BOOKSIM_SRC, "booksim")
CONFIG_FILE = "examples/torus88"
RESULTS_CSV = os.path.join(PROJECT_DIR, "q3_packet_latency_torus88.csv")
PLOT_FILE = os.path.join(PROJECT_DIR, "q3_packet_latency_torus88.png")

# Sweep parameters
rates = [round(i * 0.01, 2) for i in range(1, 11)]  # 0.01 .. 0.10
SAMPLE_PERIOD = 1000000

LATENCY_RE = re.compile(r"Packet latency average\s*=\s*([0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?)")


def run_rate(rate):
    args = [BOOKSIM_EXE, CONFIG_FILE, f"injection_rate={rate}", f"sample_period={SAMPLE_PERIOD}"]
    print(f"Running: {' '.join(args)} (cwd={BOOKSIM_SRC})")
    proc = subprocess.run(args, cwd=BOOKSIM_SRC, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    # Find last latency match
    matches = LATENCY_RE.findall(out)
    if not matches:
        print("--- Simulator output (truncated) ---")
        print(out[-4000:])
        raise RuntimeError(f"Packet latency average not found for rate {rate}")
    latency = float(matches[-1])
    print(f"Rate {rate}: latency {latency}")
    return latency


def main():
    file_is_empty = not os.path.exists(RESULTS_CSV) or os.path.getsize(RESULTS_CSV) == 0
    with open(RESULTS_CSV, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if file_is_empty:
            writer.writerow(["injection_rate", "average_packet_latency"])
            csvfile.flush()

        for r in rates:
            latency = run_rate(r)
            writer.writerow([r, latency])
            csvfile.flush()

    # Create plot (optional, requires matplotlib)
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        rates_list = []
        lat_list = []
        with open(RESULTS_CSV, newline="") as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                rates_list.append(float(row["injection_rate"]))
                lat_list.append(float(row["average_packet_latency"]))
        plt.figure()
        plt.plot(rates_list, lat_list, "o-", linewidth=2)
        plt.xlabel("Injection Rate (packets/cycle)")
        plt.ylabel("Average Packet Latency (cycles)")
        plt.title("Average Packet Latency vs Injection Rate (torus88)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(PLOT_FILE)
        print(f"Plot saved to {PLOT_FILE}")
    except Exception as e:
        print(f"Skipping plot: {e}")


if __name__ == '__main__':
    main()
