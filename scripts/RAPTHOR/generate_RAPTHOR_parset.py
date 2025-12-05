import os
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
parser.add_argument('--observation', type=str, help='observation-ID')
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
if os.path.isdir(os.path.join("linc_out_uncompressed", observation)):
    data_path = os.path.abspath(os.path.join("linc_out_uncompressed", observation))
    print(colored("Found linc_out_uncompressed", "green"), "at", data_path)
elif os.path.isdir(os.path.join("linc_out", observation)):
    data_path = os.path.abspath(os.path.join("linc_out", observation))
    print(colored("Found linc_out", "green"), "at", data_path)
else:
	print(colored("No linc_out folder found", "yellow"))

# make separate RAPTHOR output directory
rapthor_out_dir = "rapthor_out_"+observation
os.makedirs(rapthor_out_dir, exist_ok=True)

# then replace some of the lines in there, as opposed to writing it in this function
in_file = Path("defaults.parset")
out_file = Path(observation+".parset")

with in_file.open("r", encoding="utf-8") as f: lines = f.readlines()

new_lines = []
for line in lines:
    # maybe easier to hardcode linenumbers, but maybe the file will eventually change
    if line.startswith("dir_working ="): line = "dir_working ="+rapthor_out_dir+"\n"
    if line.startswith("input_ms ="): line = "input_ms ="+data_path+"/*.ms\n"

    # optional line that can be useful if the compression fails
    if line.startswith("compress_selfcal_images ="): line = "compress_selfcal_images = False"

	#if line.startswith(""): line = ""
    #if	line.startswith(""): line = ""

    new_lines.append(line)
