import numpy as np
from spacecoords import celestial
from spacecoords import linalg
import matplotlib.pyplot as plt

lats = np.linspace(0.0, 90.0, 100)
lon = 20.0
alt = 0.0
zenith_ang_errors = np.empty_like(lats)
for ind, lat in enumerate(lats):
    locs_itrs = celestial.geodetic_to_ITRS(
        np.array([lat, lat]),
        np.array([lon, lon]),
        np.array([alt, alt + 1]),
        degrees=True,
    )
    loc_itrs = locs_itrs[:, 0]
    wgs84_zenith_itrs = locs_itrs[:, 1] - locs_itrs[:, 0]
    wgs84_zenith_itrs = wgs84_zenith_itrs / np.linalg.norm(wgs84_zenith_itrs)
    geocentric_zenith_itrs = loc_itrs / np.linalg.norm(loc_itrs)

    zenith_ang_errors[ind] = linalg.vector_angle(wgs84_zenith_itrs, geocentric_zenith_itrs, degrees=True)

fig, ax = plt.subplots()
ax.plot(lats, zenith_ang_errors)
ax.set_xlabel("Latitude [deg]")
ax.set_ylabel("Geocentric vs geodetic zenith [deg]")

plt.show()
