#!/usr/bin/env python3
"""Unit tests the <client> module."""
import unittest
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from parameterized import parameterized, param, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from utils import access_nested_map


ORG_PAYLOAD = TEST_PAYLOAD[0][0]
REPOS_PAYLOAD = TEST_PAYLOAD[0][1]
EXPECTED_REPOS = [repo['name'] for repo in REPOS_PAYLOAD]
APACHE2_REPOS = list()
for repo in REPOS_PAYLOAD:
    try:
        if access_nested_map(repo, ['license', 'key']) == 'apache-2.0':
            APACHE2_REPOS.append(repo)
    except KeyError:
        continue


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests the client.GithubOrgClient class."""
    REPOS = [repo for repo in TEST_PAYLOAD[0][1] if repo.get('license', None)]

    @parameterized.expand([
        ('google', {'google_response': {'item': ['other', {}]}}),
        ('abc', {'abc_response': {'item': ['other', {}]}})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, exp_payload, mock_get_json):
        """Test that .org returns expected data from get_json()."""
        mock_get_json.return_value = exp_payload

        client = GithubOrgClient(org_name)
        result = client.org
        client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
            )
        self.assertDictEqual(result, exp_payload)

    @parameterized.expand([
        ('google', {'repos_url': {'item': ['other', {}]}}),
        ('abc', {'repos_url': {'item': ['other', {}]}})
    ])
    @patch('client.get_json')
    def test_public_repos_url(self, org_name, exp_payload, mock_get_json):
        """Tests that the result of _public_repos_url is the expected
        one based on the mocked payload.
        """
        mock_get_json.return_value = exp_payload
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = exp_payload
        client = GithubOrgClient(org_name)

        self.assertDictEqual(client._public_repos_url,
                             exp_payload.get('repos_url'))

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Unit tests GithubOrgClient.public_repos using a mock payload."""
        exp_repos = [repo['name'] for repo in self.REPOS]
        mock_get_json.return_value = self.REPOS
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_pub_repos_url:
            mock_pub_repos_url.return_value = \
                    "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient('google')
            result = client.public_repos()

            self.assertEqual(result, exp_repos)

            mock_get_json.assert_called_once()
            mock_pub_repos_url.assert_called_once()

    @parameterized.expand([
        param(repo, access_nested_map(repo, ['license', 'key']),
              bool(repo.get('license').get('key', None)))
        for repo in REPOS
    ])
    @patch('client.get_json')
    def test_has_license(self, load, license_key,
                         expected_output, mock_get_json):
        """
        Tests the static method `has_license` for accurate
        license detection.
        """
        mock_get_json.return_value = self.REPOS
        client = GithubOrgClient('google')
        result = client.has_license(load, license_key)

        self.assertEqual(result, expected_output)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'),
                     [(ORG_PAYLOAD, REPOS_PAYLOAD,
                       EXPECTED_REPOS, APACHE2_REPOS)
                      ])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos()"""
    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set side_effect for
        different URLs.
        """
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Returns the appropriate mock response for each URL."""
            mock_response = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repos
        (all licenses).
        """
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)


if __name__ == "__main__":
    unittest.main()
