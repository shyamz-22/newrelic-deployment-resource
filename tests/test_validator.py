import unittest

from assets import out


class ValidatorTest(unittest.TestCase):

    def test_returns_not_ok_when_source_is_none(self):
        source_values = None
        params_values = None

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual('Configuration for assets cannot be empty', result.error_message)

    def test_returns_not_ok_when_source_is_empty(self):
        source_values = {}
        params_values = None

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual('Configuration for assets cannot be empty', result.error_message)

    def test_returns_not_ok_when_mandatory_source_param_is_missing(self):
        source_values = {'not_mandatory': True}
        params_values = None

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual(f'Missing mandatory source parameters:\n {source_values}', result.error_message)

    def test_returns_not_ok_when_params_is_none(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = None

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual('Params for assets cannot be empty in put step', result.error_message)

    def test_returns_not_ok_when_params_is_empty(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = {}

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual('Params for assets cannot be empty in put step', result.error_message)

    def test_returns_not_ok_when_mandatory_param_is_missing(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = {'app_id': '125674'}

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual(f'Missing mandatory parameters in put step:\n {params_values}', result.error_message)

    def test_returns_not_ok_when_one_of_mandatory_param_is_missing(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = {'git_src_directory': '/Users/project'}

        result = out.validate(source_values, params_values)

        self.assertFalse(result.ok)
        self.assertEqual(f'Please provide one of the parameters in put step:\n {out.either_or_params}', result.error_message)

    def test_returns_ok_when_one_of_mandatory_param_is_present_1(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = {'git_src_directory': '/Users/project', 'app_id': '123455'}

        result = out.validate(source_values, params_values)

        self.assertTrue(result.ok)
        self.assertIsNone(result.error_message)

    def test_returns_ok_when_one_of_mandatory_param_is_present_2(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = {'git_src_directory': '/Users/project', 'api_url': 'https://eu.newrelic.com'}

        result = out.validate(source_values, params_values)

        self.assertTrue(result.ok)
        self.assertIsNone(result.error_message)

    def test_returns_ok_when_all_params_are_present(self):
        source_values = {'api_key': 'a_key', 'user': 'commiter@dilab.com'}
        params_values = {'git_src_directory': '/Users/project', 'api_url': 'https://eu.newrelic.com', 'app_id': '123455'}

        result = out.validate(source_values, params_values)

        self.assertTrue(result.ok)
        self.assertIsNone(result.error_message)
