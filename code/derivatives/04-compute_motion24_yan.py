import os
import numpy as np
import pandas as pd

def compute_mopars(epi_acq):
    # Load list of subjects with the specified EPI sequence.
    sublist_file = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/has_acq-{0}.txt'.format(epi_acq)
    subject_list = np.loadtxt(sublist_file, dtype='int')
    subject_list = [str(i) for i in subject_list]

    print("Processing {0} patients who were scanned with the {1} sequence...".format(str(len(subject_list)), epi_acq))

    # Set file path templates
    confounds_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/preproc/out/fmriprep/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_confounds.tsv'
    motion24_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_confounds-motion24.csv'

    for pid in subject_list:
        print("...computing 24 motion parameters for patient {0}...".format(pid))
        
        os.mkdir('/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/func'.format(pid))
        bold_confounds = confounds_fpt.format(pid,epi_acq)

        all_confounds = pd.read_csv(bold_confounds, sep='\t')

        nuisance_vars = all_confounds[['aCompCor0', 'aCompCor1', 'aCompCor2', 'aCompCor3', 'aCompCor4', 'aCompCor5',
                                      'X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']].copy()

        # Create squared versions of each motion parameter at Tt
        for mopar in ['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']:
            sq_col_name = mopar+'sq'
            sq_col_data = np.square(nuisance_vars[mopar])
            nuisance_vars.loc[:,sq_col_name] = sq_col_data

        # Include parameter set from volume t-1
        zpad = pd.Series([0])
        for mopar in nuisance_vars.columns[-12:]:
            pv_col_name = mopar+'_t-1'
            pv_col_data = zpad.append(nuisance_vars[mopar], ignore_index=True)[:-1]
            nuisance_vars.loc[:,pv_col_name] = pv_col_data

        nuisance_vars.to_csv(motion24_fpt.format(pid,epi_acq), sep=',', index=False)

for acq in ['128px', '64px']:
    compute_mopars(acq)

