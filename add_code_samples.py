"""
add_code_samples.py - Automates adding code samples to the OpenAPI spec.

This script reads the OpenAPI specification file, identifies operations
that are missing `x-codeSamples`, and adds boilerplate examples for cURL,
Python, and JavaScript. It is designed to be run from the command line.
"""

import yaml
import sys

# A custom Dumper to produce cleaner YAML for multiline strings
class MyDumper(yaml.Dumper):
    """
    Custom YAML dumper for producing cleaner multiline string output.
    
    This dumper extends PyYAML's default Dumper to ensure that multiline
    strings are properly indented in the output YAML file. It's particularly
    useful for code samples that span multiple lines.
    
    Attributes:
        Inherits all attributes from yaml.Dumper
    
    Example:
        >>> yaml.dump(data, Dumper=MyDumper, sort_keys=False)
    """
    
    def increase_indent(self, flow=False, indentless=False):
        """
        Control indentation behavior for YAML output.
        
        This method overrides the parent class behavior to ensure consistent
        indentation across all YAML structures, including flow and block
        collections. It forces indentless=False to maintain proper indentation.
        
        Args:
            flow (bool): Whether the collection is in flow style. Defaults to False.
            indentless (bool): Whether to use indentless style. This parameter
                              is overridden to False internally. Defaults to False.
        
        Returns:
            The result of the parent class's increase_indent method with
            indentless forced to False.
        """
        return super(MyDumper, self).increase_indent(flow, False)

def str_presenter(dumper, data):
    """
    Custom string representer for YAML output.
    
    This function determines how strings should be represented in YAML output.
    It uses the literal style ('|') for multiline strings to preserve
    formatting and line breaks, making code samples more readable.
    
    Args:
        dumper: The YAML dumper instance performing the serialization.
        data (str): The string data to be represented in YAML format.
    
    Returns:
        A YAML scalar representation of the string. Uses literal style ('|')
        for multiline strings and default style for single-line strings.
    
    Example:
        Single-line: "Hello World"
        Multi-line:  |
                     Line 1
                     Line 2
    """
    # Use '|' for multiline strings
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter, Dumper=MyDumper)


def add_code_samples(spec_path="venice.openapi.v3.yaml"):
    """
    Add boilerplate code samples to OpenAPI specification operations.
    
    This function reads an OpenAPI specification file, identifies all operations
    (GET, POST, PUT, etc.) that don't have x-codeSamples, and adds boilerplate
    examples in three languages: cURL, Python (requests), and JavaScript (fetch).
    
    The generated code samples include:
    - Proper HTTP method and URL construction
    - Authorization header with Bearer token placeholder
    - Content-Type header for operations that accept request bodies
    - Request body structure for POST/PUT/PATCH operations
    - Response handling and output
    
    Args:
        spec_path (str): Path to the OpenAPI specification YAML file.
                        Defaults to "venice.openapi.v3.yaml".
    
    Raises:
        FileNotFoundError: If the specification file doesn't exist at spec_path.
        yaml.YAMLError: If the file exists but contains invalid YAML syntax.
        SystemExit: Exits with code 1 if file is not found or YAML is invalid.
    
    Side Effects:
        - Modifies the specification file in place by adding x-codeSamples
        - Prints progress messages to stdout for each operation modified
        - Prints success message when complete
    
    Example:
        >>> add_code_samples("my_api.yaml")
        Adding code samples to POST /api/endpoint
        Code samples added successfully.
    
    Note:
        Operations that already have x-codeSamples are skipped and not modified.
        Only valid HTTP methods (GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, TRACE)
        are processed.
    """
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Specification file not found at {spec_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Could not parse YAML file: {e}")
        sys.exit(1)


    paths = spec.get("paths", {})
    for path, path_item in paths.items():
        if not path_item:
            continue
        for method, operation in path_item.items():
            # Skip non-dict operations or those with existing samples
            if not isinstance(operation, dict) or "x-codeSamples" in operation:
                continue

            # Ensure it's a valid HTTP method before proceeding
            valid_methods = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
            if method.lower() not in valid_methods:
                continue

            print(f"Adding code samples to {method.upper()} {path}")

            # --- cURL Sample ---
            curl_lines = [
                f"curl -X {method.upper()} 'https://api.venice.ai/api/v1{path}' \\",
            ]
            
            if method.lower() in ['post', 'put', 'patch']:
                # For methods with request body, add backslash after Authorization
                curl_lines.append("  -H 'Authorization: Bearer YOUR_API_KEY' \\")
                curl_lines.extend([
                    "  -H 'Content-Type: application/json' \\",
                    "  -d '{}'"
                ])
            else:
                # For GET/DELETE/etc., Authorization is the last line (no backslash)
                curl_lines.append("  -H 'Authorization: Bearer YOUR_API_KEY'")
            
            curl_sample = '\n'.join(curl_lines)

            # --- Python Sample ---
            python_lines = [
                "import requests",
                "",
                f"url = 'https://api.venice.ai/api/v1{path}'",
                "headers = {'Authorization': 'Bearer YOUR_API_KEY'}"
            ]
            if method.lower() in ['post', 'put', 'patch']:
                 python_lines.append(f"response = requests.{method.lower()}(url, headers=headers, json={{}})")
            else:
                 python_lines.append(f"response = requests.{method.lower()}(url, headers=headers)")
            python_lines.extend(["", "print(response.json())"])
            python_sample = '\n'.join(python_lines)

            # --- JavaScript Sample ---
            js_lines = [
                f"const response = await fetch('https://api.venice.ai/api/v1{path}', {{",
                f"  method: '{method.upper()}',",
                "  headers: {",
            ]
            
            # Add Authorization header with comma only if there are more headers
            if method.lower() in ['post', 'put', 'patch']:
                js_lines.append("    'Authorization': 'Bearer YOUR_API_KEY',")
                js_lines.extend([
                    "    'Content-Type': 'application/json'",
                    "  },",
                    "  body: JSON.stringify({})"
                ])
            else:
                js_lines.append("    'Authorization': 'Bearer YOUR_API_KEY'")
                js_lines.append("  }")
            
            js_lines.extend([
                "});",
                "const data = await response.json();",
                "console.log(data);"
            ])
            js_sample = '\n'.join(js_lines)


            operation["x-codeSamples"] = [
                {"lang": "cURL", "label": "cURL", "source": curl_sample},
                {"lang": "Python", "label": "Python (requests)", "source": python_sample},
                {"lang": "JavaScript", "label": "JavaScript (fetch)", "source": js_sample},
            ]

    with open(spec_path, 'w', encoding='utf-8') as f:
        yaml.dump(spec, f, Dumper=MyDumper, sort_keys=False, indent=2, allow_unicode=True)

    print("\nCode samples added successfully.")

if __name__ == "__main__":
    add_code_samples()
