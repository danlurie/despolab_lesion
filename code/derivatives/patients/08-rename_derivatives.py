import numpy as np
import os

def rename(epi_acq):
    # Load list of subjects with the specified EPI sequence.
    sublist_file = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/has_acq-{0}.txt'.format(epi_acq)
    subject_list = np.loadtxt(sublist_file, dtype='int')
    subject_list = [str(i) for i in subject_list]

    print("Processing {0} patients who were scanned with the {1} sequence...".format(str(len(subject_list)), epi_acq))

    # Set file path templates
    motion24_fpt_old = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_confounds-motion24.csv'
    motion24_fpt_new = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_variant-motion24_confounds.csv'
    ts_fpt_old = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_timeseries_atlas-BNA_motion24.npy'
    ts_fpt_new = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_atlas-BNA_variant-motion24_timeseries.npy'
    corrmat_fpt_old = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_corrmat_atlas-BNA_motion24.npy'
    corrmat_fpt_new = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_atlas-BNA_variant-motion24_corrmat.npy'

    for pid in subject_list:

        motion_old = motion24_fpt_old.format(pid, epi_acq)
        motion_new = motion24_fpt_new.format(pid, epi_acq)
        os.rename(motion_old, motion_new)

        ts_old = ts_fpt_old.format(pid, epi_acq)
        ts_new = ts_fpt_new.format(pid, epi_acq)
        os.rename(ts_old, ts_new)

        corr_old = corrmat_fpt_old.format(pid, epi_acq)
        corr_new = corrmat_fpt_new.format(pid, epi_acq)
        os.rename(corr_old, corr_new)

        print('Renamed derivatives for patient '+pid)
    
for acq in ['128px', '64px']:
    rename(acq)
