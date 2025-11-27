import numpy as np
import matplotlib.pyplot as plt
import spacecoords.linalg as linalg


def add_sphere(ax, center, radius, alpha=0.3, res=100):
    # from matplotlib examples gallery
    u = np.linspace(0, 2 * np.pi, res)
    v = np.linspace(0, np.pi, res)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
    ax.plot_surface(x, y, z, alpha=alpha)


stations = np.stack(
    [
        np.array([1, 0, 0], dtype=np.float64),
        np.array([10, 1, 0], dtype=np.float64),
        np.array([0, -10, 5], dtype=np.float64),
        np.array([0, 0, -5], dtype=np.float64),
    ],
    axis=1,
)
target = np.array([3, 0, 10])

np.random.seed(328734)

range_errors = np.random.randn(stations.shape[1]) * 0
ranges = np.linalg.norm(stations - target[:, None], axis=0) + range_errors

system_mat, system_result = linalg.trilateration_system(ranges, stations)
print(system_mat, " x = ", system_result)

closest_point, resid, rank, _ = np.linalg.lstsq(system_mat, system_result)

print("x = ", closest_point)
print("target = ", target)
print(resid, rank)

fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection="3d")

ax.plot(stations[0, :], stations[1, :], stations[2, :], "ob")
ax.plot(target[0], target[1], target[2], "or")
ax.plot(closest_point[0], closest_point[1], closest_point[2], "xg")

for ind in range(stations.shape[1]):
    add_sphere(ax, stations[:, ind], ranges[ind])

ax.set_aspect("equal")
plt.show()
