#!/usr/bin/env python3

"""
unittest module for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unittest for GithubOrgClient.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org method"""
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_public_repos_url(self, org_name):
        """Test _public_repos_url property"""

        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            url = f"https://api.github.com/orgs/{org_name}/repos"
            payload = {"repos_url": url}
            mock_org.return_value = payload
            client = GithubOrgClient(org_name)
            res = client._public_repos_url
            mock_org.assert_called_once()
            self.assertEqual(res, url)

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_public_repos(self, org_name, mock_get_json):
        """Test public_repos method"""
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            url = f"https://api.github.com/orgs/{org_name}/repos"
            mock_public_repos_url.return_value = url
            expected_payload = [{"name": "repo1"}, {"name": "repo2"}]
            mock_get_json.return_value = expected_payload
            client = GithubOrgClient(org_name)
            repos = client.public_repos()
            mock_get_json.assert_called_once_with(url)
            self.assertEqual(repos, ["repo1", "repo2"])
