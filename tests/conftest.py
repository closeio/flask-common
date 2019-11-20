from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import sys

if sys.version_info[0] > 2:
    collect_ignore = [
        'test_legacy.py',
        'test_declenum.py',
        'test_formfields.py',
        'test_crypto.py',
        'mongo',
    ]
