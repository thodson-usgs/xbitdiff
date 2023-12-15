from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any
import xarray as xr
from xarray import Dataset
from xarray.backends.common import AbstractDataStore

if TYPE_CHECKING:
    from io import BufferedIOBase


# TODO these are methods, so patch and diff only
@xr.register_dataset_accessor("xdiff")
class DiffAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        self._source_file = None

    def patch(self, diff: xr.Dataset) -> xr.Dataset:
        """Patch an array using a diff array.

        Patch adds the diff array to the original array, which is equivalent to a bitwise OR
        (|) operation.

        Returns
        -------
        dataset : Dataset
            The patched dataset.
        """

        output = self._obj + diff
        # TODO: if no source file, warn
        output._source_file = diff._source_file
        return output

    def diff(self, source: Dataset) -> Dataset:
        """Return the bitwise difference between two arrays.

        Diff takes the difference between two arrays, which is equivalent to a
        bitwise AND (&) and bitwise complement (~) operation.

        Parameters
        ----------
        source : Dataset
            The source dataset from which to compute the diff.

        Returns
        -------
        dataset : Dataset
            The diff dataset.
        """
        output = source - self._obj
        output._source_file = self._source_file
        return output


def open_dataset(
    filename_or_obj: str | os.PathLike[Any] | BufferedIOBase,
    AbstractDataStore,
    source_filename: str = None,
    **kwargs,
) -> Dataset:
    """Open a dataset from a file.

    Parameters
    ----------
    filename_or_obj : str, Path, file-like or DataStore
    Strings and Path objects are interpreted as a path to a netCDF file
    or an OpenDAP URL and opened with python-netCDF4, unless the filename
    ends with .gz, in which case the file is gunzipped and opened with
    scipy.io.netcdf (only netCDF3 supported). Byte-strings or file-like
    objects are opened by scipy.io.netcdf (netCDF3) or h5py (netCDF4/HDF).

    source_filename : str
        Path to the source dataset.

    **kwards : dict
        Additional arguments passed to xarray.open_dataset.

    Returns
    -------
    dataset : Dataset
        The patched dataset dataset.
    """

    diff_ds = xr.open_dataset(filename_or_obj, **kwargs)

    if source_filename:
        source_ds = xr.open_dataset(source_filename, **kwargs)
        output = source_ds.xdiff.patch(diff_ds)

    # check whether key exists properly
    elif diff_ds._source_file:
        source_ds = xr.open_dataset(diff_ds._source_file, **kwargs)
        output = source_ds.xdiff.patch(diff_ds)

    else:
        source_filename = filename_or_obj
        output = diff_ds

    return output
