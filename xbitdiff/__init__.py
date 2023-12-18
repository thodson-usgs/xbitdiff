from importlib.metadata import PackageNotFoundError, version

from xbitdiff.accessor import *

try:
    __version__ = version('xbitdiff')
except PackageNotFoundError:
    __version__ = 'version-unknown'
