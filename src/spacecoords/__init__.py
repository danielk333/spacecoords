"""General purpose convenience functions for different coordinate systems and linear algebra
functions
"""

import types
import importlib.util
from .version import __version__

from . import linalg
from . import spherical

# Modules
if importlib.util.find_spec("astropy") is not None:
    from . import astropy
else:

    class _MissingModule(types.ModuleType):
        def __getattr__(self, name):
            raise ImportError(
                "The optional dependency `astropy` for is missing.\n"
                "Install it with `pip install spacecoords[all]` or `pip install astropy`."
            )

    astropy = _MissingModule("astropy")
