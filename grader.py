#!/usr/bin/env python3
import csv
import json
import math
from scipy import stats

ANSWER_KEY = [
    "The student sleeps like a Person",
    "tweety = Bird()",
    "robot.turnLeft()\nrobot.moveForward()\nrobot.moveForward()",
    "awooo!",
    "(none of these cause an error)",
]

OPINION_MAP = {
    "Strongly Agree": 2,
    "Agree": 1,
    "Neutral": 0,
    "Disagree": -1,
    "Strongly Disagree": -2
}

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
        
        enjoyed = []
        knew_oop_before = []
        knew_oop_better = []

        wrong_to_right = [0, 0, 0, 0, 0]
        right_to_wrong = [0, 0, 0, 0, 0]
        wrong_to_wrong = [0, 0, 0, 0, 0]
        right_to_right = [0, 0, 0, 0, 0]

        pretest_right = [0, 0, 0, 0, 0]
        posttest_right = [0, 0, 0, 0, 0]
        
        for user_id, post_answers in posttest_answers.items():
            pre_answers = pretest_answers.get(user_id)
            if not pre_answers:
                print "\nNo pretest for " + user_id
                continue

            pre_score = sum(1 for response, truth in zip(pre_answers, ANSWER_KEY) if response == truth)
            post_score = sum(1 for response, truth in zip(post_answers, ANSWER_KEY) if response == truth)

            pre_score_list.append(pre_score)
            post_score_list.append(post_score)
            
            enjoyed.append(OPINION_MAP[post_answers[5]])
            knew_oop_before.append(OPINION_MAP[post_answers[6]])
            knew_oop_better.append(OPINION_MAP[post_answers[7]])

            for i in range(len(pre_answers)):

                ans = ANSWER_KEY[i]
                pre = pre_answers[i]
                post = post_answers[i]

                if pre != ans and post != ans:
                    wrong_to_wrong[i] += 1
                elif pre != ans and post == ans:
                    wrong_to_right[i] += 1
                elif pre == ans and post != ans:
                    right_to_wrong[i] += 1
                elif pre == ans and post == ans:
                    right_to_right[i] += 1

                if pre_answers[i] == ANSWER_KEY[i]:
                    pretest_right[i] += 1
                if post_answers[i] == ANSWER_KEY[i]:
                    posttest_right[i] += 1

            print ""
            print("User ID:", user_id)
            print("Pretest score:", pre_score)
            print("Posttest score:", post_score)

        t_value, p_value = stats.ttest_rel(post_score_list, pre_score_list)
        _, _, pre_mean, pre_sample_variance, _, _ = stats.describe(pre_score_list)
        _, _, post_mean, post_sample_variance, _, _ = stats.describe(post_score_list)

        print "\n==============================\n"
        print "n = " + str(len(post_score_list)) + "\n"
        print "Pretest sample mean: " + str(pre_mean)
        print "Pretest sample SD: " + str(math.sqrt(pre_sample_variance))
        print "Posttest sample mean: " + str(post_mean)
        print "Posttest sample SD: " + str(math.sqrt(post_sample_variance))

        print ""
        print "'I enjoyed this game' average: " + str(stats.describe(enjoyed).mean)
        print "'I knew OOP before playing' average: " + str(stats.describe(knew_oop_before).mean)
        print "'I knew OOP better after playing' average: " + str(stats.describe(knew_oop_better).mean)

        print ""
        print "Paired t-test results"
        print "t-value: " + str(t_value)
        print "p-value: " + str(p_value)

        # print ""
        # print str(pretest_right) + "\tCorrect on pretest"
        # print str(posttest_right) + "\tCorrect on posttest\n"
        # print pre_score_list
        # print post_score_list

        print ""
        print str(wrong_to_wrong) + "\t\tWrong, Wrong"
        print str(wrong_to_right) + "\t\tWrong, Right"
        print str(right_to_wrong) + "\t\tRight, Wrong"
        print str(right_to_right) + "\tRight, Right"
        
