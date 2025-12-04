

import os
import glob
import subprocess
import argparse

try:
    from termcolor import colored
except:
    print("termcolor not found, ignoring color")
    def colored(str, col): return str

# ensure observation ID is passed
parser = argparse/ArgumentParser(description='Setting up rapthor parset')
parser.add_argument('--observation', type=str, help='observation-ID')
args = parser.parse_args()

# see if defaults.parset exists
# if not, download it from the git
if os.path.isfile("defaults.parset"):
    print(colored("defaults.parset found", "green"))
else:
    print(colored(("defaults.parset not found, attempting download", "yellow"))
    subprocess.run(["wget", "https://git.astron.nl/RD/rapthor/-/raw/master/rapthor/settings/defaults.parset"], check=True)
    print(colored("defaults.parset downloaded", "green"))

# then replace some of the lines in there, as opposed to writing it in this function