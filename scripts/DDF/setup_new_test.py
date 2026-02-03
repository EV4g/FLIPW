import subprocess
import argparse
import glob
import shutil
import os

parser = argparse.ArgumentParser(description='Setting up new imaging test')
parser.add_argument('--name', type=str, help="Name of new test", required=True)

args = parser.parse_args()

# copy template folder to new location
if not os.path.isdir(args.name):
    print("Copying folder...")
    shutil.copytree("template_folder", args.name)
else:
    print(f"Folder {args.name} already exists, skipping copy")

# should run "setup_new_test.py --name=..."
linc_dir = os.path.join(args.name, "linc_out_uncompressed/*")
observation = glob.glob(linc_dir)[0].split("/")[-1].split("_")[0]

subprocess.run(["python3", "make_gal_ddf_batch.py",
f"--workdir={args.name}",
f"--linc_dir={linc_dir}",
f"--output_name={args.name}",
f"--mask=test_mask.fits"])

# update big_mslist.txt
# update batch_SSD2.sh
