import argparse
import json
import requests
import time

parser = argparse.ArgumentParser(description='Wait for Optilogic Job to Complete')
parser.add_argument('--workspace', help='Optilogic Workspace Name')
parser.add_argument('--jobKey', help='Optilogic Job Key')
parser.add_argument('--apiKey', help='Optilogic Token')
parser.add_argument('-d', action='store_true')

args = parser.parse_args()

url = f'https://api.optilogic.app/v0/{args.workspace}/job/{args.jobKey}?op=status'
if args.d:
    url = url.replace('api.', 'dev.api.')
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
    except Exception as e:
        print(f'There was a problem getting the job status. No longer checking for safety sake.\n\n{job_object}')
        raise
print(job_status)
