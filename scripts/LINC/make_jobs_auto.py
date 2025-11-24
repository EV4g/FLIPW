import subprocess
import os
#from glob import glob

#ID, calID
observation = [
[691508, 691504],
[693765, 693761],
[2020624, 2020619],
[2020633, 2020630]
]

cal_path = "/project/lspc/Data/floris/run-calibrator"
tar_path = "/project/lspc/Data/floris/run-target"

for (id, cal) in observation:
    #print("L"+str(id), "L"+str(cal))

    #for calibrators
    if os.path.isfile(cal_path+"/submit-scripts/L"+str(cal)+"_caljob.sh"):
        print("L"+str(cal)+"_caljob.sh already exists. Skipping.")
    else:
        subprocess.run(['python3', cal_path+"/make_calibrator_job.py", "--id=L"+str(cal), "--basedir="+cal_path])
        print(cal_path+"/make_calibrator_job.py", "--id=L"+str(cal), "--basedir="+cal_path)
    print("----------------------------------------------------")

    #for targets
    if os.path.isfile(tar_path+"/submit-scripts/L"+str(id)+"_tarjob.sh"):
         print("L"+str(id)+"_tarjob.sh already exists. Skipping.")
    else:
        calsol_path = cal_path+"/outdir/L"+str(cal)+"/cal_solutions.h5"
        subprocess.run(['python3', tar_path+"/make_target_job.py", "--id=L"+str(id), "--basedir="+tar_path, "--calsols="+calsol_path])
        print(tar_path+"/make_target_job.py", "--id=L"+str(id), "--basedir="+tar_path, "--calsols="+calsol_path)
    print("----------------------------------------------------")

