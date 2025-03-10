# generate dummy data

import json
import random

N = 20

# read file
c = None
w = None
with open("dummy/countries.json", "r") as f:
    c = json.load(f)
with open("dummy/words.txt", "r") as f:
    w = f.readlines()

ranking = [i for i in range(1, N+1)]

def item(id):
    team = {}
    team["id"] = id
    team["name"] = random.choice(w).strip()
    team["country"], team["continent"] = random.choice(list(c.items()))
    team["loc"] = (random.randint(-89e5, 89e5)/1e5, random.randint(-179e5, 179e5)/1e5)
    team["rank"] = ranking[id-1]
    print(team)
    return team

def gen(n):
    d = {}
    teams = []
    for i in range(1, n+1):
        teams.append(item(i))
    d["teams"] = teams
    d["_comment"] = "for loc, the format is (lat, lon)"
    with open("teams_gen.json", "w") as f:
        json.dump(d, f, indent=4)

gen(N)
