```{.python .input  n=1}
import h5py

hf = h5py.File('Data/annot_1.mat')
hf
```

```{.json .output n=1}
[
 {
  "data": {
   "text/plain": "<HDF5 file \"annot_1.mat\" (mode r)>"
  },
  "execution_count": 1,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=2}

dsobj = hf['annot']['patient']
dsobj
```

```{.json .output n=2}
[
 {
  "data": {
   "text/plain": "<HDF5 dataset \"patient\": shape (1, 1), type \"|O\">"
  },
  "execution_count": 2,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=3}
dsobj.len()
```

```{.json .output n=3}
[
 {
  "data": {
   "text/plain": "1"
  },
  "execution_count": 3,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=4}
dsobj.shape
```

```{.json .output n=4}
[
 {
  "data": {
   "text/plain": "(1, 1)"
  },
  "execution_count": 4,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=5}
type(dsobj)
```

```{.json .output n=5}
[
 {
  "data": {
   "text/plain": "h5py._hl.dataset.Dataset"
  },
  "execution_count": 5,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=6}
type(dsobj) == h5py.Dataset

```

```{.json .output n=6}
[
 {
  "data": {
   "text/plain": "True"
  },
  "execution_count": 6,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=7}
ref = dsobj[0][0]
ref


```

```{.json .output n=7}
[
 {
  "data": {
   "text/plain": "<HDF5 object reference>"
  },
  "execution_count": 7,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=8}
deref = hf[ref]
deref

```

```{.json .output n=8}
[
 {
  "data": {
   "text/plain": "<HDF5 dataset \"b\": shape (17, 1), type \"<u2\">"
  },
  "execution_count": 8,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=9}
ndarr = dref[:]
ndarr
```

```{.json .output n=9}
[
 {
  "ename": "NameError",
  "evalue": "name 'dref' is not defined",
  "output_type": "error",
  "traceback": [
   "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
   "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
   "\u001b[0;32m/mnt/data2/eegdbs2/jbernabei-icu-eeg/ICU_EEG/read_hdf_v73_annot_1.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mndarr\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdref\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0mndarr\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
   "\u001b[0;31mNameError\u001b[0m: name 'dref' is not defined"
  ]
 }
]
```

```{.python .input  n=10}
ndarr = deref[:]
ndarr
```

```{.json .output n=10}
[
 {
  "data": {
   "text/plain": "array([[ 73],\n       [ 67],\n       [ 85],\n       [ 68],\n       [ 97],\n       [116],\n       [ 97],\n       [ 82],\n       [101],\n       [100],\n       [117],\n       [120],\n       [ 95],\n       [ 48],\n       [ 48],\n       [ 54],\n       [ 48]], dtype=uint16)"
  },
  "execution_count": 10,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

```{.python .input  n=11}
ndarr.tobytes().decode('utf-16')

```

```{.json .output n=11}
[
 {
  "data": {
   "text/plain": "'ICUDataRedux_0060'"
  },
  "execution_count": 11,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```
