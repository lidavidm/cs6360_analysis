#!/usr/bin/env python3
import csv
import json
from scipy import stats

ANSWER_KEY = [
    "The student sleeps like a Person",
    "tweety = Bird()",
    "robot.turnLeft()\nrobot.moveForward()\nrobot.moveForward()",
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
            answers[2] = answers[2]["code"] if isinstance(answers[2], dict) else answers[2]
            posttest_answers[user_id] = answers

        pre_score_list = []
        post_score_list = []
        for user_id, post_answers in posttest_answers.items():
            pre_answers = pretest_answers.get(user_id)
            if not pre_answers:
                print "\nNo pretest for " + user_id
                continue

            pre_score = sum(1 for response, truth in zip(pre_answers, ANSWER_KEY) if response == truth)
            post_score = sum(1 for response, truth in zip(post_answers, ANSWER_KEY) if response == truth)

            pre_score_list.append(pre_score)
            post_score_list.append(post_score)

            print ""
            print("User ID:", user_id)
            print("Pretest score:", pre_score)
            print("Posttest score:", post_score)

        t_value, p_value = stats.ttest_rel(post_score_list, pre_score_list)

        print "\n==============================\n"
        print "Pretest average: " + str(reduce(lambda x, y: x + y, pre_score_list)/float(len(pre_score_list)))
        print "Posttest average: " + str(reduce(lambda x, y: x + y, post_score_list)/float(len(post_score_list)))
        print "\nPaired t-test results"
        print "t-value: " + str(t_value)
        print "p-value: " + str(p_value)
        print ""
