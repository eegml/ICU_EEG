# Matlab python interoperability

-The [mat4py](https://github.com/nephics/mat4py) packages works very well for mat files in Matlab v5 format. I think this is better than the scipy.io.loadmat

- h5py can be used for matlab version 7.3+ mat files but there are some tricks I had to use to deal with hdf5 references. These are used sometimes but not always for string storage by matlab.

### unicode string representation

matlab stores strings as utf-16
if you are dealing with regular arrays of uint16, this works:

```
def ndarray_uint16_utf16_to_string(arr):
    assert arr.dtype == np.uint16
    arr_bytes = arr.tobytes()
    arr_str = arr_bytes.decode('utf-16')
    return arr_str
```

But sometimes you get a dataset of hdf5 references.
For example:
```ipython
In [1]: import h5py

In [2]: hf = h5py.File('annot_1.mat')
In [3]: hf
Out[3]: <HDF5 file \"annot_1.mat\" (mode r)>

In [4]: dsobj = hf['annot']['patient']
In [5]: dsobj
Out[5]: <HDF5 dataset "patient": shape (1, 1), type "|O">

In [6]: dsobj.len(), dsobj.shape
Out[6]: (1, (1, 1))
```
The key thing is that the dtype of this data is object:
```ipython
In [7]: dsobj.dtype
Out[7]: dtype('O')
```
Given that the shape of the dataset is (1,1), we can get that single object with
```
In [8]: ref = dsobj[0,0]

In [9]: ref
Out[9]: <HDF5 object reference>
```
"De-referencing" is done from what I can tell by using the root group. Note these referenced data sets are stored in the '#refs#' group
```ipython
In [11]: deref = hf[ref]
    ...: deref
Out[11]: <HDF5 dataset "b": shape (17, 1), type "<u2">

In [12]: derefarr = deref[:] # dataset -> numpy array

In [13]: derefarr
Out[13]: 
array([[ 73],
       [ 67],
       [ 85],
       [ 68],
       [ 97],
       [116],
       [ 97],
       [ 82],
       [101],
       [100],
       [117],
       [120],
       [ 95],
       [ 48],
       [ 48],
       [ 54],
       [ 48]], dtype=uint16)
```
Finally, we can treat it like all matlab strings and use the fact that we know it is utf-16 encoded to get its value into a python string.

```ipython
In [14]: derefarr.tobytes().decode('utf-16')
Out[14]: 'ICUDataRedux_0060'
```
#### Other options:

[hdf5storage](https://github.com/frejanordsiek/hdf5storage)
