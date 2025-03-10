import json
import random
from tqdm import tqdm
from gen import gen


N = 8

teams = []

# import data


def load():
    global teams
    with open("teams.json", "r") as f:
        d = json.load(f)

    # sort the teams according elo
    teams = list(reversed(sorted(d["teams"], key=lambda x: x["elo"])))


def gen_teams(N):
    return list(reversed(sorted(gen(N)["teams"], key=lambda x: x["elo"])))


##### functions #####

def rank(t, teams):
    return [x for x in range(len(teams)) if teams[x]["id"] == t["id"]][0]


def prob(a, b):
    return 1/(1+10**(-(a["elo"]-b["elo"])/400))


def play(a, b):
    if (random.random() <= prob(a, b)):
        return a, b
    else:
        return b, a


##### simulations #####

### (single) robin ###

def robin(t):
    pts = [0 for _ in t]
    for i in range(len(t)):
        for j in range(len(t)):
            if i == j:
                continue
            w, l = play(t[i], t[j])
            pts[w["id"]-1] += 1
    return [x for i, x in enumerate(t) if pts[t[i]["id"]-1] == max(pts)]


### single elimination ###

def single(t):
    game1, _ = play(t[0], t[7])
    game2, _ = play(t[3], t[4])
    game3, _ = play(t[2], t[5])
    game4, _ = play(t[1], t[6])
    game5, _ = play(game1, game2)
    game6, _ = play(game3, game4)
    game7, _ = play(game5, game6)
    return game7

### double elimination ###


def double(t, complete=True):
    win1, lose1 = play(t[0], t[7])
    win2, lose2 = play(t[3], t[4])
    win3, lose3 = play(t[2], t[5])
    win4, lose4 = play(t[1], t[6])
    win5, lose5 = play(lose1, lose2)
    win6, lose6 = play(lose3, lose4)
    win7, lose7 = play(win1, win2)
    win8, lose8 = play(win3, win4)
    win9, lose9 = play(win5, lose8)
    win10, lose10 = play(win6, lose7)
    win11, lose11 = play(win7, win8)
    win12, lose12 = play(win9, win10)
    win13, lose13 = play(win12, lose11)
    win14, lose14 = play(win11, win13)
    if complete:
        if (win11["id"] == win14["id"]):
            return win14
        win15, lose15 = play(win14, lose14)
        return win15
    return win14

###### run #####


def simulate(mode, teams, iters):
    win = [0 for _ in teams]

    if mode == "single":
        for _ in range(iters):
            win[rank(single(teams), teams)] += 1

    if mode == "double":
        for _ in range(iters):
            win[rank(double(teams, False), teams)] += 1

    if mode == "double comp":
        for _ in range(iters):
            win[rank(double(teams, True), teams)] += 1

    if mode == "robin":
        for _ in range(iters):
            x = teams.copy()
            while len(x) != 1:
                x = robin(teams)
            win[rank(x[0], teams)] += 1

    return win, win[0]/sum(win)


s = 0
iter_out = 1000
iter_in = 1000
mode = "double comp"

for _ in tqdm(range(iter_out)):
    w, wr = simulate(mode, gen_teams(N), iter_in)
    s += wr

print(f"{mode}: {s/iter_out}")
