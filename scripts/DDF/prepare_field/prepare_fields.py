import argparse
from reprocessing_utils import prepare_field

parser = argparse.ArgumentParser(description='making the ms file list')
parser.add_argument('--pointing',type=str,help='Pointing', required=True)
pointing = parser.parse_args().pointing

print("Pointing: ", pointing)

prepare_field(pointing, './', verbose=True)
