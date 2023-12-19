from __future__ import annotations

import os
import pickle
from typing import TYPE_CHECKING, Any
import xarray as xr
from xarray import Dataset
from xarray.backends.common import AbstractDataStore

if TYPE_CHECKING:
    from io import BufferedIOBase


@xr.register_dataset_accessor("bitdiff")
class DiffAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        self.source = None

    @property
    def source(self) -> object:
        """Return the source of the diff dataset."""
        return pickle.loads(bytes(self._obj.attrs['xbitdiff_source']))

    @source.setter
    def source(self, filename_or_obj: str) -> None:
        """Convert source to a list() that can be stored as a netcdf attribute."""
        self._obj.attrs['xbitdiff_source'] = list(pickle.dumps(filename_or_obj))

    def patch(self, diff: Dataset) -> Dataset:
        """Patch an array using a diff array.

        Patch adds the diff array to the original array, which is equivalent to a bitwise OR
        (|) operation.

        Returns
        -------
        dataset : Dataset
            The patched dataset.
        """

        output = self._obj + diff
        # TODO warn if the datasets do not have the same source
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
        if source.bitdiff.source is None:
            raise AttributeError(
                "The source dataset does not specifiy its source filename. "
                "Open the dataset with xbitdiff.open_dataset() or set the "
                "source mannually with dataset.bitdiff.source = 'filename'."
            )

        output = source - self._obj
        output.bitdiff.source = source.bitdiff.source
        return output


def open_dataset(
    filename_or_obj: str | os.PathLike[Any] | BufferedIOBase | AbstractDataStore,
    source_filename: str | os.PathLike[Any] | BufferedIOBase | AbstractDataStore = None,
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

    source_filename : str, Path, file-like or DataStore
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
        source_ds.bitdiff.source = source_filename
        output = source_ds.bitdiff.patch(diff_ds)

    elif diff_ds.bitdiff.source:
        source_ds = xr.open_dataset(diff_ds.source, **kwargs)
        source_ds.bitdiff.source = diff_ds.bitdiff.source
        output = source_ds.bitdiff.patch(diff_ds)

    else:
        output = diff_ds
        output.bitdiff.source = filename_or_obj

    return output
