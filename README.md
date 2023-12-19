# xbitdiff

We store lot of redundant information, and in the era of big data, those costs add up.
`xbitdiff` is a simple wrapper around `xarray` for differential compression.
Given two data sets---a source and a target---differential compression stores the source and the difference 
between the source and the target, known as a diff.
When coupled with compression, the size of the diff can be substantially smaller than the size of the target.
How well differential compression works depends on the correlation (redudancy) between the source and the target.
The name `xbitdiff` is an homage to `xbitinfo` but the packages are not directly related.

`xbitdiff` can be install using `pip`
```sh
pip install xbitdiff
```
