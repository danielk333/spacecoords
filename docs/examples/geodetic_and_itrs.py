import numpy as np
import timeit
from spacecoords import celestial
from spacecoords import frames
import matplotlib.pyplot as plt

lat = 67 + 50 / 60 + 26.6 / 3600
lon = 20 + 24 / 60 + 40.0 / 3600
alt = 425
# Using astropy implementation
loc_itrs = celestial.geodetic_to_ITRS(lat, lon, alt, degrees=True)

# Using internal WGS84 implementation
loc_itrs_2 = frames.geodetic_wgs84_to_ecef(lat, lon, alt, degrees=True)

print(f"implementation diff = {loc_itrs - loc_itrs_2}")
t_astropy = timeit.timeit(
    lambda: celestial.geodetic_to_ITRS(lat, lon, alt, degrees=True),
    number=10_000,
)
t_own = timeit.timeit(
    lambda: frames.geodetic_wgs84_to_ecef(lat, lon, alt, degrees=True),
    number=10_000,
)
print(f"{t_astropy=:.2e} s vs {t_own=:.2e} s ({t_astropy / t_own} faster)")

latm = np.linspace(-10, 10, 100)
lonm = np.ones_like(latm)
altm = 425 * np.ones_like(latm)
t_astropy_vector = timeit.timeit(
    lambda: celestial.geodetic_to_ITRS(latm, lonm, altm, degrees=True),
    number=1_000,
)
t_own_vector = timeit.timeit(
    lambda: frames.geodetic_wgs84_to_ecef(latm, lonm, altm, degrees=True),
    number=1_000,
)
print(f"{t_astropy_vector=:.2e} s vs {t_own_vector=:.2e} s ({t_astropy / t_own} faster)")

enu = np.array([0, 10e3, 100e3], dtype=np.float64)
r_enu = np.linalg.norm(enu)

target_topo_itrs = frames.enu_to_ecef(lat, lon, enu, degrees=True)
target_itrs = target_topo_itrs + loc_itrs
rel_itrs = target_itrs - loc_itrs
r_itrs = np.linalg.norm(target_topo_itrs)

print(f"{loc_itrs=}")
print(f"{target_itrs=}")
print(f"{rel_itrs=}")
print(f"\n{r_enu=} - {r_itrs} = {r_enu - r_itrs}")


# TODO: flesh this out with adding in the coordinate basis vectors
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection="3d")
ax.plot([0], [0], [0], "ok")
ax.plot(
    [0, enu[0]],
    [0, enu[1]],
    [0, enu[2]],
    "-b",
)
ax.plot(
    enu[0],
    enu[1],
    enu[2],
    "xr",
)
ax.plot(
    [0, target_itrs[0] - loc_itrs[0]],
    [0, target_itrs[1] - loc_itrs[1]],
    [0, target_itrs[2] - loc_itrs[2]],
    "--b",
)
ax.plot(
    [target_itrs[0] - loc_itrs[0]],
    [target_itrs[1] - loc_itrs[1]],
    [target_itrs[2] - loc_itrs[2]],
    "or",
)
plt.show()
