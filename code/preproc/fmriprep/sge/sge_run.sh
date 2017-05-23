#!/bin/sh
source /home/despoB/dlurie/.bashrc;
source activate fmriprep-dev;
SUB_ID="${SGE_TASK}";
cd /home/despoB/dlurie/Projects/despolab_lesion/preproc;
fmriprep \
    --participant_label $SUB_ID \
    --nthreads 4 \
    --ignore slicetiming \
    --output-space MNI152NLin2009cAsym T1w \
    -w /home/despoB/dlurie/Projects/despolab_lesion/preproc/work \
    --no-freesurfer \
    --ants-nthreads 2 \
    /home/despoB/lesion/data/original/bids \
    /home/despoB/dlurie/Projects/despolab_lesion/preproc/out \
    participant;
END_TIME=$(date);
echo "fmriprep run completed successfully at $END_TIME";


