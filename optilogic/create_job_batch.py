import argparse
import json
import requests
import pickle

NON_SEARCH_TEST = {
        "batchItems": [
            {"pyModulePath": "/projects/My Models/optimization-ops/src/solve.py", "timeout": 5},
            {"pyModulePath": "/projects/My Models/optimization-ops/src/solve.py"},
            {"pyModulePath": "My Models/optimization-ops/src/solve.py", "commandArgs": "--scenario baseline"},
            ]
    }

SEARCH_TEST = {
        "batchItems": [
            {"pySearchTerm": "src/*python"},
            {"pySearchTerm": "optimization-ops/src", "commandArgs": "-ttt", "timeout": 12},
            {"pySearchTerm": "My Models/optimization-ops/src/"},
            {"pySearchTerm": "optimization-ops/src/", "commandArgs": "--scenario baseline -ttt", "timeout": 25},
            {"pySearchTerm": "optimization-ops/src/", "commandArgs": "--scenario scenario1"},
            ]
    }

def create_job_batch(args):
    if eval(str(args.jobify)):
        if eval(str(args.searchForMatches)):
            url = f'https://api.optilogic.app/v0/{args.workspace}/jobBatch/jobify/searchNRun?'
            data = SEARCH_TESTS
        else:
            url = f'https://api.optilogic.app/v0/{args.workspace}/jobBatch/jobify?'
            data = NON_SEARCH_TEST
    else:
        if eval(str(args.searchForMatches)):
            url = f'https://api.optilogic.app/v0/{args.workspace}/jobBatch/backToBack/searchNRun?'
            data = SEARCH_TESTS
        else:
            url = f'https://api.optilogic.app/v0/{args.workspace}/jobBatch/backToBack?'
            data = NON_SEARCH_TEST
            
        if eval(str(args.verboseOutput)):
            url += f'&verboseOutput=true'
        if hasattr(args, 'timeout') and args.timeout:
            url += f'&timeout={args.timeout}'

    if args.jobTags:
        url += f'&tags={args.jobTags}'
    if args.resourceConfig:
        url += f'&resourceConfig={args.resourceConfig}'
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

    response = requests.request('POST', url, headers=headers, json=data)
    job_object = json.loads(response.text)
    job_key = None
    job_keys = None
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
    parser.add_argument('--resourceConfig', help='Job size to use')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    job_key_s = create_job_batch(args)
    print(job_key_s)