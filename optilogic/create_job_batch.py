import argparse
import json
import requests
import pickle

def create_job_batch(args):
    url = f'https://api.optilogic.app/v0/{args.workspace}/job/batch?'
    if eval(str(args.searchForMatches)):
        url += f'&searchForMatches=true'
    if eval(str(args.jobify)):
        url += f'&jobify=true'
    if hasattr(args, 'timeout') and args.timeout:
        url += f'&timeout={args.timeout}'
    if eval(str(args.verboseOutput)):
        url += f'&verboseOutput=true'
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
    if not eval(str(args.jobify)):
        try:
            job_key = job_object['jobKey']
            return job_key
        except Exception as e:
            print(f'There was an error with getting the jobKey\n\nResponse: {job_object}')
    else:
        try:
            job_keys = job_object['jobKeys']
        except Exception as e:
            print(f'There was an error with getting the jobKeys\n\nResponse: {job_object}')
        with open('job_keys.pkl', 'wb') as f:
                pickle.dump(job_keys, f)
        return 'job_keys.pkl'

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
    job_key_s = create_job_batch(args)
    print(job_key_s)