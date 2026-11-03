
import random
import math


def simulate_slotted_aloha(offered_load, total_slots=10000, seed=42):

    if offered_load <= 0:
        raise ValueError("Offered load must be positive")

    rng = random.Random(seed)

    successful_frames = 0
    collided_slots = 0
    idle_slots = 0
    total_attempts = 0

    for slot in range(total_slots):

        # Generate Poisson-distributed attempts
        threshold = math.exp(-offered_load)
        product = 1.0
        attempts = 0

        while product > threshold:
            product *= rng.random()
            attempts += 1

        attempts -= 1
        total_attempts += attempts

        if attempts == 0:
            idle_slots += 1

        elif attempts == 1:
            successful_frames += 1

        else:
            collided_slots += 1

    return {
        "attempts": total_attempts,
        "successes": successful_frames,
        "collisions": collided_slots,
        "idle_slots": idle_slots,
        "throughput": successful_frames / total_slots
    }
