#!/usr/bin/env python3
from casacore.tables import table, makecoldesc
import numpy as np

try:
    from termcolor import colored
except:
    print("termcolor not found, ignoring color")
    def colored(str, col): return str

overwrite = True #overwrite CORRECTED_DATA column regardless of existence
print(colored(f"Overwrite is set to {overwrite}", "yellow"))

with open('big-mslist.txt') as f:
    mslist = [line.strip() for line in f]

for i, ms in enumerate(mslist):
    print(f"Processing {ms}...")
    t = table(ms, readonly=False)

    # Check if column exists
    if 'CORRECTED_DATA' in t.colnames():
        if overwrite:
            print(colored(f"    Removing existing CORRECTED_DATA column", "yellow"))
            t.removecols('CORRECTED_DATA')
            t.flush()
        else:
            print(colored(f"    Column CORRECTED_DATA doesn't exist yet", "yellow"))


    data_desc = t.getcoldesc('DATA')                    # Get full column description / shape
    coldesc = makecoldesc('CORRECTED_DATA', data_desc)  # Explicitly copy the column descriptor

    # Use DATA's data manager info
    dminfo = t.getdminfo('DATA')
    dminfo['NAME'] = 'CORRECTED_DATA'

    t.addcols(coldesc, dminfo)
    print(colored(f"    Created CORRECTED_DATA column", "green"))

    # Perform subtraction row by row to reduce memory
    nrows = t.nrows()
    chunksize = 10000

    for start in range(0, nrows, chunksize):
        end = min(start + chunksize, nrows)
        data = t.getcol('DATA', startrow=start, nrow=end-start)
        model = t.getcol('MODEL_DATA', startrow=start, nrow=end-start)
        corrected = data - model
        t.putcol('CORRECTED_DATA', corrected, startrow=start, nrow=end-start)

    t.close()

    print(f"  Completed [{i} / {len(mslist)}]")

print(colored("\nAll MSs processed successfully!", "green"))