# Reverse normalize Brainnetome atlas and write to derivatives directory.
for pid in `cat /home/despoB/dlurie/Projects/despolab_lesion/lesion_masks/has_bids_mask.txt`; do
    echo "Reverse-normalizing Brainnetome atlas for subject $pid...";
    mkdir -p /home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-${pid}/anat;
    antsApplyTransforms \
        --default-value 0 \
        --dimensionality 3 \
        --float 1 \
        --input /home/despoB/dlurie/Data/reference/Brainnetome/BNA-maxprob-thr25-1mm.nii.gz \
        --interpolation NearestNeighbor \
        --output /home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-${pid}/anat/sub-${pid}_t1w_label-BNA_atlas.nii.gz \
        --reference-image /home/despoB/dlurie/Projects/despolab_lesion/preproc/out/fmriprep/sub-${pid}/anat/sub-${pid}_T1w_preproc.nii.gz \
        --transform /home/despoB/dlurie/Projects/despolab_lesion/preproc/work/workflow_enumerator/${pid}/t1w_preprocessing/T1_2_MNI_Registration/ants_t1_to_mniInverseComposite.h5;
done
