import numpy as np
import matlab.engine

# Initialize MATLAB interface
eng = matlab.engine.start_matlab()
eng.addpath('/home/despoB/dlurie/Projects/despolab_lesion/code/analysis/', nargout=0)

# Load list of ROIs to use
aal2_labels = np.loadtxt('/home/despoB/dlurie/Data/reference/AAL/AAL2_MNI_V5.txt', dtype='int16', delimiter='\t', usecols=[2])
aal2_fd04_rois = np.loadtxt('/home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/subsample-fd04_atlas-AAL2_RegionList.txt', dtype='int')
fd04_index = np.in1d(aal2_labels, aal2_fd04_rois)

# Load list of patients to exclude
exclude = np.loadtxt('/home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/subsample-fd04_run-01_ExcludeList.txt', dtype='int')
exclude = [str(i) for i in exclude]

# Loop through EPI sequences
for acq in ['128px','64px']:
    # Load list of subjects with the specified EPI sequence.
    sublist_file = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/has_acq-{0}.txt'.format(acq)
    subject_list = np.loadtxt(sublist_file, dtype='int')
    subject_list = [str(i) for i in subject_list]
    
    # Set file-path templates
    corrmat_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_atlas-AAL2_variant-motion24_corrmat.npy'
    corrmat_z_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_atlas-AAL2_roi-fd04_variant-motion24_corrmatZ.csv'
    out_prefix_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_atlas-AAL2_roi-fd04_variant-motion24_thresh-none_alg-Louvain_gamma-1.0'

    for pid in subject_list:
        if pid not in exclude:
            try:
                print("Processing patient {0}...".format(pid))
                
                # Load the raw correlation matrix and zero the diagonal.
                #print("Loading correlation matrix...")
                corrmat = np.load(corrmat_fpt.format(pid, acq))
                np.fill_diagonal(corrmat, 0)
                
                # Filter the matrix by the list of ROIs
                #print("Filtering by ROI list...")
                corrmat_filtered = corrmat[fd04_index][:,fd04_index]
                corrmat_filtered_z = np.arctanh(corrmat_filtered)
                
                # Z-score the filtered matrix and save it.
                #print("Converting to z-scores...")
                corrmat_z_path = corrmat_z_fpt.format(pid, acq)
                np.savetxt(corrmat_z_path, corrmat_filtered_z)

                # Run graph-theory pipeline
                #print("Running community detection...")
                out_prefix = out_prefix_fpt.format(pid, acq)
                res = eng.run_louvain_z(1.0, corrmat_z_path, out_prefix, nargout=0)
            except:
                print("Error encountered for patient {0}".format(pid))
                pass
