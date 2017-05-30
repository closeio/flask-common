# UUID related helpers
try:
    from .id import *
except ImportError:
    pass

# TODO: split these up
try:
    from .legacy import *
except ImportError:
    pass
