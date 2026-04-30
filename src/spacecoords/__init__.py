"""General purpose convenience functions for different coordinate systems and linear algebra
functions
"""

import importlib.util
from types import ModuleType

from . import constants, hammer_aitoff, interpolation, linalg, projection, spherical
from .version import __version__


def _make_missing_module(name: str, dep: str) -> ModuleType:
    class _MissingModule(ModuleType):
        def __getattr__(self, key: str) -> None:
            raise ImportError(
                f"The optional dependency `{dep}` for is missing.\n"
                f"Install it with `pip install spacecoords[all]` or `pip install {dep}`."
            )

    return _MissingModule(name)


# Optional modules
if importlib.util.find_spec("astropy") is not None:
    from . import celestial, radiant
else:
    celestial = _make_missing_module("celestial", "astropy")
    radiant = _make_missing_module("radiant", "astropy")

if importlib.util.find_spec("jplephem") is not None:
    from . import spk_basic
else:
    spk_basic = _make_missing_module("spk_basic", "jplephem")

if importlib.util.find_spec("spiceypy") is not None:
    from . import spice
else:
    spice = _make_missing_module("spice", "spiceypy")

if importlib.util.find_spec("requests") is not None:
    from . import download
else:
    download = _make_missing_module("download", "requests")
