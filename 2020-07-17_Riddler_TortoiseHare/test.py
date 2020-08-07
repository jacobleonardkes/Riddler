import math
import matplotlib.pyplot as plt
import numpy as np

def timeToFinish(pos, length, speed):
    t = 0.0
    while pos + speed < length:
        pos += speed
        pos *= (length + 10.0) / length
        length += 10.0
        t += 1.0
    return t + (length - pos)/speed

tortoiseTime = timeToFinish(0.0, 10.0, 1.0)
print('Tortoise finish time: %.10f' % tortoiseTime)

def rabbitTimeToFinish(waitTime):
    length = (1+math.ceil(waitTime)) * 10.0
    pos = 1.25 * (math.ceil(waitTime) - waitTime)
    pos *= length / (length-10)
    return timeToFinish(pos, length, 1.25)

def binarySearch(lowerBound, upperBound):
    mid = (lowerBound + upperBound) / 2.0
    if upperBound - lowerBound < 1e-12:
        return mid
    midTime = rabbitTimeToFinish(mid)
    if midTime > tortoiseTime:
        return binarySearch(lowerBound, mid)
    else:
        return binarySearch(mid, upperBound)

hareWait = binarySearch(1.0, 10.0)
print('Hare wait time: %.10f' % hareWait)

times = np.array([float(i//2) + (0.0 if i % 2 == 0 else 0.99) for i in range(12367*2)])
tPos = [0.0, 0.99]
for i in range(1,12367):
    tPos.append((tPos[-1]+0.01)*float(i+1)/float(i))
    tPos.append(tPos[-1]+0.99)
tPos = np.array(tPos)
lengths = np.floor(times)*10.0 + 10.0
tRatios = tPos / lengths

hPos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, (3.99-hareWait)*1.25]
for i in range(4,12367):
    hPos.append((hPos[-1]+0.01*1.25)*float(i+1)/float(i))
    hPos.append(hPos[-1]+0.99*1.25)
hPos = np.array(hPos)
hRatios = hPos / lengths

plt.scatter(times, lengths, s=1, label='Track', c='black')
plt.scatter(times, tPos, s=1, label='Tortoise', c='blue')
plt.scatter(times, hPos, s=1, label='Hare', c='red')
plt.ylabel('Miles')
plt.xlabel('Time (minutes)')
plt.legend(loc=7)
plt.title('Distance Traveled')
plt.show()

plt.scatter(times, tRatios*100, s=1, c='blue', label='Tortoise')
plt.scatter(times, hRatios*100, s=1, c='red', label='Hare')
plt.xlabel('Time (minutes)')
plt.ylabel('Percent Complete')
plt.title('Percent Complete')
plt.legend()
plt.show()

plt.scatter(times, lengths-tPos, s=1, c='blue', label='Tortoise')
plt.scatter(times, lengths-hPos, s=1, c='red', label='Hare')
plt.xlabel('Time (minutes)')
plt.ylabel('Miles Remaining')
plt.title('Miles Remaining')
plt.legend()
plt.show()

x = np.arange(1.0, 10.0, 0.01)
y = x * 0.0
for i in range(len(x)):
    y[i] = rabbitTimeToFinish(x[i])
plt.plot(x, y, c='red')
plt.axvline(hareWait, 0.0, y.max())
plt.axhline(tortoiseTime, 0.0, x.max())
plt.xlabel('Minutes Rabbit Waits')
plt.ylabel('Time For Rabbit To Complete')
plt.show()
