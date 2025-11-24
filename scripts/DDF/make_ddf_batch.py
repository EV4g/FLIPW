import os
import glob

import argparse

def write_slurm_script(filename, observation, linc_dir):
    script_content = f"""#!/bin/bash
#SBATCH --job-name=DDF_{observation}
#SBATCH --output=slurm_%j_{observation}.out
#SBATCH -N 1
#SBATCH -c 60
#SBATCH -t 120:00:00

cd /project/lspc/Data/floris/run-ddf/{observation}

singularity exec \\
    -B /project/lspc/Data/floris/run-ddf,/project/lspc/Data/floris/run-ddf/{observation}/{linc_dir}/,/project/lspc/Data/floris/catalogues/ \\
    ../flocs_v6.0.0_znver2_znver2.sif \\
    pipeline.py tier1-config.cfg
"""
    with open(filename, "w") as file:
        file.write(script_content)

parser = argparse.ArgumentParser(description='Setting up the ddf run')
parser.add_argument('--observation', type=str, help='observation-ID for run', default="L2014919")
parser.add_argument("--linc_dir", type=str, help='linc_out or linc_out_uncompressed', default='linc_out')
args = parser.parse_args()

filename = args.observation+"_DDF_submit.sh"
write_slurm_script(os.path.join(args.observation, filename), args.observation, args.linc_dir)
#print(os.path.join(args.observation, filename))
