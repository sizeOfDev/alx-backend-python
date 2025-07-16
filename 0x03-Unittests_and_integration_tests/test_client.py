#!/usr/bin/env python3

"""
unittest module for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
        """
        Test public_repos method
        """
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            url = f"https://api.github.com/orgs/{org_name}/repos"
            mock_public_repos_url.return_value = url
            expected_payload = [
                {"name": "repo1"},
                {"name": "repo2"}
                ]
            mock_get_json.return_value = expected_payload
            client = GithubOrgClient(org_name)
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with(url)
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "MIT"}}, "MIT", True),
        ({"license": {"key": "GPL"}}, "MIT", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload",
     "expected_repos", "apache2_repos"), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integeration test for GithubOrgClient class
    """

    @classmethod
    def setUpClass(cls):
        """Setup class"""
        def sideEffect(url):
            if url == cls.org_payload.get("repos_url"):
                mock_response = Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response

            mock_response = Mock()
            mock_response.json.return_value = cls.org_payload
            return mock_response

        cls.get_patcher = patch("requests.get", side_effect=sideEffect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test the public_repos method
        """

        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)
