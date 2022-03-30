import argparse
import os

parser = argparse.ArgumentParser(description='Cleanup output directory')
parser.add_argument('--path')

args = parser.parse_args()

output_file = f'{os.getcwd()}/../{args.path}'
print(f'removing {output_file=}')
os.remove(output_file)
print('successfully cleaned up outputs')