# ICU_EEG

This is the final repository for the ICU EEG data reduction project. The
repository is organized into the following folders: Data: This has the annotation
files for all patients we are using in the project. The format is .mat files
where each patient has fields that describe seizure start and stop times as well
as interictal start and stop times.  Features: This folder is where calculated
feature files will go which also store patient specific annotations Models: This
contains machine learning models Results: This contains results

### chris ClM notes
Note, the mat format files are in various versions
pre 5 verion is the old format
post-ver5 is in a hdf5 format with references


### References
This data is from:

A Full-Stack Application for Detecting Seizures and Reducing Data During Continuous Electroencephalogram Monitoring

Bernabei, John M. BSE[1,2]; Owoputi, Olaoluwa BSE[1,2]; Small, Shyon D. BS[1,2]; Nyema, Nathaniel T. BS[1,2]; Dumenyo, Elom BS [1,2]; Kim, Joongwon[1,2]; Baldassano, Steven N. MD, PhD[1,2]; Painter, Christopher MS[1,2]; Conrad, Erin C. MD[3]; Ganguly, Taneeta M. MD[3]; Balu, Ramani MD, PhD[3]; Davis, Kathryn A. MD[2,3]; Levine, Joshua M. MD[3]; Pathmanathan, Jay MD, PhD[3]; Litt, Brian MD[1–4]

DOI: 10.1097/CCE.0000000000000476

https://journals.lww.com/ccejournal/Fulltext/2021/07000/A_Full_Stack_Application_for_Detecting_Seizures.14.aspx

Abstract

BACKGROUND: 
Continuous electroencephalogram monitoring is associated with lower mortality in
critically ill patients; however, it is underused due to the resource-intensive
nature of manually interpreting prolonged streams of continuous
electroencephalogram data. Here, we present a novel real-time, machine
learning–based alerting and monitoring system for epilepsy and seizures that
dramatically reduces the amount of manual electroencephalogram review.

METHODS: 
We developed a custom data reduction algorithm using a random forest and deployed
it within an online cloud-based platform, which streams data and communicates
interactively with caregivers via a web interface to display algorithm
results. We developed real-time, machine learning–based alerting and monitoring
system for epilepsy and seizures on continuous electroencephalogram recordings
from 77 patients undergoing routine scalp ICU electroencephalogram monitoring and
tested it on an additional 20 patients.

RESULTS 
We achieved a mean seizure sensitivity of 84% in cross-validation and 85% in
testing, as well as a mean specificity of 83% in cross-validation and 86% in
testing, corresponding to a high level of data reduction. This study validates a
platform for machine learning–assisted continuous electroencephalogram analysis
and represents a meaningful step toward improving utility and decreasing cost of
continuous electroencephalogram monitoring. We also make our high-quality
annotated dataset of 97 ICU continuous electroencephalogram recordings public for
others to validate and improve upon our methods.
