import os

output_file = f'{os.getcwd()}/outputs/flow_table.csv'
print(f'removing {output_file=}')
os.remove(output_file)
print('successfully cleaned up outputs')