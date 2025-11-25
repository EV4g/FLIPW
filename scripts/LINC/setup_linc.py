import os
import subprocess

ms_dir = "/project/lspc/Data/floris/P282_full/"

#### download LINC files
if not os.path.isdir("LINC"): 
    subprocess.run(["git", "clone", "https://git.astron.nl/RD/LINC.git"], check=True)
else: print("LINC already cloned")

if not os.path.isfile("linc_latest.sif"):
    subprocess.run(["singularity", "pull", "linc_latest.sif", "docker://astronrd/linc"], check=True)
else: print("LINC singularity file already present")

#### make folder structure
folders = ['json-files', 'logs', 'outdir', 'singularity-tmp', 'submit-scripts']
for folder in folders:
    os.makedirs(os.path.join(os.getcwd(), "run-target", folder))
    os.makedirs(os.path.join(os.getcwd(), "run-calibrator", folder))
