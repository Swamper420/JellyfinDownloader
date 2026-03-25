import unittest

from jellydown.api import build_download_url


class ApiTests(unittest.TestCase):
    def test_build_download_url_adds_api_key(self):
        self.assertEqual(
            build_download_url("http://example.com/", "secret", "item123"),
            "http://example.com/Items/item123/Download?api_key=secret",
        )


if __name__ == "__main__":
    unittest.main()
