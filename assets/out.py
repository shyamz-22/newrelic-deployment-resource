#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from sys import stdin, argv
from typing import Optional

import requests

mandatory_source_params = {'api_key', 'user'}
mandatory_params = {'git_src_directory'}
either_or_params = {'app_id', 'api_url'}


@dataclass
class ValidationResult:
    ok: bool
    error_message: Optional[str]


def validate(source_values: Optional[dict], params_values: Optional[dict]) -> ValidationResult:
    if not source_values:
        return ValidationResult(ok=False, error_message='Configuration for assets cannot be empty')

    if not all(k in source_values for k in mandatory_source_params):
        return ValidationResult(ok=False, error_message=f'Missing mandatory source parameters:\n {source_values}')

    if not params_values:
        return ValidationResult(ok=False, error_message='Params for assets cannot be empty in put step')

    if not all(k in params_values for k in mandatory_params):
        return ValidationResult(ok=False, error_message=f'Missing mandatory parameters in put step:\n {params_values}')

    if not any(k in params_values for k in either_or_params):
        return ValidationResult(ok=False, error_message=f'Please provide one of the parameters in put step:\n {either_or_params}')

    return ValidationResult(ok=True, error_message=None)


def get_resource_output(metadata):
    if metadata and 'deployment' in metadata:
        version_ref = str(metadata['deployment'].get('id'))
    else:
        version_ref = 'None'

    return {
        'version': {'ref': version_ref},
        'metadata': [metadata] if metadata else []
    }


if __name__ == '__main__':
    try:
        path_to_build = argv[1]
        request = json.loads(stdin.read())
        source = request.get('source', None)
        params = request.get('params', None)

        validation_result = validate(source, params)

        if not validation_result.ok:
            sys.stderr.write(validation_result.error_message)
            exit(1)

        api_key = source['api_key']
        user = source['user']
        git_src_directory = params['git_src_directory']

        app_id = params.get('app_id')
        api_url = params.get('api_url')

        cwd = os.getcwd()
        os.chdir(git_src_directory)

        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('UTF-8').strip()
        description = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode('UTF-8').strip()

        os.chdir(cwd)

        if api_url is not None:
            url = api_url
        else:
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

        output = get_resource_output(metadata=response.json())
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f'unexpected error occurred, {e}')
        exit(1)
