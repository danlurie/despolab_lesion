for pid in `cat /home/despoB/dlurie/Projects/despolab_lesion/lesion_masks/has_bids_mask.txt`; do
    echo "Reorienting lesion mask for subject  $pid...";
    # Reorient lesion mask and write to derivatives directory.
    python ~/Software/Scripts/nb_reorient.py \
        /home/despoB/lesion/data/original/bids/sub-${pid}/anat/sub-${pid}_t1w_label-lesion_roi.nii.gz \
        /home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-${pid}/anat/sub-${pid}_t1w_variant-reorient_label-lesion_roi.nii.gz;
done

