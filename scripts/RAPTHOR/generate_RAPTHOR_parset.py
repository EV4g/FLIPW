import numpy as np
import os
import glob
import subprocess
import argparse
from pathlib import Path

try:
    from termcolor import colored
except:
    print("termcolor not found, ignoring color")
    def colored(str, col): return str

# ensure observation ID is passed
parser = argparse.ArgumentParser(description='Setting up rapthor parset')
parser.add_argument('--observation', type=str, help='observation-ID', default="all")
args = parser.parse_args()

observation = args.observation

# see if defaults.parset exists
# if not, download it from the git
if os.path.isfile("defaults.parset"):
    print(colored("defaults.parset found", "green"))
else:
    print(colored("defaults.parset not found, attempting download", "yellow"))
    subprocess.run(["wget", "https://git.astron.nl/RD/rapthor/-/raw/master/rapthor/settings/defaults.parset"], check=True)
    print(colored("defaults.parset downloaded", "green"))

# check for linc_out directories
if os.path.isdir(os.path.join("linc_out_uncompressed")):
	linc_dir = os.path.abspath(os.path.join("linc_out_uncompressed"))
    print(colored("Found linc_out_uncompressed", "green"), "at", linc_dir)
elif os.path.isdir(os.path.join("linc_out")):
	linc_dir = os.path.abspath(os.path.join("linc_out"))
    print(colored("Found linc_out", "green"), "at", linc_dir)
else:
    print(colored("No linc_out folder found", "yellow"))


# check if observation is given, if not, check all files in linc_dir and repeat for all observations present
# put observation in list, such that it is iterable
if observation == 'all':
    observation = np.sort([folder.split("/")[-1] for folder in glob.glob(linc_dir + "/*")])
else:
    observation = [observation]

print(colored(f"Found {len(observation)} observations:", "green"), observation, "\n")

# make separate RAPTHOR output directory
data_paths = []
for obs in observation:
    data_paths.append(os.path.join(linc_dir, obs))

rapthor_out_dirs = []
for obs in observation:
    rapthor_dir = os.path.join(os.getcwd(),"rapthor_out_"+obs)
    os.makedirs(rapthor_dir, exist_ok=True)
    print(colored("Made dir:", "green"), rapthor_dir)
    rapthor_out_dirs.append(rapthor_dir)
print("")

# then replace some of the lines in there, as opposed to writing it in this function
in_file = Path("defaults.parset")

with in_file.open("r", encoding="utf-8") as f: lines = f.readlines()

for i, obs in enumerate(observation):
    out_file = Path(os.path.join(rapthor_out_dirs[i], observation[i]+".parset"))

    new_lines = []
    for line in lines:
        # maybe easier to hardcode linenumbers, but maybe the file will eventually change
        if line.startswith("dir_working ="): line = "dir_working = "+rapthor_out_dirs[i]+"\n"
        if line.startswith("input_ms ="): line = "input_ms = "+data_paths[i]+"/*.ms\n"

        # optional line that can be useful if the compression fails
        if line.startswith("compress_selfcal_images ="): line = "compress_selfcal_images = False"

        #if line.startswith(""): line = ""
        #if line.startswith(""): line = ""

        new_lines.append(line)

    with out_file.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(colored("Written file", "green"), "to", out_file)
