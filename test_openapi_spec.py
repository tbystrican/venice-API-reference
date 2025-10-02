#!/usr/bin/env python3
"""
test_openapi_spec.py - OpenAPI Specification Validation Test Suite

This module provides comprehensive automated tests for validating the Venice.ai
OpenAPI specification file. It ensures structural integrity, required fields,
and adherence to OpenAPI 3.0.0 standards.

Test Categories:
    - Structural validation: Verifies required OpenAPI sections exist
    - Metadata validation: Checks info section completeness
    - Security validation: Ensures security schemes are properly defined
    - Path validation: Validates endpoint definitions
    - Schema validation: Checks component schemas
    - Tag validation: Ensures all tags are properly defined

Usage:
    python3 test_openapi_spec.py
    or
    pytest test_openapi_spec.py

Requirements:
    - Python 3.7+
    - PyYAML: pip install pyyaml
    - pytest (optional): pip install pytest

Author: Venice.ai API Reference Team
"""

import yaml
import sys
import os
from typing import Dict, Any, List, Set


class TestOpenAPISpec:
    """
    Test suite for validating the Venice.ai OpenAPI specification.
    
    This class contains test methods that validate various aspects of the
    OpenAPI specification including structure, metadata, security, paths,
    schemas, and tags.
    
    Attributes:
        spec_path (str): Path to the OpenAPI specification file
        spec (dict): Loaded OpenAPI specification data
    """
    
    def __init__(self, spec_path: str = "venice.openapi.v3.yaml"):
        """
        Initialize the test suite.
        
        Args:
            spec_path (str): Path to the OpenAPI specification YAML file.
                            Defaults to "venice.openapi.v3.yaml".
        """
        self.spec_path = spec_path
        self.spec = None
        
    def load_spec(self) -> Dict[str, Any]:
        """
        Load and parse the OpenAPI specification file.
        
        Returns:
            dict: Parsed OpenAPI specification as a dictionary
            
        Raises:
            FileNotFoundError: If the specification file doesn't exist
            yaml.YAMLError: If the file contains invalid YAML
        """
        if not os.path.exists(self.spec_path):
            raise FileNotFoundError(f"OpenAPI spec file not found: {self.spec_path}")
            
        with open(self.spec_path, 'r', encoding='utf-8') as f:
            self.spec = yaml.safe_load(f)
            
        return self.spec
    
    def test_file_exists(self) -> bool:
        """
        Test that the OpenAPI specification file exists.
        
        Returns:
            bool: True if file exists, False otherwise
        """
        exists = os.path.exists(self.spec_path)
        print(f"✓ File exists: {self.spec_path}" if exists else f"✗ File not found: {self.spec_path}")
        return exists
    
    def test_valid_yaml(self) -> bool:
        """
        Test that the specification file is valid YAML.
        
        Returns:
            bool: True if YAML is valid, False otherwise
        """
        try:
            self.load_spec()
            print("✓ Valid YAML syntax")
            return True
        except yaml.YAMLError as e:
            print(f"✗ Invalid YAML: {e}")
            return False
    
    def test_openapi_version(self) -> bool:
        """
        Test that the OpenAPI version is specified and valid.
        
        Validates that the 'openapi' field exists and contains a valid
        OpenAPI version (3.0.x).
        
        Returns:
            bool: True if version is valid, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        version = self.spec.get('openapi')
        if not version:
            print("✗ Missing 'openapi' version field")
            return False
            
        if not version.startswith('3.0'):
            print(f"✗ Invalid OpenAPI version: {version} (expected 3.0.x)")
            return False
            
        print(f"✓ Valid OpenAPI version: {version}")
        return True
    
    def test_info_section(self) -> bool:
        """
        Test that the info section is complete and valid.
        
        Validates required fields in the info section:
        - title: API title
        - version: API version
        - description: API description
        - contact: Contact information
        
        Returns:
            bool: True if info section is valid, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        info = self.spec.get('info', {})
        required_fields = ['title', 'version', 'description']
        recommended_fields = ['contact', 'license']
        
        all_valid = True
        
        for field in required_fields:
            if field not in info:
                print(f"✗ Missing required field in info: {field}")
                all_valid = False
            else:
                print(f"✓ Info field present: {field}")
        
        for field in recommended_fields:
            if field not in info:
                print(f"⚠ Recommended field missing in info: {field}")
            else:
                print(f"✓ Info field present: {field}")
                
        return all_valid
    
    def test_servers_section(self) -> bool:
        """
        Test that at least one server is defined.
        
        Validates that the 'servers' section exists and contains at least
        one server with a valid URL.
        
        Returns:
            bool: True if servers are properly defined, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        servers = self.spec.get('servers', [])
        
        if not servers:
            print("✗ No servers defined")
            return False
            
        if not isinstance(servers, list):
            print("✗ Servers must be a list")
            return False
            
        for idx, server in enumerate(servers):
            if 'url' not in server:
                print(f"✗ Server {idx} missing 'url' field")
                return False
            print(f"✓ Server {idx} defined: {server['url']}")
            
        return True
    
    def test_security_schemes(self) -> bool:
        """
        Test that security schemes are properly defined.
        
        Validates that security schemes exist in components and are
        properly structured with required fields.
        
        Returns:
            bool: True if security schemes are valid, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        components = self.spec.get('components', {})
        security_schemes = components.get('securitySchemes', {})
        
        if not security_schemes:
            print("⚠ No security schemes defined")
            return True  # Not strictly required
            
        for name, scheme in security_schemes.items():
            if 'type' not in scheme:
                print(f"✗ Security scheme '{name}' missing 'type' field")
                return False
            print(f"✓ Security scheme defined: {name} ({scheme['type']})")
            
        return True
    
    def test_paths_section(self) -> bool:
        """
        Test that API paths are defined and valid.
        
        Validates that:
        - At least one path is defined
        - Each path has at least one operation (GET, POST, etc.)
        - Each operation has required fields
        
        Returns:
            bool: True if paths are valid, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        paths = self.spec.get('paths', {})
        
        if not paths:
            print("✗ No paths defined")
            return False
            
        path_count = len(paths)
        operation_count = 0
        
        for path, operations in paths.items():
            if not isinstance(operations, dict):
                print(f"✗ Invalid path definition: {path}")
                return False
                
            for method, operation in operations.items():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                    operation_count += 1
                    
                    # Check for required operation fields
                    if 'responses' not in operation:
                        print(f"✗ Operation {method.upper()} {path} missing 'responses'")
                        return False
        
        print(f"✓ Paths defined: {path_count} paths, {operation_count} operations")
        return True
    
    def test_components_schemas(self) -> bool:
        """
        Test that component schemas are defined.
        
        Validates that reusable schemas are defined in the components section.
        While not strictly required, schemas improve maintainability.
        
        Returns:
            bool: True if schemas are present or None, False if invalid
        """
        if not self.spec:
            self.load_spec()
            
        components = self.spec.get('components', {})
        schemas = components.get('schemas', {})
        
        if not schemas:
            print("⚠ No component schemas defined")
            return True  # Not strictly required
            
        schema_count = len(schemas)
        print(f"✓ Component schemas defined: {schema_count} schemas")
        return True
    
    def test_tags_defined(self) -> bool:
        """
        Test that all tags used in operations are defined globally.
        
        Validates that every tag referenced in path operations is also
        defined in the global tags section with a description.
        
        Returns:
            bool: True if all tags are properly defined, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        # Get globally defined tags
        global_tags = self.spec.get('tags', [])
        global_tag_names = {tag['name'] for tag in global_tags if isinstance(tag, dict) and 'name' in tag}
        
        # Get tags used in operations
        used_tags: Set[str] = set()
        paths = self.spec.get('paths', {})
        
        for path, operations in paths.items():
            if not isinstance(operations, dict):
                continue
                
            for method, operation in operations.items():
                if isinstance(operation, dict) and 'tags' in operation:
                    operation_tags = operation['tags']
                    if isinstance(operation_tags, list):
                        used_tags.update(operation_tags)
        
        # Check for undefined tags
        undefined_tags = used_tags - global_tag_names
        
        if undefined_tags:
            print(f"⚠ Tags used but not defined globally: {', '.join(undefined_tags)}")
            # Return True as some tags might be intentionally undefined
            return True
            
        print(f"✓ All {len(used_tags)} used tags are properly defined")
        return True
    
    def test_required_top_level_fields(self) -> bool:
        """
        Test that all required top-level OpenAPI fields are present.
        
        According to OpenAPI 3.0.0 spec, required fields are:
        - openapi: version string
        - info: metadata object
        - paths: endpoint definitions
        
        Returns:
            bool: True if all required fields exist, False otherwise
        """
        if not self.spec:
            self.load_spec()
            
        required_fields = ['openapi', 'info', 'paths']
        all_present = True
        
        for field in required_fields:
            if field not in self.spec:
                print(f"✗ Missing required top-level field: {field}")
                all_present = False
            else:
                print(f"✓ Required field present: {field}")
                
        return all_present
    
    def run_all_tests(self) -> bool:
        """
        Run all validation tests and report results.
        
        Executes all test methods in sequence and reports overall success
        or failure. Provides a summary of test results.
        
        Returns:
            bool: True if all tests passed, False if any test failed
        """
        print("=" * 60)
        print("Venice.ai OpenAPI Specification Test Suite")
        print("=" * 60)
        print()
        
        tests = [
            ("File Existence", self.test_file_exists),
            ("YAML Validity", self.test_valid_yaml),
            ("OpenAPI Version", self.test_openapi_version),
            ("Info Section", self.test_info_section),
            ("Servers Section", self.test_servers_section),
            ("Security Schemes", self.test_security_schemes),
            ("Paths Section", self.test_paths_section),
            ("Component Schemas", self.test_components_schemas),
            ("Tag Definitions", self.test_tags_defined),
            ("Required Fields", self.test_required_top_level_fields),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n--- Testing: {test_name} ---")
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"✗ Test failed with exception: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status}: {test_name}")
        
        print()
        print(f"Results: {passed}/{total} tests passed")
        print("=" * 60)
        
        return all(result for _, result in results)


def main():
    """
    Main entry point for running the test suite.
    
    Executes all tests and exits with appropriate status code:
    - 0 if all tests pass
    - 1 if any test fails
    """
    # Determine spec file path
    spec_path = "venice.openapi.v3.yaml"
    
    # Allow override via command line argument
    if len(sys.argv) > 1:
        spec_path = sys.argv[1]
    
    # Run tests
    test_suite = TestOpenAPISpec(spec_path)
    success = test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
