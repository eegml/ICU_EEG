# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: 'Python 3.8.10 64-bit (''mne'': conda)'
#     name: python3
# ---

# %%
import scipy.io as sio
import h5py
import mat4py # even more convenient that scipy.io.loadmat for v5
import numpy as np
import yaml
import json

# %%
import glob

# %%
asbytes_latin1 = lambda s: s.encode('latin1') # may want utf-8
asstr_latin1 = lambda b: b.decode('latin1')

def ndarray_uint16_to_string(arr):
    arr_uint = arr.astype('uint8') # truncate off 2nd byte
    arr_bytes = arr_uint.tobytes()
    return asstr_latin1(arr_bytes)



# %%
annotation_files = glob.glob('a*.mat')

# %%
annotation_files.sort()
afile = annotation_files[0]

# %%
# try a single file
h = h5py.File(afile)

# %%
list(h.attrs.items())

# %%
list(h.keys())

# %%
a = h['annot_1']

# %%
list(a.attrs.items()) # this shows the names of the fields as arrays of |S1 dtype

# %%
list(a.items())

# %%
datasets = {}
for kk,vv  in a.items():
    print(f"{kk}: {vv[:]=}")
    datasets[kk] = vv[:]

# %%
#import tables
datasets

# %%
list(h['#refs#'].items())

# %%
ann = {}
errorfiles = []

for afile in annotation_files:
    sp = afile.split('_')
    num_str = sp[1][:-4]
    annot_name = afile[:-4]
    num = int(num_str)
    #print(f"working on {annot_name=} {num} from file {afile}")
    try:
        h = h5py.File(afile)
        
        #print(f"{list(h.keys())}")
        a = h[annot_name]
        datasets = {}
        for kk,vv  in a.items():
            #print(f"{kk}: {vv[:]=}")
            datasets[kk] = vv[:]
        ann[num] = datasets 
    except OSError:
        print(f"problems opening {afile}")
        errorfiles.append(afile) 
    

    #h = h5py.File(afile)

# %%
len(ann)

# %%
# fix those annotations
for kk, aa in ann.items():
    for jj, vv in aa.items():
        aa[jj] = np.squeeze(vv)
    aa['patient'] = ndarray_uint16_to_string(aa['patient'])

ann[1]

# %%
pt = ann[1]['patient']

# %%
for fn in errorfiles:
    sp = fn.split('_')
    num_str = sp[1][:-4]
    annot_name = fn[:-4]
    num = int(num_str)
    print(f"{fn=},{num=}, {annot_name=}")
    data = mat4py.loadmat(fn)
    print(data)
    ann[num] = data[annot_name] 

# %%
yaml.dump(ann, open('annotations_numpy.yaml','w+'))

# %% [markdown]
# ## Important
# the mat v5 files do not contain data start/stop annotations

# %%
ann[6]

# %%
ann[1]

# %%
# now we may as well convert things to python lists given how short these arrays are
for kk in ann:
    data = ann[kk]
    for ii,vv in data.items():
        if type(vv) == np.ndarray:
            data[ii] = vv.tolist()


# %%
ann[1]

# %%
yaml.dump(ann, open('annotations_floats.yaml','w+'))

# %%
#annpy = yaml.safe_load(open('annotations_floats.yaml'))

# %%
for kk, data in ann.items():
    for ii,vv in data.items():
        if type(vv) == list:
            data[ii] = [int(val) for val in vv]
        if type(vv) == float:
            data[ii] = int(vv)

# %%
yaml.safe_dump(ann, open('annotations.yaml','w+'))


# %%
json.dump(ann, open('annotations.json', 'w+'))

# %%
ann

# %%
import hdf5storage

# %%
#json.dump(annpy, open('annotations.json', 'w'))
# yaml.safe_dump(annpy, open('annotations.yaml', 'w'))

# %%
afile

# %%
# hdf5storage is based upon h5py and is supposed to support matlab 7.3 format
# let's see what it is does.
import collections as cl
import numpy as np
options = hdf5storage.Options(matlab_compatible=True)
matfile = hdf5storage.read(filename=afile, options=options)

# %%
matfile

# %%
matfile['annot_99']

# %%
matfile.dtype

# %%
np.squeeze(matfile['annot_99']['patient']) # dtype='<U17' means a 17 character unicode string, so it handles unicode better

# %%
matfile['annot_99']['iic_stop']

# %%
np.squeeze(matfile['annot_99']['iic_start'])

# %%
