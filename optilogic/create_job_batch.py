import argparse
import json
import requests

def create_job_batch(args):
    url = f'https://api.optilogic.app/v0/{args.workspace}/job/batch?'
    if hasattr(args, 'searchForMatches'):
        url += f'&searchForMatches={args.searchForMatches}'
    if hasattr(args, 'jobify'):
        url += f'&jobify={args.jobify}'
    if hasattr(args, 'timeout') and args.timeout:
        url += f'&timeout={args.timeout}'
    if args.jobTags:
        url += f'&tags={args.jobTags}'
    if args.d:
        url = url.replace('api.', 'dev.api.')

    headers = {
        'X-API-KEY': f'{args.apiKey}'
        }

    data = {
        "batchList": [
            ["optimization-ops/src/"],
            ["optimization-ops/src"],
            ["My Models/optimization-ops/src/"],
            ["optimization-ops/src/", "--scenario baseline"],
            ["optimization-ops/src/", "--scenario scenario1"],
            ]
    }

    response = requests.request('POST', url, headers=headers, data=data)
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
    parser.add_argument('--searchForMatches', action='store_true', help='search path for matches')
    parser.add_argument('--jobify', action='store_true', help='create a unique job for each module')
    parser.add_argument('--jobTags', help='Tags to add to job')
    parser.add_argument('--timeout', help='Max time for job to run')
    parser.add_argument('-d', action='store_true')

    args = parser.parse_args()
    job_key = create_job_batch(args)
    print(job_key)