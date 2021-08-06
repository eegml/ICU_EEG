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
import pandas as pd
import numpy as np
import yaml
import json

# %% [markdown]
# Early notes: There are some subjects in the repository which were not ultimately used in the published form of this project (in particular, anything with 'IIC' in it - these were interictal - ictal continuum patients which we did not want to use in training the model), as well as a few others which clinicians on our team judged to have insufficient data quality. We also had to re-upload files recently under new IDs on ieeg.org for deidentification purposes which may have made some of the annotation files fail. 
#
# It looks like the annotations are labeled in seconds.
# I'm not sure what the ii_start and ii_start are for.

# %%
pt_df = pd.read_csv('patient_table.csv')

# %%
pt_df

# %%
pt_df = pt_df.sort_values(by='annotation_no')
pt_df.to_csv('patient_table_sorted.csv',index=False)

# %%
annotations = yaml.safe_load(open('Data/annotations.yaml'))

# %%
ptdf2 = pt_df.set_index(['annotation_no'])
ptdatadict = ptdf2.to_dict(orient='index')

# %%
len(ptdatadict)
ptdatadict

# %%
for anum,data in annotations.items():
    num = int(anum)
    if num in ptdatadict:
        #print(f"{type(data)}")
        #print(f"{data}")
        data['portal_id'] = ptdatadict[num]['portal_id']
        data['sz_presence'] = ptdatadict[num]['sz_presence']
        data['diagnosis'] = ptdatadict[num]['diagnosis']
        if ptdatadict[num]['sz_presence']:
            data['pt_type'] = 1
        else:
            data['pt_type'] = 2
        del data['type']

# %%
yaml.safe_dump(annotations, open('patient_annotations.yaml','w+'))
json.dump(annotations, open('patient_annotations.json','w+'), indent=2)

# %%
annotations

# %%
