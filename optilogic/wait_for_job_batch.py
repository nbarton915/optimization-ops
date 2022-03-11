import argparse
from dataclasses import dataclass
import pickle

@dataclass()
class JobCompletionArgs(object):
    workspace: str
    jobKey: str
    apiKey: str
    appKey: str
    d: bool

def wait_for_job_batch(args):
    from wait_for_job_completion import wait_for_job_completion, TerminalJobStatus
    job_keys = args.jobKeys
    if job_keys == 'job_keys.pkl':
        with open(job_keys, 'rb') as f:
            job_keys = pickle.load(f)
    all_status = {}
    for j in job_keys:
        job_completion_args = JobCompletionArgs(
            workspace = args.workspace,
            jobKey = j,
            apiKey = args.apiKey,
            appKey = args.appKey,
            d = args.d
            )
        try:
            job_status = wait_for_job_completion(job_completion_args)
        except Exception as e:
            print(f'The following job is not in a terminal status: {j=}\n\n')
            print(e)
        if not TerminalJobStatus.is_valid_terminal_status(job_status):
            print(f'The following job is not in a terminal status: {j=}')
        all_status[j] = job_status
    return all_status


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wait for batch of Optilogic Jobs to Complete')
    parser.add_argument('--workspace', help='Optilogic Workspace Name')
    parser.add_argument('--jobKeys', help='Optilogic Job Key')
    parser.add_argument('--apiKey', help='Optilogic Token')
    parser.add_argument('--appKey', help='Optilogic App Key')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    all_status = wait_for_job_batch(args)
    print(all_status)
