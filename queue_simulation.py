import random
import matplotlib.pyplot as plt

# geo/D/1 queue simulation
# geo = geometric arrival process
# D = deterministic service time
# 1 = single server
def single_queue_simulation_geo_d_1(injection_rate, service_time, simulation_length):

    # initialization of state variables
    occupancy_counter = 0
    num_arrivals = 0
    utilization_counter = 0
    is_server_busy = 0
    current_occupancy = 0
    remaining_service_time = 0

    # simulation

    for cycle in range(simulation_length):

        # arrival routine
        if random.random() <= injection_rate:
            current_occupancy = current_occupancy + 1
            num_arrivals = num_arrivals + 1
        
        # service routine
        if is_server_busy == 1:
            remaining_service_time = remaining_service_time - 1
            if remaining_service_time == 0:
                is_server_busy = 0
        
        # putting a packet in the server
        if is_server_busy == 0 and current_occupancy > 0:
            is_server_busy = 1
            current_occupancy = current_occupancy - 1
            remaining_service_time = service_time
        
        # updating the counters
        occupancy_counter = occupancy_counter + current_occupancy
        if is_server_busy == 1:
            utilization_counter = utilization_counter + 1
        
        assert occupancy_counter >=0, "Error in occupany_counter"
        assert current_occupancy >=0, "Error in current_occupany"

    average_occupancy = occupancy_counter / simulation_length
    average_utilization = utilization_counter / simulation_length

    return average_occupancy, average_utilization

# Simulation for Q1
def Q1():

    service_time = 2
    injection_rate_array = [rate / 100 for rate in range(5, 50, 5)] + [0.49]
    simulation_lengths = [100, 10000, 1000000, 100000000]
    average_occupancy = {}
    average_utilization = {}
    markers = ["o", "s", "^", "D"]

    for simulation_length in simulation_lengths:
        occupancy_for_length = []
        utilization_for_length = []
        for injection_rate in injection_rate_array:
            occupancy, utilization = single_queue_simulation_geo_d_1(
                injection_rate, service_time, simulation_length
            )
            occupancy_for_length.append(occupancy)
            utilization_for_length.append(utilization)
        average_occupancy[simulation_length] = occupancy_for_length
        average_utilization[simulation_length] = utilization_for_length

    figure, axes = plt.subplots()
    for simulation_length, marker in zip(simulation_lengths, markers):
        axes.plot(
            injection_rate_array,
            average_occupancy[simulation_length],
            marker=marker,
            linestyle="--",
            linewidth=2,
            markersize=8,
            label=f"Simulation length = {simulation_length:,}",
        )
    axes.legend(loc="upper left", fontsize=10)
    axes.set_xlabel(
        "Injection Rate (packets/cycle)",
        fontsize=12,
        fontweight="bold",
    )
    axes.set_ylabel("Average Occupancy", fontsize=12, fontweight="bold")
    axes.set_title(
        "Plot of Average Occupany vs injection rate as simulation lengths vary"
    )
    axes.grid(True)
    axes.spines["top"].set_visible(True)
    axes.spines["right"].set_visible(True)
    figure.tight_layout()
    plt.show()

    return injection_rate_array, average_occupancy, average_utilization

# geo/geo/1 queue simulation
# geo = geometric arrival process
# geo = geometric service time
# 1 = single server
def single_queue_simulation_geo_geo_1(injection_rate, mean_service_time, simulation_length):

    # initialization of state variables
    occupancy_counter = 0
    num_arrivals = 0
    utilization_counter = 0
    is_server_busy = 0
    current_occupancy = 0

    # simulation

    for cycle in range(simulation_length):

        # arrival routine
        if random.random() <= injection_rate:
            current_occupancy = current_occupancy + 1
            num_arrivals = num_arrivals + 1
        
        # service routine
        if is_server_busy == 1:
            if random.random() <= 1 / mean_service_time:
                is_server_busy = 0
        
        # putting a packet in the server
        if is_server_busy == 0 and current_occupancy > 0:
            is_server_busy = 1
            current_occupancy = current_occupancy - 1
        
        # updating the counters
        occupancy_counter = occupancy_counter + current_occupancy
        if is_server_busy == 1:
            utilization_counter = utilization_counter + 1
        
        assert occupancy_counter >=0, "Error in occupany_counter"
        assert current_occupancy >=0, "Error in current_occupany"

    average_occupancy = occupancy_counter / simulation_length
    average_utilization = utilization_counter / simulation_length

    return average_occupancy, average_utilization

# Simulation for Q2
def Q2():

    mean_service_time = 2
    injection_rate_array = [rate / 100 for rate in range(5, 50, 5)] + [0.49]
    simulation_length = 100000000
    deterministic_occupancy = []
    geometric_occupancy = []

    for injection_rate in injection_rate_array:
        deterministic_result = single_queue_simulation_geo_d_1(
            injection_rate, mean_service_time, simulation_length
        )
        geometric_result = single_queue_simulation_geo_geo_1(
            injection_rate, mean_service_time, simulation_length
        )
        deterministic_occupancy.append(deterministic_result[0])
        geometric_occupancy.append(geometric_result[0])

    figure, axes = plt.subplots()
    axes.plot(
        injection_rate_array,
        deterministic_occupancy,
        marker="o",
        linestyle="--",
        linewidth=2,
        markersize=8,
        label="Deterministic service",
    )
    axes.plot(
        injection_rate_array,
        geometric_occupancy,
        marker="s",
        linestyle="--",
        linewidth=2,
        markersize=8,
        label="Geometric service",
    )
    axes.legend(loc="upper left", fontsize=10)
    axes.set_xlabel(
        "Injection Rate (packets/cycle)",
        fontsize=12,
        fontweight="bold",
    )
    axes.set_ylabel("Average Occupancy", fontsize=12, fontweight="bold")
    axes.set_title(
        "Average Occupancy vs Injection Rate for Two Service Models"
    )
    axes.grid(True)
    axes.spines["top"].set_visible(True)
    axes.spines["right"].set_visible(True)
    figure.tight_layout()
    plt.show()

    return injection_rate_array, deterministic_occupancy, geometric_occupancy


if __name__ == "__main__":
    Q2()