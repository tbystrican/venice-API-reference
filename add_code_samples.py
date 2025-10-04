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
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def str_presenter(dumper, data):
    # Use '|' for multiline strings
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter, Dumper=MyDumper)


def add_code_samples(spec_path="venice.openapi.v3.yaml"):
    '''
    Adds boilerplate x-codeSamples to all operations in an OpenAPI spec
    that don't already have them.
    '''
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
                "  -H 'Authorization: Bearer YOUR_API_KEY'"
            ]
            if method.lower() in ['post', 'put', 'patch']:
                curl_lines.extend([
                    "  -H 'Content-Type: application/json' \\",
                    "  -d '{}'"
                ])
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
                "    'Authorization': 'Bearer YOUR_API_KEY'",
            ]
            if method.lower() in ['post', 'put', 'patch']:
                js_lines.extend([
                    "    'Content-Type': 'application/json'",
                    "  },",
                    "  body: JSON.stringify({})"
                ])
            else:
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
