#!/usr/bin/env python

"""Transforms between common coordinate frames without any additional dependencies"""

import numpy as np
from .spherical import sph_to_cart
from .types import (
    NDArray_N,
    NDArray_3,
    NDArray_3xN,
)
from .constants import WGS84

WGS84_POLE_LIMIT = 1e-9


def ned_to_ecef(
    lat: float,
    lon: float,
    ned: NDArray_3xN | NDArray_3,
    degrees: bool = False,
) -> NDArray_3xN | NDArray_3:
    """NED (north/east/down) using geocentric zenith to ECEF coordinate system
    conversion, not including translation.

    Parameters
    ----------
    lat
        Latitude of the origin in geocentric spherical coordinates
    lon
        Longitude of the origin in geocentric spherical coordinates
    ned
        (3,n) input matrix of positions in the NED-convention.
    degrees
        If `True`, use degrees. Else all angles are given in radians.

    Returns
    -------
        (3,) or (3,n) array x,y and z coordinates in ECEF.
    """
    enu = np.empty(ned.size, dtype=ned.dtype)
    enu[0, ...] = ned[1, ...]
    enu[1, ...] = ned[0, ...]
    enu[2, ...] = -ned[2, ...]
    return enu_to_ecef(lat, lon, enu, degrees=degrees)


def azel_to_ecef(
    lat: float,
    lon: float,
    az: NDArray_N | float,
    el: NDArray_N | float,
    degrees: bool = False,
) -> NDArray_3xN | NDArray_3:
    """Radar pointing (az,el) using geocentric zenith to unit vector in
    ECEF, not including translation.

    Parameters
    ----------
    lat
        Latitude of the origin in geocentric spherical coordinates
    lon
        Longitude of the origin in geocentric spherical coordinates
    az
        Azimuth of the pointing direction
    el
        Elevation of the pointing direction
    degrees
        If `True`, use degrees. Else all angles are given in radians.

    Returns
    -------
        (3,) or (3,n) array x,y and z coordinates in ECEF.
    """
    shape: tuple[int, ...] = (3,)

    if isinstance(az, np.ndarray):
        if len(az.shape) == 0:
            az = float(az)
        elif len(az) > 1:
            shape = (3, len(az))
            az = az.flatten()
        else:
            az = az[0]

    if isinstance(el, np.ndarray):
        if len(el.shape) == 0:
            el = float(el)
        elif len(el) > 1:
            shape = (3, len(el))
            el = el.flatten()
        else:
            el = el[0]

    sph = np.empty(shape, dtype=np.float64)
    sph[0, ...] = az
    sph[1, ...] = el
    sph[2, ...] = 1.0
    enu = sph_to_cart(sph, degrees=degrees)
    return enu_to_ecef(lat, lon, enu, degrees=degrees)


def enu_to_ecef(
    lat: float,
    lon: float,
    enu: NDArray_3 | NDArray_3xN,
    degrees: bool = False,
) -> NDArray_3xN | NDArray_3:
    """Rotate ENU (east/north/up) using geocentric latitude and longitude (and zenith)
    to ECEF coordinate system, not including translation.

    Parameters
    ----------
    lat
        Latitude of the origin in geocentric spherical coordinates
    lon
        Longitude of the origin in geocentric spherical coordinates
    enu
        (3,n) input matrix of positions in the ENU-convention.
    degrees
        If `True`, use degrees. Else all angles are given in radians.

    Returns
    -------
        (3,) or (3,n) array x,y and z coordinates in ECEF.
    """
    if degrees:
        lat, lon = np.radians(lat), np.radians(lon)

    mx = np.array(
        [
            [-np.sin(lon), -np.cos(lon) * np.sin(lat), np.cos(lon) * np.cos(lat)],
            [np.cos(lon), -np.sin(lon) * np.sin(lat), np.sin(lon) * np.cos(lat)],
            [0, np.cos(lat), np.sin(lat)],
        ]
    )

    ecef = np.dot(mx, enu)
    return ecef


def ecef_to_enu(
    lat: float,
    lon: float,
    ecef: NDArray_3 | NDArray_3xN,
    degrees: bool = False,
) -> NDArray_3xN | NDArray_3:
    """Rotate ECEF coordinate system to local ENU (east,north,up) using geocentric
    latitude and longitude (and zenith), not including translation.

    Parameters
    ----------
    lat
        Latitude of the origin in geocentric spherical coordinates
    lon
        Longitude of the origin in geocentric spherical coordinates
    ecef
        (3,) or (3,n) array x,y and z coordinates in ECEF.
    degrees
        If `True`, use degrees. Else all angles are given in radians.

    Returns
    -------
        (3,) or (3,n) array x, y and z coordinates in ENU.
    """
    if degrees:
        lat, lon = np.radians(lat), np.radians(lon)

    mx = np.array(
        [
            [-np.sin(lon), np.cos(lon), 0],
            [-np.cos(lon) * np.sin(lat), -np.sin(lon) * np.sin(lat), np.cos(lat)],
            [np.cos(lon) * np.cos(lat), np.sin(lon) * np.cos(lat), np.sin(lat)],
        ]
    )
    enu = np.dot(mx, ecef)
    return enu


def geodetic_wgs84_to_ecef(
    lat: NDArray_N | float,
    lon: NDArray_N | float,
    alt: NDArray_N | float,
    degrees: bool = False,
) -> NDArray_3xN | NDArray_3:
    """Convert WGS84 geodetic coordinates to ECEF coordinates with custom implementation [^1].

    [^1]: J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates to geodetic coordinates,"
        IEEE Transactions on Aerospace and Electronic Systems, vol. 30, pp. 957-961, 1994.

    Returns
    -------
        (3,) or (3,n) array x, y and z coordinates in ECEF.

    """
    if degrees:
        lat, lon = np.radians(lat), np.radians(lon)
    xi = np.sqrt(1 - WGS84.esq * np.sin(lat) ** 2)
    x = (WGS84.a / xi + alt) * np.cos(lat) * np.cos(lon)
    y = (WGS84.a / xi + alt) * np.cos(lat) * np.sin(lon)
    z = (WGS84.a / xi * (1 - WGS84.esq) + alt) * np.sin(lat)

    return np.array([x, y, z])


def ecef_to_geodetic_wgs84(
    x: NDArray_N | float,
    y: NDArray_N | float,
    z: NDArray_N | float,
    degrees: bool = False,
) -> NDArray_3xN | NDArray_3:
    """Convert ECEF coordinates to WGS84 geodetic coordinates with custom implementation [^1].

    [^1]: J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates to geodetic coordinates,"
        IEEE Transactions on Aerospace and Electronic Systems, vol. 30, pp. 957-961, 1994.

    Parameters
    ----------
    x
        Position along prime meridian [m]
    y
        Position along prime meridian + 90 degrees [m]
    z
        Position along earth rotation axis [m]

    Returns
    -------
    numpy.ndarray
        (3,) or (3,n) array lat [deg], lon [deg], alt [m] coordinates in WGS84 geodetic coordinates.

    """
    xyz_len = x.size if isinstance(x, np.ndarray) else None

    if xyz_len is None:
        assert (
            isinstance(x, float) and isinstance(y, float) and isinstance(z, float)
        ), "all inputs must be float or arrays of same size"
    else:
        assert x.size == y.size and x.size == z.size, "all inputs must be float or arrays of same size"  # type: ignore

    shape = (3, xyz_len) if xyz_len is not None else (3, 1)
    xyz = np.empty(shape, dtype=np.float64)
    lla = np.empty(shape, dtype=np.float64)
    xyz[0, :] = x
    xyz[1, :] = y
    xyz[2, :] = z

    r = np.sqrt(xyz[0, :] * xyz[0, :] + xyz[1, :] * xyz[1, :])
    sel = r > WGS84_POLE_LIMIT
    not_sel = np.logical_not(sel)

    lla[0, not_sel] = np.sign(xyz[2, not_sel]) * np.pi / 2
    lla[1, not_sel] = 0.0
    lla[2, not_sel] = np.abs(xyz[2, not_sel]) - WGS84.b

    Esq = WGS84.a * WGS84.a - WGS84.b * WGS84.b
    F = 54 * WGS84.b * WGS84.b * xyz[2, sel] * xyz[2, sel]
    G = r[sel]  * r[sel]  + (1 - WGS84.esq) * xyz[2, sel] * xyz[2, sel] - WGS84.esq * Esq
    C = (WGS84.esq * WGS84.esq * F * r[sel]  * r[sel] ) / (np.power(G, 3))
    S = np.cbrt(1 + C + np.sqrt(C * C + 2 * C))
    P = F / (3 * np.power((S + 1 / S + 1), 2) * G * G)
    Q = np.sqrt(1 + 2 * WGS84.esq * WGS84.esq * P)
    r_0 = -(P * WGS84.esq * r[sel] ) / (1 + Q) + np.sqrt(
        0.5 * WGS84.a * WGS84.a * (1 + 1.0 / Q)
        - P * (1 - WGS84.esq) * xyz[2, sel] * xyz[2, sel] / (Q * (1 + Q))
        - 0.5 * P * r[sel]  * r[sel] 
    )
    U = np.sqrt(np.power((r[sel]  - WGS84.esq * r_0), 2) + xyz[2, sel] * xyz[2, sel])
    V = np.sqrt(np.power((r[sel]  - WGS84.esq * r_0), 2) + (1 - WGS84.esq) * xyz[2, sel] * xyz[2, sel])
    Z_0 = WGS84.b * WGS84.b * xyz[2, sel] / (WGS84.a * V)
    lla[0, sel] = np.arctan((xyz[2, sel] + WGS84.e1sq * Z_0) / r[sel] )
    lla[1, sel] = np.arctan2(xyz[1, sel], xyz[0, sel])
    lla[2, sel] = U * (1 - WGS84.b * WGS84.b / (WGS84.a * V))

    if degrees:
        lla[:2, :] = np.degrees(lla[:2, :])
    if xyz_len is None:
        lla = lla[:, 0]  # type: ignore

    return lla
