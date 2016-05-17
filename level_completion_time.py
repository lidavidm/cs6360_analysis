#!/usr/bin/env python3
import collections
import csv
import json
from scipy import stats

if __name__ == "__main__":
    level_completion_times = collections.defaultdict(list)
    with open("level_completion_time.tsv") as completion_stats:
        completion_stats = csv.reader(completion_stats, delimiter="\t")

        # Discard the header
        next(completion_stats)

        for (quest_id, user_id, time) in completion_stats:
            level_completion_times[int(quest_id)].append(int(time))

        for quest_id in sorted(level_completion_times):
            completion_times = level_completion_times[quest_id]
            _, _, mean, sample_variance, _, _ = stats.describe(completion_times)

            print("Level", quest_id + 1)
            print("Mean completion time (seconds):", mean)
            print("Sample variance completion time:", sample_variance)

        print("Level", ",", "Mean Completion Time (minutes)")
        for quest_id in sorted(level_completion_times):
            completion_times = level_completion_times[quest_id]
            _, _, mean, sample_variance, _, _ = stats.describe(completion_times)
            print(quest_id + 1, ",", mean / 60.0)
