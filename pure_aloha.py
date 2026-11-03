
import random


def simulate_pure_aloha(offered_load, total_frames=10000, seed=42):

    if offered_load <= 0:
        raise ValueError("Offered load must be positive")

    rng = random.Random(seed)

    simulation_time = total_frames / offered_load

    transmission_times = sorted(
        rng.uniform(0, simulation_time)
        for _ in range(total_frames)
    )

    successful_frames = 0
    collided_frames = 0

    for i in range(total_frames):

        previous_collision = (
            i > 0 and
            transmission_times[i] - transmission_times[i - 1] < 1
        )

        next_collision = (
            i < total_frames - 1 and
            transmission_times[i + 1] - transmission_times[i] < 1
        )

        if previous_collision or next_collision:
            collided_frames += 1
        else:
            successful_frames += 1

    throughput = successful_frames / simulation_time

    # Return all statistics as a dictionary
    return {
        "attempts": total_frames,
        "successes": successful_frames,
        "collisions": collided_frames,
        "throughput": throughput
    }
