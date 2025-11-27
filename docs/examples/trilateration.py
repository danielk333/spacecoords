import numpy as np
import matplotlib.pyplot as plt
import spacecoords.linalg as linalg


stations = np.stack(
    [
        np.array([1, 0, 0], dtype=np.float64),
        np.array([2, 1, 0], dtype=np.float64),
        np.array([0, -1, 0.2], dtype=np.float64),
        np.array([0, 0, -0.1], dtype=np.float64),
    ],
    axis=1,
)
target = np.array([3, 0, 20])

np.random.seed(328734)

range_errors = np.random.randn(stations.shape[1]) * 0
ranges = np.linalg.norm(stations - target[:, None], axis=0) + range_errors

system_mat, system_result = linalg.trilateration_system(ranges, stations)
print(system_mat, " x = ", system_result)

closest_point, resid, rank, _ = np.linalg.lstsq(system_mat, system_result)

print("x = ", closest_point)
print("target = ", target)
print(resid, rank)

# fig = plt.figure(figsize=(15, 15))
# ax = fig.add_subplot(111, projection="3d")
#
# ax.plot(stations[0, :], stations[1, :], stations[2, :], "ob")
# ax.plot(target[0], target[1], target[2], "or")
#
# ax.plot(closest_point[0], closest_point[1], closest_point[2], "xg")
#
# for ind in range(stations.shape[1]):
#     st = stations[:, ind]
#     ax.plot([target[0], st[0]], [target[1], st[1]], [target[2], st[2]], "--k", alpha=0.3)
#
# s_vec = np.linspace(0, 40, 200)
# for ind in range(stations.shape[1]):
#     st = stations[:, ind]
#     x = line(st, dirs_norm[:, ind], s_vec)
#     ax.plot(x[0, :], x[1, :], x[2, :], "-g")
#
# plt.show()
