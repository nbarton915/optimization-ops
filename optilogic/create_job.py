import argparse
import json
import requests

def create_job(args):
    url = f'https://api.optilogic.app/v0/{args.workspace}/job?directoryPath={args.directoryPath}&filename={args.filename}'
    if args.commandArgs:
        url += f'&commandArgs={args.commandArgs}'
    if args.jobTags:
        url += f'&tags={args.jobTags}'
    if hasattr(args, 'timeout') and args.timeout:
        url += f'&timout={args.timeout}'
    if args.d:
        url = url.replace('api.', 'dev.api.')
    headers = {
        'X-API-KEY': f'{args.apiKey}'
        }

    response = requests.request('POST', url, headers=headers)
    job_object = json.loads(response.text)
    try:
        job_key = job_object['jobKey']
        return job_key
    except Exception as e:
        print(f'There was an error with getting the jobKey\n\nResponse: {job_object}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new Optilogic Job')
    parser.add_argument('--workspace', help='Optilogic Workspace Name')
    parser.add_argument('--directoryPath', help='Optilogic Path to Directory')
    parser.add_argument('--filename', help='Optilogic Filename')
    parser.add_argument('--apiKey', help='Optilogic Token ')
    parser.add_argument('--commandArgs', help='Arg to pass to python')
    parser.add_argument('--jobTags', help='Tags to add to job')
    parser.add_argument('--timeout', help='Max time for job to run')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    job_key = create_job(args)
    print(job_key)