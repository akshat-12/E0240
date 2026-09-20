import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


SIMULATION_CYCLES = 1_000_000
INJECTION_RATES = np.arange(0.1, 0.51, 0.1)


def simulate_queue(injection_rate, service_time_sampler, simulation_cycles):
    """Return average waiting occupancy and server utilization."""
    queue_length = 0
    remaining_service_time = 0
    occupancy_total = 0
    busy_cycles = 0

    for _ in range(simulation_cycles):
        u1 = random.random()
        if u1 < injection_rate:
            queue_length += 1

        if remaining_service_time == 0 and queue_length > 0:
            queue_length -= 1
            remaining_service_time = service_time_sampler()

        if remaining_service_time > 0:
            busy_cycles += 1
            remaining_service_time -= 1

        occupancy_total += queue_length

    return (
        occupancy_total / simulation_cycles,
        busy_cycles / simulation_cycles,
    )


def random_service_time():
    u1 = random.random()
    if u1 < 1 / 3:
        return 1
    elif u1 < 2 / 3:
        return 2
    else:
        return 3


def deterministic_service_time():
    return 2


def run_simulation():
    random_service_occupancy = []
    deterministic_occupancy = []
    random_service_utilization = []
    deterministic_utilization = []

    for injection_rate in INJECTION_RATES:
        random_result = simulate_queue(
            injection_rate,
            random_service_time,
            SIMULATION_CYCLES,
        )
        deterministic_result = simulate_queue(
            injection_rate,
            deterministic_service_time,
            SIMULATION_CYCLES,
        )

        random_service_occupancy.append(random_result[0])
        random_service_utilization.append(random_result[1])
        deterministic_occupancy.append(deterministic_result[0])
        deterministic_utilization.append(deterministic_result[1])

        print(
            f"λ={injection_rate:.1f} | "
            f"Geo/{{1,2,3}}/1 occupancy={random_result[0]:.4f}, "
            f"utilization={random_result[1]:.4f} | "
            f"Geo/D/1 occupancy={deterministic_result[0]:.4f}, "
            f"utilization={deterministic_result[1]:.4f}"
        )

    return (
        np.array(random_service_occupancy),
        np.array(deterministic_occupancy),
        np.array(random_service_utilization),
        np.array(deterministic_utilization),
    )


def plot_results(results):
    random_occupancy, deterministic_occupancy, _, _ = results

    figure, axis = plt.subplots(figsize=(9, 6))
    axis.plot(
        INJECTION_RATES,
        random_occupancy,
        marker="o",
        linewidth=2,
        label="Geo/{1, 2, 3}/1 service",
    )
    axis.plot(
        INJECTION_RATES,
        deterministic_occupancy,
        marker="s",
        linewidth=2,
        label="Geo/D/1 service time 2",
    )
    axis.set_xlabel("Injection rate λ (packets/cycle)")
    axis.set_ylabel("Average queue occupancy")
    axis.set_title("Geo/G/1 versus Geo/D/1 with 1,000,000 cycles")
    axis.set_xticks(INJECTION_RATES)
    axis.grid(True, alpha=0.3)
    axis.legend()

    # Zoom into the stable, lower-occupancy rates without hiding the rate 0.5 result.
    inset = axis.inset_axes([0.12, 0.48, 0.42, 0.42])
    inset.plot(INJECTION_RATES[:4], random_occupancy[:4], "o-", linewidth=1.5)
    inset.plot(
        INJECTION_RATES[:4],
        deterministic_occupancy[:4],
        "s-",
        linewidth=1.5,
    )
    low_values = np.concatenate(
        (random_occupancy[:4], deterministic_occupancy[:4])
    )
    inset.set_xlim(0.08, 0.42)
    inset.set_ylim(0, max(low_values) * 1.2)
    inset.set_xticks(INJECTION_RATES[:4])
    inset.grid(True, alpha=0.3)
    inset.set_title("Low occupancy detail", fontsize=9)
    mark_inset(axis, inset, loc1=2, loc2=4, fc="none", ec="0.5")

    figure.tight_layout()
    figure.savefig("Q2_plot.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    simulation_results = run_simulation()
    plot_results(simulation_results)