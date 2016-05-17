#!/usr/bin/env python3
import csv
import json
from scipy import stats

if __name__ == "__main__":
    completion_times = []
    with open("completion_time.tsv") as completion_stats:
        completion_stats = csv.reader(completion_stats, delimiter="\t")

        # Discard the header
        next(completion_stats)

        for (user_id, time) in completion_stats:
            completion_times.append(int(time))

        _, _, mean, sample_variance, _, _ = stats.describe(completion_times)

        print("Mean completion time (seconds):", mean)
        print("Sample variance completion time:", sample_variance)
