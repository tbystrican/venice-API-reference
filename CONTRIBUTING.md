# Contributing to Venice.ai OpenAPI Specification

Thank you for your interest in contributing to the Venice.ai OpenAPI specification! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Testing Your Changes](#testing-your-changes)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Documentation Standards](#documentation-standards)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

This repository contains the OpenAPI 3.0.0 specification for the Venice.ai API. The main specification file is `venice.openapi.v3.yaml`.

### What You Can Contribute

- **Documentation improvements**: Enhance descriptions, add examples, improve clarity
- **Schema updates**: Add missing schemas or improve existing ones
- **Bug fixes**: Correct inaccuracies in the specification
- **Example additions**: Add more code samples and request/response examples
- **Error documentation**: Improve error response documentation

## How to Contribute

1. **Check existing issues**: Look for open issues or create a new one to discuss your proposed changes
2. **Fork the repository**: Create your own fork to work on
3. **Create a branch**: Use a descriptive branch name (e.g., `fix/chat-completion-schema`, `docs/add-python-examples`)
4. **Make your changes**: Follow the guidelines below
5. **Test your changes**: Ensure the specification validates correctly
6. **Submit a pull request**: Provide a clear description of your changes

## Development Setup

### Prerequisites

- **Node.js** (v14 or higher) - for running linters
- **npm** - for managing dependencies
- **Git** - for version control

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Fayeblade1488/venice-API-reference.git
   cd venice-API-reference
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. You're ready to make changes!

## Testing Your Changes

### Local Validation

Always validate your changes before submitting:

1. **Run the lint script**:
   ```bash
   ./lint.sh
   ```
   
   This runs both Spectral and Redocly linters to check for errors and style issues.

2. **Alternative: Run individual linters**:
   ```bash
   # Spectral lint
   npm run lint:api:spectral
   
   # Redocly lint
   npm run lint:api:redocly
   ```

### Browser Validation

You can also validate in a browser:

1. Go to [editor.swagger.io](https://editor.swagger.io)
2. Import the `venice.openapi.v3.yaml` file
3. Check for errors in the right panel

### Preview Documentation

Preview how your changes will look in documentation:

```bash
# Using Redoc
npx @redocly/cli build-docs venice.openapi.v3.yaml -o docs/index.html

# Using Swagger UI (Docker)
docker run -p 8080:8080 -e SWAGGER_JSON=/tmp/spec.yaml \
  -v "$PWD/venice.openapi.v3.yaml":/tmp/spec.yaml swaggerapi/swagger-ui
```

## Submitting Changes

### Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
   - Good: "Add Python streaming example for chat completions"
   - Bad: "Update spec"

2. **Description**: Include:
   - What changes you made
   - Why you made them
   - Any relevant issue numbers
   - Screenshots (if applicable for documentation changes)

3. **Validation**: Confirm that:
   - The specification validates without new errors
   - All existing functionality still works
   - New examples are accurate and tested

4. **Size**: Keep PRs focused and reasonably sized
   - If making multiple unrelated changes, submit separate PRs

### Commit Message Format

Use clear, descriptive commit messages:

```
type: brief description

Detailed explanation (if needed)

Fixes #issue_number
```

Types:
- `docs:` - Documentation changes
- `feat:` - New features or endpoints
- `fix:` - Bug fixes
- `refactor:` - Code restructuring without behavior change
- `test:` - Adding or updating tests
- `style:` - Formatting changes

Examples:
```
docs: add comprehensive Python examples for chat completions

Added examples showing streaming, function calling, and vision
capabilities using the OpenAI Python library.

Fixes #42
```

## Style Guidelines

### YAML Formatting

- **Indentation**: Use 2 spaces (no tabs)
- **Line length**: Keep lines under 120 characters when possible
- **Quotes**: Use double quotes for strings
- **Arrays**: Use bracket notation for short arrays, multiline for long arrays

### Description Writing

1. **Be concise but complete**: Provide enough detail to be useful
2. **Use proper grammar**: Full sentences with proper punctuation
3. **Include examples**: Show expected formats and values
4. **Document constraints**: Mention min/max values, required fields, etc.

### Schema Documentation

Every schema property should have:
- **type**: The data type
- **description**: What the field represents
- **example**: A realistic example value
- **constraints**: Any validation rules (min, max, pattern, enum, etc.)

Example:
```yaml
temperature:
  type: number
  minimum: 0
  maximum: 2
  default: 1
  description: |
    Controls randomness in the output. Higher values (e.g., 1.5) make output more random,
    while lower values (e.g., 0.2) make it more focused and deterministic.
  example: 0.8
```

### Endpoint Documentation

Each endpoint should include:
- **summary**: Brief one-line description
- **description**: Detailed explanation of functionality
- **parameters**: Full documentation of all parameters
- **requestBody**: Schema with examples
- **responses**: All possible response codes with examples
- **x-codeSamples**: Code examples in multiple languages

## Documentation Standards

### Code Samples

When adding code samples, include examples in at least these languages:
- **cURL**: For quick testing
- **Python**: Using the OpenAI library or requests
- **JavaScript**: Using fetch or the OpenAI library

Format:
```yaml
x-codeSamples:
  - lang: 'cURL'
    label: 'Basic Chat'
    source: |
      curl -X POST "https://api.venice.ai/api/v1/chat/completions" \
        -H "Authorization: Bearer {VENICE_API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "venice-uncensored",
          "messages": [{"role": "user", "content": "Hello!"}]
        }'
```

### API Key Handling

- Always use `{VENICE_API_KEY}` as a placeholder in examples
- Never commit real API keys
- Mention security best practices in documentation

### Error Documentation

Document errors with:
- HTTP status code
- Error schema
- Common causes
- How to resolve

### Version Information

- Keep version numbers up to date
- Document breaking changes
- Note deprecated features

## Questions?

If you have questions or need help:
- Open an issue with the `question` label
- Check existing documentation in the README
- Review the official Venice.ai documentation at https://docs.venice.ai

## Thank You!

Your contributions help make the Venice.ai API more accessible and easier to use for everyone. We appreciate your time and effort!
