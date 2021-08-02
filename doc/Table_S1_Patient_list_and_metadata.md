### Table S1: Patient list and metadata.
The first 77 patients in the table were in the cross-validation set, and the
final 20 were in the test set.

- Column 1 lists the portal ID number of the records publicly available on ieeg.org.
- Column 2 denotes the annotation file number in the ‘Data’ folder of
our GitHub repository, containing start/stop times of the data we used in this study as well as seizure annotation start/stop times. 
- Column 3 contains a diagnosis code that most directly led to the continuous EEG study being ordered. Abbreviations: 
    * AMS – altered mental status, SZ – witnessed or reported seizure, Anoxic – anoxic brain injury, UC – unspecified coma, ICH – intracranial hemorrhage (including subdural and intracerebral).

- Column 4 denotes patient age at time of EEG recording.
- Column 5 denotes patient sex.
- Column 6 indicates number of total seizures.
- Column 7 contains mean length of seizure. 
- Column 8 shows the total length of data clip used in
seconds. 
- Column 9 denotes the number of total 5-second intervals that the artifact rejection
algorithm marked for removal. 
- Column 10 contains a brief description of the seizures obtained from the clinical EEG report by a neurologist board certified in clinical neurophysiology. 
    * Abbreviations: (N)CSE – (non)-convulsive status epilepticus.
	
Addendum: 
The table in the supplment was converted to a comma-separated file (csv) and with spaces and periods removed from column headers to ease their reference in code.
