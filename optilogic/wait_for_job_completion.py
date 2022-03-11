import argparse
import json
import requests
import time

class TerminalJobStatus:
    DONE: str = 'done'
    ERROR: str = 'error'
    CANCELLED: str = 'cancelled'
    STOPPED: str = 'stopped'
    VALID_TERMINAL_STATUS = [DONE, ERROR, CANCELLED, STOPPED]
    
    def is_valid_terminal_status(status) -> bool:
        if (status in TerminalJobStatus.VALID_TERMINAL_STATUS):
            return True
        return False

def wait_for_job_completion(args):

    url = f'https://api.optilogic.app/v0/{args.workspace}/job/{args.jobKey}?op=status'
    if args.d:
        url = url.replace('api.', 'dev.api.')

    if args.appKey:
        headers = {
            'X-APP-KEY': f'{args.appKey}'
            }
    else:
        headers = {
            'X-API-KEY': f'{args.apiKey}'
            }

    complete_status_list = ['done', 'error', 'cancelled', 'stopped']
    job_status = None
    while job_status not in complete_status_list:
        time.sleep(10)
        try:
            response = requests.request('GET', url, headers=headers)
            job_object = json.loads(response.text)
            job_status = job_object['status']
        except KeyError as e:
            raise type(e)(f'There was a problem getting the job status. No longer checking for safety sake.\n\n{job_object=}')
        except Exception as e:
            raise type(e)(f'There was a problem getting the job status. No longer checking for safety sake.\n\n{job_object=}')
    return job_status

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wait for Optilogic Job to Complete')
    parser.add_argument('--workspace', help='Optilogic Workspace Name')
    parser.add_argument('--jobKey', help='Optilogic Job Key')
    parser.add_argument('--apiKey', help='Optilogic Token')
    parser.add_argument('--appKey', help='Optilogic App Key')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    job_status = wait_for_job_completion(args)
    print(job_status)