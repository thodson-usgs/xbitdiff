from importlib.metadata import PackageNotFoundError, version

from xdiff.accessor import *

try:
    __version__ = version('xdiff')
except PackageNotFoundError:
    __version__ = 'version-unknown'
