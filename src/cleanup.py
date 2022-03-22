import os

output_file = f'{os.getcwd()}/outputs/flow_table.csv'
print(f'removing {output_file=}')
os.remove()
print('successfully cleaned up outputs')