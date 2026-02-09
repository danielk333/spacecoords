import unittest
import numpy as np
import numpy.testing as nt
from astropy.time import Time

from spacecoords import celestial


class TestKernelLoad(unittest.TestCase):
    def test_astropy_get_body(self):
        # TODO - get kernel path from pytest cli with "fixture" (?) and skip if not given
        # pos, vel = celestial.astropy_get_body("Earth", Time("2026-01-01"), None)
        raise NotImplementedError()
