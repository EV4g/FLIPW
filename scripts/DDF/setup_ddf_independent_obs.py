
#locate .sif file
#locate tier1-config.cfg file
#locate linc_out folder
#   locate linc_out subfolders L* --> one per observation
#   check if it has linc_out or linc_out_uncompressed
#locate catalogue folder

#setup folders per observation
#   each should at the end contain
#   [L-observation]
#       tier1-config.cfg
#       mslist.txt
#       bigmslist.txt
#       linc_out(_uncompressed)/
#           *.ms
#

#optional locate linc_out_uncompressed
#   if not found --> optional DP3 runner before copying [metadata_uncompressor.py]

#generate sbatch file [make_ddf_batch.py]


import os
import glob
import subprocess
import numpy as np
import shutil

try:
    from termcolor import colored
except:
    print("termcolor not found, ignoring color")
    def colored(str, col): return str

decompress = True #enable if LINC compressed the data, but you're using a ddf version that cannot handle that yet.
overwrite = False

#### setup
try:
    singularity_image = glob.glob("flocs*.sif")[0] #"flocs_v6.0.0_znver2_znver2.sif"
    print("Using", colored(singularity_image, "green"))
except:
    print(colored("No .sif file found", "red"))

try:
    config_file = glob.glob("*.cfg")[0] #"tier1-config.cfg"
    print("Using", colored(config_file, "green"))
except:
    print(colored("No .cfg file found", "red"))

if os.path.isdir("../catalogues"):
    print("Using", colored("../catalogues/", "green"))
else:
    print(colored("No catalogue folder found", "red"))

#### check linc-target dir
linc_dirs = glob.glob("linc_out*")
if decompress == True:
    if "linc_out_uncompressed" in linc_dirs:
        linc_dir = "linc_out_uncompressed"
        decompress = False
    elif "linc_out" in linc_dirs:
        linc_dir = "linc_out"
else:
    linc_dir = linc_dirs[0]

print("Using", colored(linc_dir+"/", "green"))
print("Decompress:", decompress)
print("Overwrite:", overwrite)

observations = np.sort([folder.split("/")[-1] for folder in glob.glob(linc_dir + "/*")])
print("Found observations:", observations, "\n")

#### make dirs for each obs
for obs in observations:
    os.makedirs(obs, exist_ok=True)

#### check compression requirements, run DP3
if decompress == True:
    try:
        glob.glob("metadata_uncompressor.py")[0]
        print("Decompression started")
        subprocess.run("python3", "metadata_uncompressor.py")
        print(colored("Decompression done\n", "green"))
    except:
        exit(colored("Decompressor not found", "red"))
else:
    print("Decompression step skipped, not needed\n")

#### move folder to L-observations/
for obs in observations:
    source_dir = f"{linc_dir}/{obs}/results/"
    target_dir = f"{obs}/{linc_dir}/"
    if os.path.exists(target_dir):
        print(colored(f"Target {target_dir} already exists, skip copy", "yellow"))
    else:
        shutil.move(source_dir, target_dir)
        print(f"Copied {source_dir} to {target_dir}")

#### move .cfg to each observation folder
print("\n")
for obs in observations:
    config_dir = f"{obs}/{config_file}"
    if not(os.path.isfile(config_dir)) or overwrite==True:
        shutil.copy(config_file, config_dir)
        print("Copied config file to:", obs+"/")
    else:
        print(colored(f"{obs}/{config_file} already exist, skipping", "yellow"))

#### generate batch file per observation
print("\n")
for obs in observations:
    batch_dir = os.path.join(os.getcwd(), obs)
    if not(os.path.isfile(os.path.join(batch_dir, f"{obs}_DDF_submit.sh"))) or overwrite==True:
        subprocess.run(["python3", "make_ddf_batch.py", "--observation="+obs, "--linc_dir="+linc_dir], check=True)
        print(f"Made batch: [{obs}, {linc_dir}]", colored("done", "green"))
    else:
        print(colored(f"{obs}_DDF_batch.sh already exist, skipping", "yellow"))

#### generate mslist.txt / bigmslist.txt
print("\n")
for obs in observations:
    msdir = os.path.join(os.getcwd(), obs, linc_dir)+"/*.ms"
    if not(os.path.isfile(os.path.join(os.getcwd(), obs, "mslist.txt"))) or overwrite==True:
        subprocess.run(["python3", "make_mslists.py", "--dir="+msdir])
        print("msdir:", f"--dir={msdir}", colored("done", "green"))
    else:
        print(colored("mslist.txt already exist, skipping", "yellow"))

print("\n")
print(colored("All done", "green"))
print("\n")


