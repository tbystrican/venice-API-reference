"""
test_add_code_samples.py - Unit tests for the add_code_samples script.

This module verifies that the `add_code_samples` script correctly adds
boilerplate code samples to an OpenAPI specification file without modifying
operations that already have them.
"""

import unittest
import yaml
import os
from add_code_samples import add_code_samples

class TestAddCodeSamples(unittest.TestCase):
    """Test suite for the add_code_samples script."""

    def setUp(self):
        """Set up a temporary OpenAPI spec file for testing."""
        self.test_spec_path = "test_spec.yaml"
        self.spec_content = {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0.0"},
            "paths": {
                "/test1": {
                    "get": {
                        "summary": "Endpoint without code samples",
                        "responses": {"200": {"description": "OK"}}
                    }
                },
                "/test2": {
                    "post": {
                        "summary": "Endpoint with existing code samples",
                        "x-codeSamples": [{"lang": "cURL", "source": "curl ..."}],
                        "responses": {"200": {"description": "OK"}}
                    }
                }
            }
        }
        with open(self.test_spec_path, 'w') as f:
            yaml.dump(self.spec_content, f)

    def tearDown(self):
        """Clean up the temporary spec file after tests."""
        os.remove(self.test_spec_path)

    def test_add_code_samples(self):
        """
        Verify that code samples are added correctly.
        
        This test checks that:
        1. Code samples are added to operations that are missing them.
        2. Existing code samples are not overwritten or modified.
        """
        add_code_samples(self.test_spec_path)
        with open(self.test_spec_path, 'r') as f:
            updated_spec = yaml.safe_load(f)

        # Check that samples were added to the first endpoint
        self.assertIn("x-codeSamples", updated_spec["paths"]["/test1"]["get"])
        self.assertEqual(len(updated_spec["paths"]["/test1"]["get"]["x-codeSamples"]), 3)

        # Check that existing samples were not modified
        self.assertEqual(len(updated_spec["paths"]["/test2"]["post"]["x-codeSamples"]), 1)
        self.assertEqual(updated_spec["paths"]["/test2"]["post"]["x-codeSamples"][0]["source"], "curl ...")

if __name__ == "__main__":
    unittest.main()
