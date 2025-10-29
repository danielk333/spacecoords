#!/usr/bin/env python

"""Coordinate frame transformations and related functions.
Main usage is the `convert` function that wraps Astropy frame transformations.
"""
from typing import Type, Any
import numpy as np
import astropy.coordinates as coord
import astropy.units as units
from astropy.coordinates import EarthLocation

from .types import (
    NDArray_N,
    NDArray_6,
    NDArray_6xN,
    T,
)

"""List of astropy frames
"""
ASTROPY_FRAMES = {
    "TEME": "TEME",
    "ITRS": "ITRS",
    "ITRF": "ITRS",
    "ICRS": "ICRS",
    "ICRF": "ICRS",
    "GCRS": "GCRS",
    "GCRF": "GCRS",
    "HCRS": "HCRS",
    "HCRF": "HCRS",
    "HeliocentricMeanEcliptic".upper(): "HeliocentricMeanEcliptic",
    "GeocentricMeanEcliptic".upper(): "GeocentricMeanEcliptic",
    "HeliocentricTrueEcliptic".upper(): "HeliocentricTrueEcliptic",
    "GeocentricTrueEcliptic".upper(): "GeocentricTrueEcliptic",
    "BarycentricMeanEcliptic".upper(): "BarycentricMeanEcliptic",
    "BarycentricTrueEcliptic".upper(): "BarycentricTrueEcliptic",
    "SPICEJ2000": "ICRS",
}

"""List of frames that are not time-dependant
"""
ASTROPY_NOT_OBSTIME = [
    "ICRS",
    "BarycentricMeanEcliptic",
    "BarycentricTrueEcliptic",
]


def not_geocentric(frame: str) -> bool:
    """Check if the given frame name is one of the non-geocentric frames."""
    frame = frame.upper()
    return frame in ["ICRS", "ICRF", "HCRS", "HCRF"] or frame.startswith("Heliocentric".upper())


def is_geocentric(frame: str) -> bool:
    """Check if the frame name is a supported geocentric frame"""
    return not not_geocentric(frame)


def convert(
    t: NDArray_N,
    states: NDArray_6xN,
    in_frame: str,
    out_frame: str,
    frame_kwargs: dict[str, Any],
) -> NDArray_6xN:
    """Perform predefined coordinate transformations using Astropy.
    Always returns a copy of the array.

    Parameters
    ----------
    t
        Absolute time corresponding to the input states.
    states
        Size `(6,n)` matrix of states in SI units where rows 1-3
        are position and 4-6 are velocity.
    in_frame
        Name of the frame the input states are currently in.
    out_frame
        Name of the state to transform to.
    frame_kwargs
        Any arguments needed for the specific transform detailed by `astropy`
        in their documentation

    Returns
    -------
        Size `(6,n)` matrix of states in SI units where rows
        1-3 are position and 4-6 are velocity.

    """

    in_frame = in_frame.upper()
    out_frame = out_frame.upper()

    if in_frame == out_frame:
        return states.copy()

    if in_frame in ASTROPY_FRAMES:
        in_frame_ = ASTROPY_FRAMES[in_frame]
        in_frame_cls = getattr(coord, in_frame_)
    else:
        err_str = [
            f"In frame '{in_frame}' not recognized, ",
            "please check spelling or perform manual transformation",
        ]
        raise ValueError("".join(err_str))

    kw = {}
    kw.update(frame_kwargs)
    if in_frame_ not in ASTROPY_NOT_OBSTIME:
        kw["obstime"] = t

    astropy_states = _convert_to_astropy(states, in_frame_cls, kw)

    if out_frame in ASTROPY_FRAMES:
        out_frame_ = ASTROPY_FRAMES[out_frame]
        out_frame_cls = getattr(coord, out_frame_)
    else:
        err_str = [
            f"Out frame '{out_frame}' not recognized, ",
            "please check spelling or perform manual transformation",
        ]
        raise ValueError("".join(err_str))

    kw = {}
    kw.update(frame_kwargs)
    if out_frame_ not in ASTROPY_NOT_OBSTIME:
        kw["obstime"] = t

    out_states = astropy_states.transform_to(out_frame_cls(**kw))

    rets = states.copy()
    rets[:3, ...] = out_states.cartesian.xyz.to(units.m).value
    rets[3:, ...] = out_states.velocity.d_xyz.to(units.m / units.s).value

    return rets


def _convert_to_astropy(
    states: NDArray_6xN | NDArray_6,
    frame: Type[T],
    frame_kwargs: dict[str, Any],
) -> T:
    state_p = coord.CartesianRepresentation(states[:3, ...] * units.m)
    state_v = coord.CartesianDifferential(states[3:, ...] * units.m / units.s)
    astropy_states = frame(state_p.with_differentials(state_v), **frame_kwargs)  # type: ignore
    return astropy_states


def geodetic_to_ITRS(lat, lon, alt, degrees=True, ellipsoid=None):
    """Use `astropy.coordinates.EarthLocation` to transform from geodetic to ITRS."""
    raise NotImplementedError()
    # todo: replace this with astropy.coordinates.WGS84GeodeticRepresentation
    # so that it can be vectorized - we never use any other ellipsoid anyway

    if degrees:
        lat, lon = np.radians(lat), np.radians(lon)

    cord = EarthLocation.from_geodetic(
        lon=lon * units.rad,
        lat=lat * units.rad,
        height=alt * units.m,
        ellipsoid=ellipsoid,
    )
    x, y, z = cord.to_geocentric()

    pos = np.empty((3,), dtype=np.float64)

    pos[0] = x.to(units.m).value
    pos[1] = y.to(units.m).value
    pos[2] = z.to(units.m).value

    return pos


def ITRS_to_geodetic(x, y, z, degrees=True, ellipsoid=None):
    """Use `astropy.coordinates.EarthLocation` to transform from geodetic to ITRS.

    x: X-coordinate in ITRS
    y: Y-coordinate in ITRS
    z: Z-coordinate in ITRS
    :param bool radians: If :code:`True` then all values are given in radians instead of degrees.
    :param str/None ellipsoid: Name of the ellipsoid model used for geodetic
    coordinates, for default value see Astropy `EarthLocation`.
    :rtype: numpy.ndarray
    :return: (3,) array of longitude, latitude and height above ellipsoid
    """
    raise NotImplementedError()
    # todo: replace this with astropy.coordinates.WGS84GeodeticRepresentation
    # so that it can be vectorized - we never use any other ellipsoid anyway

    cord = EarthLocation.from_geocentric(
        x=x * units.m,
        y=y * units.m,
        z=z * units.m,
    )
    lon, lat, height = cord.to_geodetic(ellipsoid=ellipsoid)

    llh = np.empty((3,), dtype=np.float64)

    if degrees:
        u_ = units.deg
    else:
        u_ = units.rad
    llh[0] = lat.to(u_).value
    llh[1] = lon.to(u_).value
    llh[2] = height.to(units.m).value

    return llh
