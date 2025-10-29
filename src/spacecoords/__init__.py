"""General purpose convenience functions for different coordinate systems and linear algebra
functions
"""

from types import ModuleType
import importlib.util
from .version import __version__

from . import linalg
from . import spherical


def _make_missing_module(name: str, dep: str):
    class _MissingModule(ModuleType):
        def __getattr__(self, key):
            raise ImportError(
                f"The optional dependency `{dep}` for is missing.\n"
                f"Install it with `pip install spacecoords[all]` or `pip install {dep}`."
            )

    return _MissingModule(name)


# Optional modules
if importlib.util.find_spec("astropy") is not None:
    from . import astropy
else:
    astropy = _make_missing_module("astropy", "astropy")

if importlib.util.find_spec("jplephem") is not None:
    from . import naif_ephemeris
else:
    naif_ephemeris = _make_missing_module("naif_ephemeris", "jplephem")

if importlib.util.find_spec("spiceypy") is not None:
    from . import naif_spice
else:
    naif_spice = _make_missing_module("naif_spice", "spiceypy")

if importlib.util.find_spec("requests") is not None:
    from . import download
else:
    download = _make_missing_module("download", "requests")
