import json
from geopy import distance
from tqdm import tqdm
import numpy as np


# import data
with open("teams.json", "r") as f:
    d = json.load(f)

teams = d["teams"]


##### functions #####


# distance
def dist(a, b):
    return distance_matrix[a][b]


# distance between team location of a and b
def dist_a(a, b):
    return distance.distance(a, b)


# search for teams in a continent
def search(c, t):
    return [element for element in t if element['continent'] == c]


# search for teams with odd/even rank
def search_r(x, t):
    return [element for element in t if element['rank'] % 2 == x]


# next permutation of a list of numbers
def next_permutation(nums):
    i = j = len(nums) - 1
    while i > 0 and nums[i - 1] >= nums[i]:
        i -= 1
    if i == 0:
        nums.reverse()
        return
    k = i - 1
    while nums[j] <= nums[k]:
        j -= 1
    nums[k], nums[j] = nums[j], nums[k]
    l, r = k + 1, len(nums) - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
    return nums


# factorial
def factorial(num):
    if num == 0 or num == 1:
        return 1
    else:
        return num * factorial(num-1)


# generate the single round robin schedule
def gen_robin(teams):
    n = len(teams)
    schedule = []

    # though this won't happen because the league ensures an even number of teams
    # but still added this just in case
    if n % 2 != 0:
        teams.append(None)
        n += 1

    for _ in range(n - 1):
        round_matches = []
        for i in range(n // 2):
            if teams[i] is not None and teams[n - 1 - i] is not None:
                round_matches.append((teams[i], teams[n - 1 - i]))
        schedule.append(round_matches)
        teams.insert(1, teams.pop())

    return schedule


# create schedule
def make_schedule(teams_group):

    first_half = gen_robin(teams_group)

    # since it is double robin
    second_half = []
    for round_matches in first_half:
        reversed_round = [(away, home) for (home, away) in round_matches]
        second_half.append(reversed_round)

    schedule = first_half + second_half

    return schedule


# print the schedule for humans to read
def print_schedule(schedule):
    rounds = {}
    for idx, round_matches in enumerate(schedule):
        rounds[idx + 1] = round_matches

    for round_num, matches in rounds.items():
        print(f"Round {round_num}:")
        for match in matches:
            home, away = match
            print(f"  {home['name']} (Home) vs {away['name']} (Away)")
        print()


# calculate distance
def total_distance(schedule, teams_group):

    # init

    team_opponents = {}

    for t in teams_group:
        team_opponents[t["name"]] = []

    for idx, round in enumerate(schedule):
        for match in round:
            team_opponents[match[0]["name"]].append(match[0]["id"])
            team_opponents[match[1]["name"]].append(match[0]["id"])

    distance_each = {}
    for t in teams_group:
        distance_each[t["name"]] = 0
    for c, o in team_opponents.items():
        for idx in range(len(o)-1):
            distance_each[c] += dist(team_opponents[c]
                                     [idx], team_opponents[c][idx+1]).km

    return sum(v for k, v in distance_each.items()), distance_each


##### initialise #####

# initialise distance matrix
distance_matrix = [[[] for _2 in range(len(teams)+1)] for _1 in range(len(teams)+1)]

for i in range(len(teams)):
    for j in range(len(teams)):
        distance_matrix[teams[i]["id"]][teams[j]["id"]] = dist_a(
            teams[i]["loc"], teams[j]["loc"])


##### main functions #####


### brute force the all distances ###

# run to calculate all situations
def brute_force_distance():

    # even rounds
    teams_group = search_r(0, teams)

    # odd rounds
    # teams_group = search_r(1, teams)

    team_idx = [_ for _ in range(len(teams_group))]

    schedule = make_schedule([teams_group[idx] for idx in team_idx])
    distance_total, distance_each = total_distance(schedule, teams_group)

    distance_total_min = 100000000000000

    io_buffer = []
    iter2 = 0
    file_buffer_len = 1000000
    iter3 = 1

    for iter in tqdm(range(factorial(len(teams_group)))):
        schedule = make_schedule([teams_group[idx] for idx in team_idx])
        distance_total, distance_each = total_distance(schedule, teams_group)
        io_buffer.append(
            f"{iter},{distance_total},{np.std([v for k, v in distance_each.items()])},{','.join([str(v) for k, v in distance_each.items()])}\n")
        distance_total_min = min(distance_total, distance_total_min)
        team_idx = next_permutation(team_idx)

        iter2 += 1
        if iter2 >= file_buffer_len:
            with open(f"result_data/results_odd_{iter3}.csv", "w+") as f:
                f.write(
                    f"iter,total,variance,{','.join([str(k) for k, v in distance_each.items()])}\n")
                f.writelines(io_buffer)
                iter2 = 0
                iter3 += 1
                io_buffer = []

    with open(f"result_data/results_odd_{iter3}.csv", "w+") as f:
        f.write(
            f"iter,total,variance,{','.join([str(k) for k, v in distance_each.items()])}\n")
        f.writelines(io_buffer)

    print(f"minimum total travel distance: {distance_total_min}km")


### get the optimal solution ###

def optimal_sol():

    # even rounds
    teams_group = search_r(0, teams)
    optimal_sol_idx = 2089854

    # odd rounds
    # teams_group = search_r(1, teams)
    # optimal_sol_idx = 1738550

    team_idx = [_ for _ in range(len(teams_group))]

    distance_total_min = 100000000000000

    for iter in tqdm(range(optimal_sol_idx)):
        team_idx = next_permutation(team_idx)

    schedule = make_schedule([teams_group[idx] for idx in team_idx])
    distance_total, distance_each = total_distance(schedule, teams_group)
    distance_total_min = min(distance_total, distance_total_min)

    print(
        f"{iter+1},{distance_total},{np.std([v for k, v in distance_each.items()])},{','.join([str(v) for k, v in distance_each.items()])}\n")

    print_schedule(schedule)


##### run #####

# brute_force_distance()
optimal_sol()
