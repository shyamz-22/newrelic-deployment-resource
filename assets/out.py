#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from sys import stdin, argv

import requests

mandatory_source_params = {'api_key', 'user'}
mandatory_params = {'git_src_directory', 'app_id'}


def validate_input(input_val: dict, mandatory_keys: set) -> bool:
    return all(k in input_val for k in mandatory_keys)


def validate(source_values: dict, params_values: dict):
    if not source_values:
        sys.stderr.write('Configuration for resource cannot be empty')
        exit(1)

    if not validate_input(source_values, mandatory_source_params):
        sys.stderr.write(f'Missing mandatory source parameters:\n {source_values}')
        exit(1)

    if not params_values:
        sys.stderr.write('Params for resource cannot be empty in put step')
        exit(1)

    if not validate_input(params_values, mandatory_params):
        sys.stderr.write(f'Missing mandatory parameters in put step:\n {params_values}')
        exit(1)


try:
    path_to_build = argv[1]
    request = json.loads(stdin.read())
    source = request.get('source', None)
    params = request.get('params', None)

    validate(source, params)

    api_key = source['api_key']
    user = source['user']
    app_id = params['app_id']
    git_src_directory = params['git_src_directory']

    cwd = os.getcwd()
    os.chdir(git_src_directory)

    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('UTF-8').strip()
    description = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode('UTF-8').strip()

    os.chdir(cwd)

    url = f'https://api.newrelic.com/v2/applications/{app_id}/deployments.json'
    sys.stderr.write(f'✅ adding deployment marker to {url}\n')

    data = {
        'deployment': {
            'revision': revision,
            'description': description,
            'user': user
        }
    }

    response = requests.post(url, json=data, headers={'X-Api-Key': api_key})
    response.raise_for_status()

    sys.stderr.write(f'✅ Deployment marker added successfully: {response.status_code}\n')
    metadata = response.json()
    output = {
        'version': {'ref': metadata['deployment'].get('id', None)},
        'metadata': [metadata]
    }

    print(json.dumps(output))

except Exception as e:
    sys.stderr.write(f'unexpected error occurred, {e}')
    exit(1)
