import argparse
from dataclasses import dataclass
from multiprocessing.connection import wait

from blessings import Terminal

dataclass
class JobCompletionArgs(object):
    workspace: str
    jobKey: str
    apiKey: str
    d: bool

def wait_for_job_batch(args):
    from wait_for_job_completion import wait_for_job_completion, TerminalJobStatus
    job_keys = args.jobKeys
    all_status = {}
    for j in job_keys:
        job_completion_args = JobCompletionArgs(
            workspace = args.workspace,
            jobKey = j,
            apiKey = args.apiKey,
            d = args.d
            )
        job_status = wait_for_job_completion(job_completion_args)
        if not TerminalJobStatus.is_valid_terminal_status(job_status):
            print(f'The following job is not in a terminal status: {job_status=}')
        all_status[job_keys] = job_status
    return all_status


if __name__ == '__main__.py':
    parser = argparse.ArgumentParser(description='Wait for Optilogic Job to Complete')
    parser.add_argument('--workspace', help='Optilogic Workspace Name')
    parser.add_argument('--jobKeys', help='Optilogic Job Key')
    parser.add_argument('--apiKey', help='Optilogic Token')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    all_status = wait_for_job_batch(args)
    print(all_status)
