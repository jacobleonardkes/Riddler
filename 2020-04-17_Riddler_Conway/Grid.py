import numpy as np
import enum

gridCache = {}

class CalcStatus(enum.Enum):
    IN_PROGRESS = 0
    TERMINATES = 1
    OSCILLATOR = 2
    PRE_OSCILLATOR = 3

calcCache = {}

class Grid(object):
    def __init__(self, cols=1):
        if cols > 21:
            raise ValueError('Must have fewer than 21 cols')
        self.data = np.zeros((3, cols), 'int64')

    @staticmethod
    def fromInt(cols, x):
        key = (cols, x)
        if key not in gridCache:
            g = Grid(cols)
            a = g.data.reshape(3 * cols)
            a += (x // 2 ** np.arange(0, 3 * cols)) % 2
            gridCache[key] = g
        return gridCache[key]

    def toInt(self):
        x = (self.data.reshape(self.data.size) * (2 ** np.arange(0, self.data.size))).sum()
        return x

    def next(self):
        ret = Grid(self.data.shape[1])
        # Add 2 up and down cells
        ret.data += self.data.sum(0)
        ret.data -= self.data
        # Add 3 left, left-diagonal cells
        ret.data[:, 1:] += self.data[:, :-1].sum(0)
        ret.data[:, 0] += self.data[:, -1].sum()
        # Add 3 right, right-diagonal cells
        ret.data[:, :-1] += self.data[:, 1:].sum(0)
        ret.data[:, -1] += self.data[:, 0].sum()

        # Cells are alive if 3 live neighbors or (2 live neighbors and were already alive)
        ret.data = 1 * ((ret.data == 3) | ((ret.data == 2) & (self.data == 1)))
        x = ret.toInt()
        gridCache[x] = ret
        return x

    def __str__(self):
        return '\n'.join(map(lambda row: ' '.join(map(lambda c: '#' if c else '_', row)), self.data))

    def evaluate(self):
        x = self.toInt()
        oscillationPath = []
        if x not in calcCache:
            y = self.next()
            if y == x:
                calcCache[x] = CalcStatus.TERMINATES
            else:
                calcCache[x] = CalcStatus.IN_PROGRESS
                calcCache[x] = gridCache[y].evaluate()
        if calcCache[x] == CalcStatus.IN_PROGRESS or calcCache[x] == CalcStatus.OSCILLATOR:
            path = [x]
            y = self.next()
            while y not in path:
                path.append(y)
                y = gridCache[y].next()
            if y == x:
                calcCache[x] = CalcStatus.OSCILLATOR
            else:
                calcCache[x] = CalcStatus.PRE_OSCILLATOR
        return calcCache[x]

cols = 4
for x in range(2**(3*cols)):
    if Grid.fromInt(cols, x).evaluate() == CalcStatus.OSCILLATOR:
        print(gridCache[x])
        print('----------------------------------')
