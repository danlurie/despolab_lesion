#!/bin/sh
source /home/despoB/dlurie/.bashrc;
source activate sandbox;
SUB_ID="${SGE_TASK}";
cd /home/despoB/dlurie/Projects/despolab_lesion/code/derivatives/hcp/aal2;
python /home/despoB/dlurie/Projects/despolab_lesion/code/derivatives/hcp/aal2/sge/sge_run.py ${SUB_ID}
END_TIME=$(date);
echo "Timeseries extraction and connectome computation completed successfully at $END_TIME";


