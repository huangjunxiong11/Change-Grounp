import random





videoHome = [i for i in range(30)]
movNumble = 6

architecture = []
for b in range(movNumble):
    first = random.sample(videoHome, 10)
    tenRan = []
    for j in first:
        k = videoHome[:]
        k.remove(j)
        child = random.sample(k, 5)
        child.insert(0, j)
        tenRan.append(child)
    architecture.append(tenRan)



