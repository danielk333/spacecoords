import pytest
import unittest
import pathlib
import tempfile
import numpy as np
import numpy.testing as nt
from astropy.time import Time

from spacecoords import celestial

au = 149597870700.0

class TestKernelLoad(unittest.TestCase):

    @pytest.mark.need_download
    def test_astropy_get_body(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            state = celestial.astropy_get_body(
                "Earth",
                Time("2025-03-20T09:01:00", format="isot", scale="utc"),
                pathlib.Path(tmpdirname),
            )
        nt.assert_almost_equal(np.linalg.norm(state[:3]) / au, 1, decimal=1)
