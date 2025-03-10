import tqdm
sum = 0
for i in tqdm.tqdm(range(0, 100000000)):
    sum += i
print(sum)
