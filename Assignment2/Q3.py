import random

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SIMULATION_CYCLES = 1_000_000

# Both queue types have the same mean arrival rate:
# D/Geo/1: one arrival every 2 cycles
# Geo/D/1: Bernoulli arrival probability 0.5 per cycle
ARRIVAL_RATE = 0.5
ARRIVAL_PERIOD = 2

MEAN_SERVICE_RATES = np.arange(0.5, 1.0 + 1e-9, 0.1)


def geometric_service_time(mean_service_rate):
    service_time = 1
    u = random.random()

    while u > mean_service_rate:
        service_time += 1
        u = random.random()

    return service_time


def simulate_d_geo_1(
    mean_service_rate,
    simulation_cycles,
    arrival_period=ARRIVAL_PERIOD,
):
    queue_length = 0
    service_remaining = 0
    occupancy_total = 0

    for cycle in range(simulation_cycles):

        if cycle % arrival_period == 0:
            queue_length += 1

        if service_remaining == 0 and queue_length > 0:
            queue_length -= 1
            service_remaining = geometric_service_time(mean_service_rate)

        occupancy_total += queue_length

        if service_remaining > 0:
            service_remaining -= 1

    return occupancy_total / simulation_cycles


def simulate_geo_d_1(
    arrival_rate,
    service_time,
    simulation_cycles,
):
    queue_length = 0
    service_remaining = 0
    occupancy_total = 0

    for _ in range(simulation_cycles):

        u = random.random()

        if u < arrival_rate:
            queue_length += 1

        if service_remaining == 0 and queue_length > 0:
            queue_length -= 1
            service_remaining = service_time

        occupancy_total += queue_length

        if service_remaining > 0:
            service_remaining -= 1

    return occupancy_total / simulation_cycles


def main():

    d_geo_1_occupancy = []

    print("D/Geo/1")
    print("-----------------------------")

    for mean_service_rate in MEAN_SERVICE_RATES:

        occupancy = simulate_d_geo_1(
            mean_service_rate,
            SIMULATION_CYCLES,
        )

        d_geo_1_occupancy.append(occupancy)

        print(
            f"mu = {mean_service_rate:.1f}, "
            f"mean service time = {1 / mean_service_rate:.3f}, "
            f"average occupancy = {occupancy:.4f}"
        )

    # Geo/D/1 with deterministic service time = 1
    geo_d_service_1 = simulate_geo_d_1(
        ARRIVAL_RATE,
        service_time=1,
        simulation_cycles=SIMULATION_CYCLES,
    )

    # Geo/D/1 with deterministic service time = 2
    geo_d_service_2 = simulate_geo_d_1(
        ARRIVAL_RATE,
        service_time=2,
        simulation_cycles=SIMULATION_CYCLES,
    )

    print("\nGeo/D/1")
    print("-----------------------------")

    print(
        f"lambda = 0.5, service time = 1, mu = 1.0: "
        f"average occupancy = {geo_d_service_1:.4f}"
    )

    print(
        f"lambda = 0.5, service time = 2, mu = 0.5: "
        f"average occupancy = {geo_d_service_2:.4f}"
    )

    # Plot
    plt.figure(figsize=(9, 6))

    plt.plot(
        MEAN_SERVICE_RATES,
        d_geo_1_occupancy,
        marker="o",
        linewidth=2,
        label="D/Geo/1 (arrival every 2 cycles)"
    )

    plt.scatter(
        [1.0],
        [geo_d_service_1],
        marker="s",
        s=80,
        label="Geo/D/1 (S = 1, lambda = 0.5)"
    )

    plt.scatter(
        [0.5],
        [geo_d_service_2],
        marker="^",
        s=80,
        label="Geo/D/1 (S = 2, lambda = 0.5)"
    )

    plt.xlabel("Mean Service Rate (mu)")
    plt.ylabel("Average Queue Occupancy")

    plt.title(
        "Average Queue Occupancy: D/Geo/1 vs Geo/D/1"
    )

    plt.xticks(MEAN_SERVICE_RATES)

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "Q3_plot.png",
        dpi=300
    )

    plt.close()


if __name__ == "__main__":
    main()