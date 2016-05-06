#!/usr/bin/env python3
import csv
import json

ANSWER_KEY = [
    "The student sleeps like a Person",
    "tweety = Bird()",
    "robot.turnLeft()\\nrobot.moveForward()\\nrobot.moveForward()"
    "awooo!",
    "(none of these cause an error)",
]

if __name__ == "__main__":
    pretest_answers = {}
    posttest_answers = {}

    with open("pretest.tsv") as pretest, open("posttest.tsv") as posttest:
        pretest = csv.reader(pretest, delimiter="\t")
        posttest = csv.reader(posttest, delimiter="\t")

        # Discard the headers
        next(pretest)
        next(posttest)

        for row in pretest:
            user_id = row[0]
            answers = json.loads(row[1])
            answers[2] = answers[2]["code"] if isinstance(answers[2], dict) else answers[2]
            pretest_answers[user_id] = answers

        for row in posttest:
            user_id = row[0]
            answers = json.loads(row[1])
            posttest_answers[user_id] = answers

        for user_id, post_answers in posttest_answers.items():
            pre_answers = pretest_answers.get(user_id)
            if not pre_answers:
                print("No pretest for", user_id)
                continue

            pre_score = sum(1 for response, truth in zip(pre_answers, ANSWER_KEY) if response == truth)
            post_score = sum(1 for response, truth in zip(post_answers, ANSWER_KEY) if response == truth)

            print("User ID:", user_id)
            print("Pretest score:", pre_score)
            print("Posttest score:", post_score)
