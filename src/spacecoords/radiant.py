import astropy.coordinates as coords
import astropy.units as units
import numpy as np
import numpy.typing as npt
from astropy.time import Time, TimeDelta


def ecliptic(ra: float, dec: float) -> coords.SkyCoord:
    """Goes to GeocentricMeanEcliptic"""

    radiant = coords.SkyCoord(ra * units.deg, dec * units.deg, frame="gcrs")
    return radiant.transform_to(coords.GeocentricMeanEcliptic())


def local(
    t: npt.NDArray[np.floating] | npt.NDArray[np.integer],
    epoch: Time | float,
    ra: float,
    dec: float,
    lon: float,
    lat: float,
    height: float = 0.0,
) -> coords.SkyCoord:
    """Calculate the local coordinates of meteor shower radiant.

    Args:
        t: Time in seconds relative the epoch at which to evaluate the radiant.
        epoch: If not given as `astropy.time.Time` instance,
            Epoch is treated as an UTC fractional Modified Julian Date
        lon: Longitude in degrees of the local observer
        lat: Latitude in degrees of the local observer
        ra: Right ascension in degrees of the meteor shower radiant in J2000 GCRS coordinates
        dec: Declination in degrees of the meteor shower radiant in J2000 GCRS coordinates
        height (optional): Height in meters above the ellipsoid of the local observer, defaults to `0`

    """

    if not isinstance(epoch, Time):
        epoch = Time(epoch, format="mjd", scale="utc")
    times = epoch + TimeDelta(t, format="sec")

    observer = coords.EarthLocation.from_geodetic(
        lon=lon * units.deg,
        lat=lat * units.deg,
        height=height * units.m,
        ellipsoid=None,
    )

    local_system = coords.AltAz(
        obstime=times,
        location=observer,
    )

    radiant = coords.SkyCoord(ra * units.deg, dec * units.deg, frame="gcrs")

    return radiant.transform_to(local_system)
