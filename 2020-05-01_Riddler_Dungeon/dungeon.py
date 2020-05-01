import scipy.optimize as opt

binCoeffCache = {}
def binCoeff(n, i):
  key = (n, i)
  if key not in binCoeffCache:
    x = 1.0
    for j in range(1,i+1):
      x *= n-i+j
      x /= j
    binCoeffCache[key] = x
  return binCoeffCache[key]

def pFree(n, pFlip):
  tot = 0.0
  pBar = 1.0 - pFlip
  for i in range(1, n+1):
    tot += (pFlip ** i) * (pBar ** (n-i)) * binCoeff(n, i) * (2 ** (-i))
  return tot

def dpFreedpFlip(n, pFlip):
  tot = 0.0
  pBar = 1.0 - pFlip
  for i in range(1, n+1):
    tot += pFlip ** (i-1) * pBar ** (n-i-1) * (i * pBar - (n-i)*pFlip) * binCoeff(n, i) * 2.0 ** (-i)
  return tot

print('n\tpLip        \tpFree     \tn*p')
print('1\t1.00000000\t0.5000000\t1.00000000')
for n in range(2, 101):
  x = opt.root_scalar(lambda p: dpFreedpFlip(n, p), method='bisect', bracket=(0.000001, 0.999999)).root
  print('%d\t%.8f\t%.8f\t%.8f' % (n, x, pFree(n, x), n*x))


x = opt.root_scalar(lambda p: dpFreedpFlip(1000, p), method='bisect', bracket=(0.000001, 0.999999)).root
print('%d\t%.8f\t%.8f\t%.8f' % (1000, x, pFree(1000, x), x*1000))
