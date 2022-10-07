import numpy as np
from matplotlib import pyplot as plt


def extra_credit(chair_max: int, basket_pairs_max: int) -> float:
    cache = {}
    basket_max = basket_pairs_max * 2

    def p(chair: int, basket: int) -> float:
        key = chair, basket
        if key not in cache:
            remaining_socks = chair + basket
            remaining_pairs = remaining_socks // 2
            if remaining_pairs <= chair_max:
                cache[key] = 1.0
                return 1.0

            # Chance of matching next sock drawn
            p_match = chair / basket

            # Chance of matching next sock drawn and subsequently "winning"
            if chair > 0:
                p_match_win = p_match * p(chair - 1, basket - 1)
            else:
                p_match_win = 0.0

            # Chance of not matching next sock drawn
            p_nomatch = 1.0 - p_match

            # Chance of not matching next sock drawn and subsequently "winning"
            if chair == chair_max:
                p_nomatch_win = 0.0
            else:
                p_nomatch_win = p_nomatch * p(chair + 1, basket - 1)

            cache[key] = p_match_win + p_nomatch_win

        return cache[key]

    return p(0, basket_max)


print(extra_credit(9, 14))

p_grid = np.ndarray((60, 100))
for chair_max in range(61):
    for basket_pairs_max in range(101):
        p_grid[chair_max-1, basket_pairs_max-1] = extra_credit(chair_max, basket_pairs_max) * 100

fig, ax = plt.subplots()

ax.pcolormesh(p_grid, cmap="copper")
ax.set_title("Percent Chance of Not Overflowing Chair")
ax.set_xlabel("Chair Capacity")
ax.set_ylabel("# Pairs Socks")
plt.colorbar(plt.pcolor(p_grid, cmap="copper"))
plt.savefig("heatmap.png")

fig.clear()
fig, ax = plt.subplots()
ax.plot(p_grid[40], label="P(not overflowing)")
ax2 = ax.twinx()
ax2.plot(p_grid[40, 0:99] - p_grid[40, 1:100], label="P'", color="red")
ax.legend()
ax2.legend()
plt.title("P(not overflowing | chair size=40)")
plt.savefig("varying_num_pairs.png")

fig.clear()
fig, ax = plt.subplots()
ax.plot(p_grid[:, 50], label="P(not overflowing)")
ax2 = ax.twinx()
ax2.plot(p_grid[1:60, 50] - p_grid[0:59, 50], label="P'", color="red")
ax.legend()
ax2.legend()
ax2.yaxis.set_ticklabels([])
plt.title("P(not overflowing | 50 pairs socks)")
plt.savefig("varying_chair_size.png")

print("Done")