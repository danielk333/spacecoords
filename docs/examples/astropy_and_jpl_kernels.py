import argparse
from pathlib import Path
from astropy.time import Time
from spacecoords import celestial

parser = argparse.ArgumentParser()
parser.add_argument("kernel_folder", type=Path)
args = parser.parse_args()

epoch = Time("2025-03-20T09:01:00", format="isot", scale="utc")
state = celestial.astropy_get_body("Earth", epoch, args.kernel_folder)

print(f"Earth state = {state} at {epoch}")
