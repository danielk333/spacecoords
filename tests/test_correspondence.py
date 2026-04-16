#!/usr/bin/env python

""" """

import unittest
import numpy as np
import numpy.testing as nt

from spacecoords import frames
from spacecoords import celestial


class ECEFRelatedFuncs(unittest.TestCase):

    def test_wgs84_frames_vs_astropy(self):
        lat = 67 + 50 / 60 + 26.6 / 3600
        lon = 20 + 24 / 60 + 40.0 / 3600
        alt = 425
        loc_itrs = celestial.geodetic_to_ITRS(lat, lon, alt, degrees=True)
        loc_itrs_2 = frames.geodetic_wgs84_to_ecef(lat, lon, alt, degrees=True)

        nt.assert_array_almost_equal(loc_itrs_2, loc_itrs, decimal=7)

        latm = np.linspace(-10, 10, 100)
        lonm = np.ones_like(latm)
        altm = 425 * np.ones_like(latm)
        loc_itrsm = celestial.geodetic_to_ITRS(latm, lonm, altm, degrees=True)
        loc_itrsm_2 = frames.geodetic_wgs84_to_ecef(latm, lonm, altm, degrees=True)

        nt.assert_array_almost_equal(loc_itrsm_2, loc_itrsm, decimal=7)

    def test_enu_to_ecef_via_geoditics(self):
        lat1 = 67 + 50 / 60 + 26.6 / 3600
        lon1 = 20 + 24 / 60 + 40.0 / 3600
        alt1 = 425

        lat2 = lat1 + 1
        lon2 = lon1
        alt2 = 0
        loc_itrs_1 = celestial.geodetic_to_ITRS(lat1, lon1, alt1, degrees=True)
        loc_itrs_2 = celestial.geodetic_to_ITRS(lat2, lon2, alt2, degrees=True)
        lat1, lon1, alt1 = celestial.geodetic_lla_to_geocentric_lla(lat1, lon1, alt1, degrees=True)
        lat2, lon2, alt2 = celestial.geodetic_lla_to_geocentric_lla(lat2, lon2, alt2, degrees=True)

        itrs_target = loc_itrs_1 + np.array([0, 100e3, 100e3])
        enu1_target = frames.ecef_to_enu(lat1, lon1, itrs_target - loc_itrs_1, degrees=True)
        enu2_target = frames.ecef_to_enu(lat2, lon2, itrs_target - loc_itrs_2, degrees=True)
        r1 = np.linalg.norm(enu1_target)
        r2 = np.linalg.norm(enu2_target)
        enu1_dir1 = enu1_target / r1
        enu2_dir2 = enu2_target / r2

        itrs1_target = frames.enu_to_ecef(lat1, lon1, enu1_dir1, degrees=True)
        itrs2_target = frames.enu_to_ecef(lat2, lon2, enu2_dir2, degrees=True)

        nt.assert_almost_equal(
            loc_itrs_1 + itrs1_target * r1,
            loc_itrs_2 + itrs2_target * r2,
            decimal=6,
        )

        enu1_loc2 = frames.ecef_to_enu(lat1, lon1, loc_itrs_2 - loc_itrs_1, degrees=True)
        enu1_dir2 = frames.ecef_to_enu(lat1, lon1, itrs2_target, degrees=True)
        nt.assert_almost_equal(
            enu1_target,
            enu1_loc2 + enu1_dir2 * r2,
            decimal=6,
        )
