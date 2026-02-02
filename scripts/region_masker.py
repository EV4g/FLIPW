from astropy.io import fits
from astropy.wcs import WCS
from regions import Regions
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

basedir = "/home/floris/Documents/PhD/Galactic plane/P282+00/masks/"

file = os.path.join(basedir, "base_mask.fits")
region_file = os.path.join(basedir, "bright_region.reg")

output_file = file.replace(file.split("/")[-1], "test_mask.fits")
save = True
overwrite = False

if output_file != file and os.path.exists(output_file):
    print(f"Warning: {output_file.split("/")[-1]} exists. Set overwrite=True to replace it.")
    sys.exit()

hdul = fits.open(file, mode="update")
data = hdul[0].data
header = hdul[0].header
wcs = WCS(header).celestial 

regs = Regions.read(region_file, format="ds9")
data_slice = data[0, 0] # [coord, coord, stokes, freq] --> [coord, coord]
ny, nx = data_slice.shape

full_mask = np.zeros((ny, nx), dtype=bool) #mask

for r in regs:
    pix_reg = r.to_pixel(wcs)  # SkyRegion --> PixelRegion
    mask_image = pix_reg.to_mask().to_image((ny, nx))
    full_mask |= mask_image.astype(bool)

# apply mask to data
data_slice[full_mask] = 1
data[0, 0] = data_slice

if save:
    if overwrite:
        hdul[0].data = data
        hdul.writeto(file, overwrite=True)
        print(f"Saved to original: {file}")
    else:
        hdul[0].data = data
        hdul.writeto(output_file, overwrite=True)
        print(f"Saved to new file: {output_file}")

hdul.close()

#debug plot
plt.imshow(data[0, 0, ::5, ::5], origin='lower')
plt.show()
