# Transform lesion masks to MNI
for pid in `cat /home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/has_EPI.txt`; do
    echo "Transforming lesion mask to MNI for patient $pid...";
    antsApplyTransforms \
        --default-value 0 \
        --dimensionality 3 \
        --float 1 \
        --input /home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-${pid}/anat/sub-${pid}_t1w_variant-reorient_label-lesion_roi.nii.gz \
        --interpolation NearestNeighbor \
        --output /home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-${pid}/anat/sub-${pid}_t1w_space-MNI152NLin2009cAsym_label-lesion_roi.nii.gz \
        --reference-image /home/despoB/dlurie/Data/reference/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii \
        --transform /home/despoB/dlurie/Projects/despolab_lesion/data/patients/preproc/work/workflow_enumerator/${pid}/t1w_preprocessing/T1_2_MNI_Registration/ants_t1_to_mniComposite.h5;
done

