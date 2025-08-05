import pandas as pd
from math import dist

def kbti_distance(ans):

    scores = pd.read_csv("Score.csv")
    scores = scores.values.tolist()

    def distance(score):
        dis1 = dist([ans[0], ans[1]], [score[6], score[10]])
        dis2 = dist([ans[2], ans[3]], [score[9], score[5]])
        dis3 = dist([ans[4], ans[5]], [score[3], score[8]])
        dis4 = dist([ans[6], ans[7]], [score[4], score[7]])
        return dist([0,0,0,0], [dis1, dis2, dis3, dis4])

    result_player = ""
    min = 1000.0

    for score in scores:
        dis = distance(score)
        if min > dis:
            result_player = score[1]
            min = dis

    return result_player