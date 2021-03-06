import argparse
import json
import requests

parser = argparse.ArgumentParser(description='Get a new Optilogic Token.')
parser.add_argument('--username', help='Optilogic Username')
parser.add_argument('--password', help='Optilogic Password')
parser.add_argument('-d', action='store_true')

args = parser.parse_args()

url = 'https://api.optilogic.app/v0/refreshApiKey'
if args.d:
	url = url.replace('api.', 'dev.api.')
headers = {
	'X-USER-ID': f'{args.username}',
	'X-USER-PASSWORD': f'{args.password}'
	}

response = requests.request('POST', url, headers=headers)
api_key = json.loads(response.text)['apiKey']
print(api_key)
