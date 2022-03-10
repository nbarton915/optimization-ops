import argparse
import json
import requests

def create_job_batch(args):
    url = f'https://api.optilogic.app/v0/{args.workspace}/job/batch?'
    if args.searchForMatches:
        url += f'&searchForMatches={args.searchForMatches}'
    if args.jobify:
        url += f'&jobify={args.jobify}'
    if hasattr(args, 'timeout') and args.timeout:
        url += f'&timeout={args.timeout}'
    if args.verboseOutput:
        url += f'&verboseOutput={args.verboseOutput}'
    if args.jobTags:
        url += f'&tags={args.jobTags}'
    if args.d:
        url = url.replace('api.', 'dev.api.')

    if hasattr(args, 'appKey') and args.appKey:
        headers = {
        'X-APP-KEY': f'{args.appKey}',
        'content-type': 'application/json'
        }
    else:
        headers = {
            'X-API-KEY': f'{args.apiKey}',
            'content-type': 'application/json'
            }

    data = {
        "batchItems": [
            ["src/*python"],
            ["optimization-ops/src"],
            ["My Models/optimization-ops/src/"],
            ["My Models/optimization-ops/src/solve.py"],
            ["My Models/optimization-ops/src/solve.py", "--scenario baseline"],
            ["optimization-ops/src/", "--scenario baseline"],
            ["optimization-ops/src/", "--scenario scenario1"],
            ]
    }

    response = requests.request('POST', url, headers=headers, json=data)
    job_object = json.loads(response.text)
    try:
        job_key = job_object['jobKey']
        return job_key
    except Exception as e:
        print(f'There was an error with getting the jobKey\n\nResponse: {job_object}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new Optilogic Job')
    parser.add_argument('--workspace', help='Optilogic Workspace Name')
    parser.add_argument('--apiKey', help='Optilogic Token ')
    parser.add_argument('--appKey', help='Optilogic App Key ')
    parser.add_argument('--searchForMatches', help='search path for matches')
    parser.add_argument('--jobify', help='create a unique job for each module')
    parser.add_argument('--verboseOutput', help='controls if job log output is verbose')
    parser.add_argument('--jobTags', help='Tags to add to job')
    parser.add_argument('--timeout', help='Max time for job to run')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    job_key = create_job_batch(args)
    print(job_key)