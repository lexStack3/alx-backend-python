#!/usr/bin/env python3
"""Unit tests the <client> module."""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests the client.GithubOrgClient class."""

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


if __name__ == "__main__":
    unittest.main()
