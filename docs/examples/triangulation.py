import numpy as np
import matplotlib.pyplot as plt
import spacecoords.linalg as linalg


def line(p, r, s):
    return p[:, None] + s[None, :] * r[:, None]


stations = np.array(
    [
        [1, 2, 0, 0],
        [0, 1, -1, 0],
        [0, 0, 0, 0],
    ],
    dtype=np.float64,
)
target = np.array([3, 0, 20])

np.random.seed(328734)

dirs = (target[:, None] + np.random.randn(*stations.shape) * 0.05) - stations
dirs_norm = dirs / np.linalg.norm(dirs, axis=0)

# This is done automatically in solve_triangulation but here we calculate the linear system
# manually to display the matricies involved in the computation
system_mat, system_result = linalg.triangulation_system(dirs_norm, stations)
closest_point = np.linalg.solve(system_mat, system_result)

print(system_mat, " x = ", system_result)
print("x = ", closest_point)

fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection="3d")

ax.plot(stations[0, :], stations[1, :], stations[2, :], "ob")
ax.plot(target[0], target[1], target[2], "or")

ax.plot(closest_point[0], closest_point[1], closest_point[2], "xg")

for ind in range(stations.shape[1]):
    st = stations[:, ind]
    ax.plot([target[0], st[0]], [target[1], st[1]], [target[2], st[2]], "--k", alpha=0.3)

s_vec = np.linspace(0, 40, 200)
for ind in range(stations.shape[1]):
    st = stations[:, ind]
    x = line(st, dirs_norm[:, ind], s_vec)
    ax.plot(x[0, :], x[1, :], x[2, :], "-g")

plt.show()
