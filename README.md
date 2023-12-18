# xbitdiff

WARNING: This package does not work yet.

We store lot of redundant information, and in the era of big data, those costs add up.
`xbitdiff` is a simple wrapper around xarray for creating data diffs that can help reduce storage costs.
The name `xbitdiff` is an homage to `xbitinfo` but packages are not directly related.

Here's a typical scenario:
You host several large datasets.
Perhaps one is the output of a climate model along with a bias-corrected version.
Or perhaps a large ensemble of models forced with different climate scenarios, like CMIP.
Each of those datasets contains a substantial amount of redundant information.
A simple strategy to reduce the storage footprint is to compute the difference or "diff" of one dataset and another,
then store the original and the diff,
which compresses better than the full dataset.
`xbitdiff` helps abstract diff management behind the scenes,
so the user can work with datasets, not diffs.
