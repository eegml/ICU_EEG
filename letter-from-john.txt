Bernabei, John <John.Bernabei@pennmedicine.upenn.edu>
Thu 7/29/2021 20:28


Hello Chris,

Thank you for your interest, and I apologize for those GitHub issues. There are some subjects in the repository which were not ultimately used in the published form of this project (in particular, anything with 'IIC' in it - these were interictal - ictal continuum patients which we did not want to use in training the model), as well as a few others which clinicians on our team judged to have insufficient data quality. We also had to re-upload files recently under new IDs on ieeg.org for deidentification purposes which may have made some of the annotation files fail. 

If it is okay with you, I can re-check your issue and clean up a few things on the GitHub next week. I'll get back to you next week when this is complete.

Best,

John 


reading through pull_data.m
ii_start and ii_stop are related to interictal start and stop timesince

for files with seizures (type=1)
when not given, the dataset acquistions times are inferred
dataset_start is the minimum of (ii_start, ii_stop, sz_start, sz_stop)
dataset_stop = max(ii_start, ii_stop, sz_start, sz_stop)

for type==2, seizure free patient files
there are again interictal start/stop times ii_start and ii_stop

and the dataset_start/stop are ii_start/ii_stop 

