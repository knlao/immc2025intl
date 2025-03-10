import json
import random

N = 8

elo_range = (2600, 2850)


def item(id):
    team = {}
    team["id"] = id
    team["elo"] = random.randint(elo_range[0], elo_range[1])
    return team


def gen(n):
    d = {}
    teams = []
    for i in range(1, n+1):
        teams.append(item(i))
    d["teams"] = teams
    return d


def gen_file(n):
    with open("teams.json", "w") as f:
        json.dump(gen(n), f, indent=4)


if __name__ == "__main__":
    gen_file(N)
