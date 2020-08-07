from scipy.special import binom
import matplotlib.pyplot as plt

def transitionProb(n, m):
    pairs = n // 2
    return binom(pairs, m-n) / (2 ** pairs)

transitionCache = {}
def transitionProbs(n):
    if n not in transitionCache:
        transitionCache[n] = {n+m: transitionProb(n, n + m) for m in range((n//2)+1)}
    return transitionCache[n]

probs = {1: {2: 1.0}}
expectations = [2.0]
for step in range(2, 20):
    probs[step] = {}
    for n, p in probs[step-1].items():
        tps = transitionProbs(n)
        for m, tp in tps.items():
            probs[step][m] = probs[step].get(m, 0.0) + p * tp
    expectations.append(sum([n*p for n,p in probs[step].items()]))
    print('%d: %.8f' % (step, expectations[-1]))

plt.plot(range(1, len(expectations)+1), expectations)
plt.xlabel('Exponent')
plt.ylabel('Expectation')
plt.xticks(range(1, len(expectations)+1))
plt.grid()
plt.show()
