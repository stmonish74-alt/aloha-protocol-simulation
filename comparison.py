
import matplotlib.pyplot as plt
import csv
import os
import math

from pure_aloha import simulate_pure_aloha
from slotted_aloha import simulate_slotted_aloha


def main():

    os.makedirs("results", exist_ok=True)

    traffic_loads = [
        0.1, 0.2, 0.3, 0.4, 0.5,
        0.6, 0.7, 0.8, 0.9, 1.0,
        1.1, 1.2, 1.3, 1.4, 1.5,
        1.6, 1.7, 1.8, 1.9, 2.0
    ]

    pure_results = []
    slotted_results = []

    print("\n==========================================")
    print("       ALOHA PROTOCOL COMPARISON")
    print("==========================================")

    print(
        f"{'Load':<8}"
        f"{'Pure S':<15}"
        f"{'Slotted S':<15}"
        f"{'Pure Success':<15}"
        f"{'Slotted Success':<17}"
    )

    print("-" * 70)

    for index, load in enumerate(traffic_loads):

        pure = simulate_pure_aloha(
            load,
            total_frames=10000,
            seed=100 + index
        )

        slotted = simulate_slotted_aloha(
            load,
            total_slots=10000,
            seed=200 + index
        )

        pure_results.append(pure)
        slotted_results.append(slotted)

        print(
            f"{load:<8.1f}"
            f"{pure['throughput']:<15.4f}"
            f"{slotted['throughput']:<15.4f}"
            f"{pure['successes']:<15}"
            f"{slotted['successes']:<17}"
        )

    # Save results in CSV
    with open(
        "results/aloha_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Offered Load",
            "Pure Attempts",
            "Pure Successes",
            "Pure Collisions",
            "Pure Throughput",
            "Slotted Attempts",
            "Slotted Successes",
            "Slotted Collisions",
            "Slotted Throughput"
        ])

        for i, load in enumerate(traffic_loads):

            p = pure_results[i]
            s = slotted_results[i]

            writer.writerow([
                load,
                p["attempts"],
                p["successes"],
                p["collisions"],
                p["throughput"],
                s["attempts"],
                s["successes"],
                s["collisions"],
                s["throughput"]
            ])

    # Generate throughput graph
   
    # Generate throughput graph

    pure_throughput = [
        r["throughput"] for r in pure_results
    ]

    slotted_throughput = [
        r["throughput"] for r in slotted_results
    ]

    # Theoretical throughput calculations

    pure_theoretical = [
        g * math.exp(-2 * g)
        for g in traffic_loads
    ]

    slotted_theoretical = [
        g * math.exp(-g)
        for g in traffic_loads
    ]

    # Plot all four curves

    plt.figure(figsize=(10, 6))

    plt.plot(
        traffic_loads,
        pure_throughput,
        marker="o",
        label="Pure ALOHA Simulation"
    )

    plt.plot(
        traffic_loads,
        slotted_throughput,
        marker="s",
        label="Slotted ALOHA Simulation"
    )

    plt.plot(
        traffic_loads,
        pure_theoretical,
        linestyle="--",
        label="Pure ALOHA Theory"
    )

    plt.plot(
        traffic_loads,
        slotted_theoretical,
        linestyle="--",
        label="Slotted ALOHA Theory"
    )

    plt.xlabel("Offered Traffic Load (G)")
    plt.ylabel("Throughput (S)")
    plt.title("Pure ALOHA vs Slotted ALOHA Throughput")

    plt.legend()
    plt.grid(True)

    plt.savefig(
        "results/throughput_comparison.png",
        dpi=300
    )

    plt.show()

    print("\n==========================================")
    print("SIMULATION COMPLETED SUCCESSFULLY")
    print("==========================================")

    print("CSV saved: results/aloha_results.csv")
    print("Graph saved: results/throughput_comparison.png")


if __name__ == "__main__":
    main()
