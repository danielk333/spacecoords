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
