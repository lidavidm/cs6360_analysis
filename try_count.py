#!/usr/bin/env python3
import collections
import csv
import json
from scipy import stats

if __name__ == "__main__":
    level_tries = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    with open("try_count.tsv") as try_stats:
        try_stats = csv.reader(try_stats, delimiter="\t")

        # Discard the header
        next(try_stats)

        for (quest_id, user_id) in try_stats:
            level_tries[int(quest_id)][user_id] += 1

        print("x,y,yerr")
        for quest_id in sorted(level_tries):
            user_tries = list(level_tries[quest_id].values())
            _, _, mean, sample_variance, _, _ = stats.describe(user_tries)
            std_error = stats.sem(user_tries)
            print(quest_id + 1, ",", mean, ",", std_error, sep="")
