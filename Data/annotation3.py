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
# after John B. cleanup
# the annotation file format has changed
# !git reflog
# 1edc29b (HEAD -> exploration) HEAD@{0}: commit (merge): merge in John updates 2021-08-04
# d1a63a4 (origin/exploration) HEAD@{1}: commit: add csv version of Table S1
# %%
import yaml
import json
import glob
import itertools 
import random

import scipy.io as sio
import h5py
import mat4py # even more convenient that scipy.io.loadmat for v5
import numpy as np

# %% [markdown]
# jbernabei has stored the annotations as matlab v5 and v7.3 (hdf5) files
# - each file stores information under the following variables. 
#   - data_start : when present 1x1 float -- likely integer time in second
#   - data_stop : when present 1x1 float -- integer time in second
#   - patient : uint16 or unicode string
#   - 'ii_start' : matrix 1xn float if present : these are 
#   - 'ii_stop' : matrix 1xn float if present
#   - 'iic_start' : matrix 1xn float if present 
#   - 'iic_stop': matrix 1xn float if present
#   - 'sz_start' : matrix 1xn float if present
#   - 'sz_stop' : matrix 1xn float if present
#   - type :  1.0 | 2.0 | 3.0 |4.0   or not present
# It looks like 
# %%
LIST_TYPE_KEYS = ['ii_start', 'ii_stop', 'iic_start','iic_stop', 'sz_start','sz_stop']
SCALAR_INT_TYPE_KEYS = ['data_stop', 'data_start', 'type', 'file_num']
# the 'patient' field is often utf-16 hdf object reference so needs
# special work to decode

# %%
asbytes_latin1 = lambda s: s.encode('latin1') # may want utf-8
asstr_latin1 = lambda b: b.decode('latin1')

asbytes_utf8 = lambda s: s.encode('utf-8') # may want utf-8
asstr_utf8 = lambda b: b.decode('utf-8')

# %% [markdown]
# MATLAB stores all characters as Unicode characters using the UTF-16 encoding, where every character is represented by a numeric code value. (Unicode incorporates the ASCII character set as the first 128 symbols, so ASCII characters have the same numeric codes in Unicode and ASCII.) Both character arrays and string arrays use this encoding. You can convert characters to their numeric code values by using various numeric conversion functions. You can convert numbers to characters using the char function.
# [link to matlab docs for R2021a](https://www.mathworks.com/help/matlab/matlab_prog/unicode-and-ascii-values.html#:~:text=MATLAB%C2%AE%20stores%20all%20characters,by%20a%20numeric%20code%20value.&text=Both%20character%20arrays%20and%20string%20arrays%20use%20this%20encoding)
# %%
def ndarray_uint16tr_to_string(arr):
    arr_uint = arr.astype('uint8') # truncate off 2nd byte np.unicode_ type instead? or just use utf-16
    arr_bytes = arr_uint.tobytes()
    return asstr_utf8(arr_bytes)

def ndarray_uint16_utf16_to_string(arr):
    assert arr.dtype == np.uint16
    arr_bytes = arr.tobytes()
    arr_str = arr_bytes.decode('utf-16')
    return arr_str



# def hdf_utf16_to_string(hdf, ds):
#     assert arr.dtype == np.object_  # then it is an dataset of type object
        
#     if arr.dtype == np.unit16:
#         arr_bytes = arr.tobytes()
#         arr_str = arr_bytes.decode('utf-16')
#         return arr_str



# %%
annotation_files = glob.glob('a*.mat')

# %%
def annotation_file_key(afile):
    sp = afile.split('_')
    num = int(sp[1][:-4])
    return num 

annotation_files.sort(key=annotation_file_key)


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
        a = h['annot']

        datasets = {}
        for kk,vv  in a.items():
            #print(f"{kk}: {vv[:]=}")
            if vv.dtype == np.object_: # this assumes dataset has just one element
                deref = h[vv[0][0]] # get reference[0][0] and "dereference"
                tmparr = deref[:]
                datasets[kk] = tmparr # convert to uint16 array
            else:
                datasets[kk] = vv[:]
            # if want to track which mat file format it came from
            #datasets['mat_version'] = '7.3'


        ann[num] = datasets 
       
    except OSError:
        print(f"problems opening {afile}")
        errorfiles.append(afile) 
    

    #h = h5py.File(afile)

# %%
len(ann)
## testing de-referencing in hdf5 files
# for kk, vv in hf1['annot'].items():
#     print(f"{type(vv)}, {vv.dtype=}")
#     if vv.dtype == np.object_:
#         print(hf1[vv[0][0]])
#         tmp = hf1[vv[0][0]]
#         tmparr = tmp[:]
#         print(f"{tmparr=}")
# %%
# fix those annotations
for kk, aa in ann.items():
    for jj, vv in aa.items():
        aa[jj] = np.squeeze(vv)
    aa['patient'] = ndarray_uint16_utf16_to_string(aa['patient'])
    #aa['patient'] = ndarray_uint16_to_string(aa['patient'])


# %%

# %%

# random_annotation = random.choice(ann)
# %%
#random_annotation['patient']

# %%
# handle the mat version 5 files
for fn in errorfiles:
    sp = fn.split('_')
    num_str = sp[1][:-4]
    annot_name = fn[:-4]
    num = int(num_str)
    print(f"{fn=},{num=}, {annot_name=}")
    data = mat4py.loadmat(fn)
    # if want to track file format version
    # data['mat_version'] = '5'
    print(data)
    ann[num] = data['annot'] 


# %%
# now we may as well convert things to python lists given how short these arrays are

for kk in ann:
    data = ann[kk]
    for ii,vv in data.items():
        if type(vv) == np.ndarray:
            data[ii] = vv.tolist()


# %% make it so
# the big type clean up 
for kk, data in ann.items():
    for ii,vv in data.items():
        if type(vv) == list: # could replace with if ii in LIST_TYPE_KEYS?
            data[ii] = [int(val) for val in vv if val == int(val)]
        if type(vv) == float:
            assert vv == int(vv)
            if ii in LIST_TYPE_KEYS:
                data[ii] = [int(vv)]  # make it so that they are always a list
            if ii in SCALAR_INT_TYPE_KEYS:
                data[ii] = int(vv)
                
        if type(vv) == int:
            if ii in LIST_TYPE_KEYS:
                data[ii] = [vv] # make it so 


# %%
# %% [markdown]
# #### reading through pull_data.m
# ii_start and ii_stop are related to interictal start and stop timesince
# ```
# for files with seizures (type=1)
# when not given, the dataset acquistions times are inferred
#
# dataset_start is the minimum of (ii_start, ii_stop, sz_start, sz_stop)
# dataset_stop = max(ii_start, ii_stop, sz_start, sz_stop)
#
# for type==2, seizure free patient files
# there are again interictal start/stop times ii_start and ii_stop
#
# and the dataset_start/stop are ii_start/ii_stop 

# type ==3 is for the "IIC" or interictal continuum patients 
# ```

# ## Important
# the mat v5 files do not contain data start/stop annotations
# %%

from collections.abc import Iterable
gen_flatten = lambda *n: (e for a in n
                            for e in (gen_flatten(*a) if isinstance(a, Iterable) else (a,)))

def flatten_list(*l):
    return list(gen_flatten(*l))

# %%
for kk, an in ann.items():
    if 'type' not in an:
        print(f"{kk=}, {an=} does not have a type")
        an['type'] = -1
    # check
    present_keys = [ss for ss in ['iic_start','iic_stop','ii_start','ii_stop',
                        'sz_start', 'sz_stop'] if ss in an]
    check_list = [an[ss] for ss in present_keys]
    print(f"{check_list=}")

    check_these = flatten_list(check_list) # flatten
    allarr = np.array(check_these)
    if an['type'] == 1: # seizure file
        if 'data_start' not in an:
            an['data_start'] = int(np.min(allarr))
        if 'data_stop' not in an:
            an['data_stop'] = int(np.max(allarr))
    elif an['type'] == 2: # seizure free
        if 'data_start' not in an:
            #an['data_start'] = np.min(min(an['ii_start']), min(an['ii_stop']) )
            an['data_start'] = int(np.min(allarr ))
        if 'data_stop' not in an:
            #an['data_stop'] = np.max([ max(an['ii_start']), max(an['ii_stop'])])
            an['data_stop'] = int(np.max(allarr))
    elif an['type'] == 3: # interictal continuum
        if 'data_start' not in an:
            #an['data_start'] = np.min((min(an[ss]) for ss in check_these) )
            an['data_start'] = int(np.min(allarr))
        if 'data_stop' not in an:
            #an['data_stop'] = np.max(max(an[ss]) for ss in check_these)
            an['data_stop'] = int(np.max(allarr))
    else:
        if 'data_start' not in an:
            #an['data_start'] = np.min((min(an[ss]) for ss in check_these) )
            an['data_start'] = int(np.min(allarr))
        if 'data_stop' not in an:
            #an['data_stop'] = np.max(max(an[ss]) for ss in check_these)
            an['data_stop'] = int(np.max(allarr))


# %%
# little test
tst = {'a': [1,3,5],
'b': [3, 4,7]}
check_this = [ss for ss in ['a','b','c'] if ss in tst]
check_this
# %%
# make a sorted version

ann_keys = list(ann.keys())
ann_keys.sort()
ann_sorted = {kk:ann[kk] for kk in ann_keys}

open('annotations_repr.py','w+').write(f"annotations = {repr(ann_sorted)}") # should format this with black

# %%
yaml.safe_dump(ann_sorted, open('annotations.yaml','w+'))


# %%
json.dump(ann_sorted, open('annotations.json', 'w+'), indent=2)

# %%
