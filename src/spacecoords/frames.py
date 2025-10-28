#!/usr/bin/env python

"""Transforms between common coordinate frames without any additional dependencies
"""

import numpy as np
from .spherical import sph_to_cart


def ned_to_ecef(lat, lon, alt, ned, degrees=True):
    """NED (north/east/down) using geocentric zenith to ECEF coordinate system
    conversion, not including translation.

    :param float lat: Latitude of the origin in geocentric spherical coordinates
    :param float lon: Longitude of the origin in geocentric spherical coordinates
    :param float alt: Altitude **Unused in this implementation**.
    :param numpy.ndarray ned: (3,n) input matrix of positions in the NED-convention.
    :param bool radians: If :code:`True` then all values are given in radians instead of degrees.
    :rtype: numpy.ndarray
    :return: (3,n) array x,y and z coordinates in ECEF.
    """
    enu = np.empty(ned.size, dtype=ned.dtype)
    enu[0, ...] = ned[1, ...]
    enu[1, ...] = ned[0, ...]
    enu[2, ...] = -ned[2, ...]
    return enu_to_ecef(lat, lon, alt, enu, degrees=degrees)


def azel_to_ecef(lat, lon, alt, az, el, degrees=True):
    """Radar pointing (az,el) using geocentric zenith to unit vector in
    ECEF, not including translation.

    TODO: Docstring
    """
    shape = (3,)

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
    return enu_to_ecef(lat, lon, alt, enu, degrees=degrees)


def enu_to_ecef(lat, lon, alt, enu, degrees=True):
    """ENU (east/north/up) using geocentric zenith to ECEF coordinate system
    conversion, not including translation.

    :param float lat: Latitude of the origin in geocentric spherical coordinates
    :param float lon: Longitude of the origin in geocentric spherical coordinates
    :param float alt: Altitude above ellipsoid, **Unused in this implementation**.
    :param numpy.ndarray enu: (3,n) input matrix of positions in the ENU-convention.
    :param bool radians: If :code:`True` then all values are given in radians instead of degrees.
    :rtype: numpy.ndarray
    :return: (3,n) array x,y and z coordinates in ECEF.
    """
    if degrees:
        lat, lon = np.radians(lat), np.radians(lon)

    mx = np.array(
        [
            [-np.sin(lon), -np.sin(lat) * np.cos(lon), np.cos(lat) * np.cos(lon)],
            [np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat) * np.sin(lon)],
            [0, np.cos(lat), np.sin(lat)],
        ]
    )

    ecef = np.dot(mx, enu)
    return ecef


def ecef_to_enu(lat, lon, alt, ecef, degrees=True):
    """ECEF coordinate system to local ENU (east,north,up) using geocentric
    zenith, not including translation.

    :param float lat: Latitude of the origin in geocentric spherical coordinates
    :param float lon: Longitude of the origin in geocentric spherical coordinates
    :param float alt: Altitude **Unused in this implementation**.
    :param numpy.ndarray ecef: (3,n) array x,y and z coordinates in ECEF.
    :param bool radians: If :code:`True` then all values are given in radians instead of degrees.
    :rtype: numpy.ndarray
    :return: (3,n) array x,y and z in local coordinates in the
        ENU-convention using geocentric zenith.
    """
    if degrees:
        lat, lon = np.radians(lat), np.radians(lon)

    mx = np.array(
        [
            [-np.sin(lon), -np.sin(lat) * np.cos(lon), np.cos(lat) * np.cos(lon)],
            [np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat) * np.sin(lon)],
            [0, np.cos(lat), np.sin(lat)],
        ]
    )
    enu = np.dot(np.linalg.inv(mx), ecef)
    return enu
