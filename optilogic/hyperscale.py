from dataclasses import dataclass
import argparse
import os
from create_job import create_job

@dataclass
class JobArgs(object):
    workspace: str
    directoryPath: str
    filename: str
    apiKey: str
    commandArgs: str
    jobTags: str

def complete_job_args(args, dir):
    job_args = JobArgs(
        workspace=args.workspace,
        directoryPath=args.directoryPath,
        filename=args.filename,
        apiKey=args.apiKey,
        commandArgs=f'--scenario={dir}',
        jobTags='hyperscale,{dir}'
    )
    return job_args

def hyperscale(args):
    scenario_directories = os.listdir(f'{os.getcwd()}/data')

    all_job_args = list(map(lambda x: complete_job_args(args, x), scenario_directories))
    for a in all_job_args:
        print(a)

    job_keys = list(map(create_job, all_job_args))
    return job_keys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new Optilogic Job')
    parser.add_argument('--workspace', help='Optilogic Workspace Name')
    parser.add_argument('--directoryPath', help='Optilogic Path to Directory')
    parser.add_argument('--filename', help='Optilogic Filename')
    parser.add_argument('--apiKey', help='Optilogic Token ')

    args = parser.parse_args()
    job_keys = hyperscale(args)
    for j in job_keys:
        print(j)