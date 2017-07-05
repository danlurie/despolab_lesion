# Reverse normalize AAL2 atlas and write to derivatives directory.
for pid in `cat /home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/has_EPI.txt`; do
    echo "Reverse-normalizing AAL2 atlas for patient $pid...";
    mkdir -p /home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-${pid}/anat;
    antsApplyTransforms \
        --default-value 0 \
        --dimensionality 3 \
        --float 1 \
        --input /home/despoB/dlurie/Data/reference/AAL/AAL2_MNI_V5.nii \
        --interpolation NearestNeighbor \
        --output /home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-${pid}/anat/sub-${pid}_t1w_label-AAL2_atlas.nii.gz \
        --reference-image /home/despoB/dlurie/Projects/despolab_lesion/data/patients/preproc/out/fmriprep/sub-${pid}/anat/sub-${pid}_T1w_preproc.nii.gz \
        --transform /home/despoB/dlurie/Projects/despolab_lesion/data/patients/preproc/work/workflow_enumerator/${pid}/t1w_preprocessing/T1_2_MNI_Registration/ants_t1_to_mniInverseComposite.h5;
done
