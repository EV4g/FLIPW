export SINGULARITYENV_RCLONE_CONFIG_DIR=/project/lspc/Data/floris/cygnus/"$1"/
singularity exec ../../run-ddf/flocs_v6.0.0_znver2_znver2.sif python3 prepare_fields.py --pointing="$1"
