from glob import glob
import os

# Get a list of patients with the 128px sequence.
tsv_128 = sorted(glob('/home/despoB/dlurie/Projects/despolab_lesion/preproc/out/fmriprep/sub-*/func/sub-*_task-rest_acq-128px_run-01_bold_confounds.tsv'))
has_128 = [os.path.basename(i)[4:7] for i in tsv_128]

with open('/home/despoB/dlurie/Projects/despolab_lesion/code/derivatives/has_acq-128px.txt', 'w') as outf:
    for pid in has_128:
        outf.write(pid)
        outf.write('\n')

# Get a list of patients with the 64px sequence.
tsv_64 = sorted(glob('/home/despoB/dlurie/Projects/despolab_lesion/preproc/out/fmriprep/sub-*/func/sub-*_task-rest_acq-64px_run-01_bold_confounds.tsv'))
has_64 = [os.path.basename(i)[4:7] for i in tsv_64]

with open('/home/despoB/dlurie/Projects/despolab_lesion/code/derivatives/has_acq-64px.txt', 'w') as outf:
    for pid in has_64:
        outf.write(pid)
        outf.write('\n')

# Write a list of all patients with either sequence.
has_epi = sorted(has_64 + has_128)

with open('/home/despoB/dlurie/Projects/despolab_lesion/code/derivatives/has_EPI.txt', 'w') as outf:
    for pid in has_epi:
        outf.write(pid)
        outf.write('\n')
