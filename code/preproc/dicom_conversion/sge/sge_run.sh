#!/bin/sh
source /home/despoB/dlurie/.bashrc;
source activate legacy;
SUB_ID="${SGE_TASK}";
cd /home/despoB/dlurie/Projects/despolab_lesion/code/dicom_conversion;
heudiconv \
    -d /home/despoB/lesion/data/original/dicom/%s/*/*.dcm \
    -s $SUB_ID \
    -f /home/despoB/dlurie/Software/heudiconv/heuristics/uc_bids.py \
    -c dcm2niix \
    -o /home/despoB/lesion/data/original/bids \
    --bids \
    --minmeta; 
END_TIME=$(date);
echo "DICOM file conversion completed successfully at $END_TIME";


