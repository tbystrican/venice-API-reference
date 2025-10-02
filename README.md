# Venice.ai OpenAPI Specification v3.0.0

<p align="center">
  <a href="https://venice.ai" target="_blank">
    <img src="https://raw.githubusercontent.com/Fayeblade1488/Venice_api_swagger/main/.github/banner.svg" alt="Venice API Banner">
  </a>
</p>

<p align="center">
    Production-ready OpenAPI definition for the Venice.ai API. This repository hosts the canonical spec used to generate SDKs, publish reference docs, and validate compatibility.
</p>

<p align="center">
    <a href="https://github.com/Fayeblade1488/Venice_api_swagger/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Fayeblade1488/Venice_api_swagger?style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/Fayeblade1488/Venice_api_swagger/tags">
        <img src="https://img.shields.io/github/v/tag/Fayeblade1488/Venice_api_swagger?style=for-the-badge&sort=semver" alt="Version">
    </a>
    <a href="https://github.com/Fayeblade1488/Venice_api_swagger/actions/workflows/lint.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/Fayeblade1488/Venice_api_swagger/lint.yml?branch=main&style=for-the-badge" alt="Lint Status">
    </a>
</p>

---

## Table of Contents

- [TL;DR](#tldr)
- [What is This?](#what-is-this)
- [Contents](#contents)
- [Quick Start](#quick-start)
  - [Validate in Browser](#validate-in-browser-zero-install)
  - [Local Validation](#local-validation-recommended)
  - [Local Preview with Swagger UI](#local-preview-with-swagger-ui)
- [For Developers](#for-developers)
  - [Understanding the Structure](#understanding-the-structure)
  - [Making Changes](#making-changes)
  - [Contributing](#contributing)
- [Generate SDKs](#generate-sdks)
- [Mock Server](#mock-server-optional)
- [Technical Specifications](#-technical-specifications)
- [Usage Instructions](#usage-instructions)
- [Quality Metrics](#quality-metrics)
- [Additional Resources](#additional-resources)

---

## TL;DR

-   **Spec lives in**: `venice.openapi.v3.yaml`
-   **Lint and preview locally** using the provided `lint.sh` script.
-   **Generate SDKs** via `openapi-generator`
-   **Publish docs** with your preferred pipeline (Swagger UI / Redoc)

---

## What is This?

This repository contains the **official OpenAPI 3.0.0 specification** for the Venice.ai API. The specification serves as:

- 📚 **Single Source of Truth**: Canonical documentation for all API endpoints, parameters, and responses
- 🔧 **SDK Generation**: Input for generating client libraries in multiple programming languages
- 📖 **Interactive Documentation**: Source for Swagger UI, Redoc, and other API documentation tools
- ✅ **Validation**: Reference for validating API requests and responses
- 🤝 **Integration Guide**: Complete reference for developers integrating with Venice.ai

### Key Benefits

- **OpenAI Compatible**: Drop-in replacement for OpenAI API clients
- **Privacy Focused**: Zero data retention - your data is never stored
- **Comprehensive**: Covers all Venice.ai API features including chat, images, audio, embeddings, and more
- **Production Ready**: Fully validated and tested specification
- **Well Documented**: Extensive examples, descriptions, and code samples

---

## Contents

```
.
├─ venice.openapi.v3.yaml       # The complete OpenAPI specification
├─ .spectral.yaml               # Configuration for the Spectral linter
├─ lint.sh                      # Script to run local validation
├─ package.json                 # Node.js dependencies for linting
└─ README.md                    # This file
```

## Quick Start

### Validate in Browser (Zero Install)

1.  Open **[editor.swagger.io](https://editor.swagger.io)**
2.  Import `venice.openapi.v3.yaml`
3.  Confirm no errors; warnings are documented in comments where applicable.

### Local Validation (Recommended)

A `lint.sh` script is provided to simplify local validation. It runs both Spectral and Redocly linters to ensure the OpenAPI specification is valid and adheres to style guidelines.

**Prerequisites:**
- Make sure `npm` is installed.
- Install the required Node.js dependencies:
  ```bash
  npm install
  ```

**Usage:**
To run the linters, execute the script from the root of the repository:
```bash
./lint.sh
```
This will validate the `venice.openapi.v3.yaml` file and report any errors or warnings.

### Local Preview with Swagger UI

```bash
# Option A: Serve with Docker (swaggerapi/swagger-ui)
docker run -p 8080:8080 -e SWAGGER_JSON=/tmp/spec.yaml \
  -v "$PWD/venice.openapi.v3.yaml":/tmp/spec.yaml swaggerapi/swagger-ui

# Option B: Redoc (static)
npx @redocly/cli build-docs venice.openapi.v3.yaml -o docs/index.html
```

## For Developers

### Understanding the Structure

The OpenAPI specification is organized into several key sections:

#### 1. **Info Section** (`info`)
Contains metadata about the API including title, version, description, and contact information.

#### 2. **Security** (`security`, `components.securitySchemes`)
Defines authentication methods. Venice.ai uses Bearer token authentication with JWT format.

```yaml
# In your requests:
Authorization: Bearer YOUR_API_KEY
```

#### 3. **Tags** (`tags`)
Organizes endpoints into logical groups:
- **Chat**: Conversational AI endpoints
- **Models**: Model listing and information
- **Image**: Image generation and manipulation
- **Characters**: Custom AI personas
- **API Keys**: Key management
- **Embeddings**: Text embeddings
- **Audio/Speech**: Text-to-speech
- **Billing**: Usage tracking

#### 4. **Components** (`components.schemas`)
Reusable schema definitions for requests and responses. These are referenced throughout the spec using `$ref`.

#### 5. **Paths** (`paths`)
The actual API endpoints with their:
- **Operations**: GET, POST, DELETE, etc.
- **Parameters**: Query, path, and header parameters
- **Request Bodies**: Expected input schemas
- **Responses**: Possible response codes and schemas
- **Examples**: Request and response examples
- **Code Samples**: Usage examples in multiple languages

### Making Changes

When modifying the specification:

1. **Edit `venice.openapi.v3.yaml`** directly
2. **Follow OpenAPI 3.0.0 standards** - refer to [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.0)
3. **Validate frequently** - run `./lint.sh` after each change
4. **Test your changes** - preview in Swagger UI or Redoc
5. **Check examples** - ensure all examples are valid and realistic

#### Common Tasks

**Adding a new endpoint:**
```yaml
paths:
  /your/new/endpoint:
    post:
      summary: Brief description
      description: Detailed explanation
      tags:
        - YourTag
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/YourSchema'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/YourResponseSchema'
```

**Adding a new schema:**
```yaml
components:
  schemas:
    YourSchema:
      type: object
      properties:
        field_name:
          type: string
          description: What this field represents
          example: "example value"
      required:
        - field_name
```

**Adding code samples:**
```yaml
x-codeSamples:
  - lang: 'Python'
    label: 'Basic Example'
    source: |
      import requests
      
      response = requests.post(
          'https://api.venice.ai/api/v1/your/endpoint',
          headers={'Authorization': 'Bearer {VENICE_API_KEY}'},
          json={'field': 'value'}
      )
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up your development environment
- Testing changes
- Submitting pull requests
- Code style and documentation standards

**Quick contribution checklist:**
- [ ] Fork the repository
- [ ] Create a feature branch
- [ ] Make your changes
- [ ] Run `./lint.sh` to validate
- [ ] Test in Swagger UI or Redoc
- [ ] Submit a pull request with clear description

## Generate SDKs

Using `openapi-generator` (Java-based tool):

```bash
# Install (one-time)
brew install openapi-generator   # macOS
# or: docker pull openapitools/openapi-generator-cli

# Typescript (fetch)
openapi-generator generate \
  -i venice.openapi.v3.yaml \
  -g typescript-fetch \
  -o sdk/typescript

# Python
openapi-generator generate \
  -i venice.openapi.v3.yaml \
  -g python \
  -o sdk/python
```

**Notes:**

-   File upload endpoints are modeled with `oneOf` for binary (multipart), byte (base64 in JSON), and uri. Your generator should map these appropriately.
-   Chat completion response `role` is restricted to `assistant` for OpenAI compatibility.

## Mock Server (Optional)

```bash
docker run -p 4010:4010 -v "$PWD/venice.openapi.v3.yaml:/tmp/spec.yaml" stoplight/prism:4 \
  mock -h 0.0.0.0 /tmp/spec.yaml
```

## 🔧 Technical Specifications

### **Validation Status**
-  **OpenAPI 3.0.0 Compliant**
-  **0 Critical Errors**
-  **6 Warnings** (related to example validation)
-  **Ready for Production Use**

### **Enhanced Features**

#### **1. Schema Quality**
- Fixed nullable field handling across all schemas
- Improved type definitions with proper constraints
- Enhanced validation rules for request/response models
- Consistent schema structure throughout

#### **2. Operation Documentation**
- **Summary & Description**: Clear, feature-rich descriptions
- **Parameters**: Fully documented with examples and constraints
- **Request Body**: 6 comprehensive examples covering:
  - Simple chat completion
  - Streaming with web search
  - Vision-enabled conversations
  - Function calling
  - Character persona interactions
  - Reasoning model usage
- **Responses**: Detailed success/error responses with headers
- **Headers**: Rate limiting, compression, request IDs

#### **3. Code Samples**
Comprehensive `x-codeSamples` covering:

**cURL Examples:**
```bash
# Simple Chat
curl -X POST "https://api.venice.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer {VENICE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "venice-uncensored", "messages": [...]}'

# Streaming with Web Search
curl -X POST "https://api.venice.ai/api/v1/chat/completions" \
  -H "Accept: text/event-stream" \
  --no-buffer \
  -d '{"stream": true, "venice_parameters": {"enable_web_search": "auto"}}'
```

**JavaScript Examples:**
```javascript
// Basic Chat
const response = await fetch('https://api.venice.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {'Authorization': 'Bearer {VENICE_API_KEY}'},
  body: JSON.stringify({model: 'venice-uncensored', messages: [...]})
});

// Server-Sent Events Streaming
const reader = response.body.getReader();
// ... complete SSE implementation
```

**Python Examples:**
```python
# Simple Chat
response = requests.post(
    'https://api.venice.ai/api/v1/chat/completions',
    headers={'Authorization': 'Bearer {VENICE_API_KEY}'},
    json={'model': 'venice-uncensored', 'messages': [...]}
)

# Vision Chat with Images
# Function Calling
# SSE Streaming
# ... complete implementations
```

#### **4. Developer Experience**

**Tag Organization:**
```yaml
x-tagGroups:
  - name: Core AI Services
    tags: [Chat, Image, Audio, Speech, Embeddings]
  - name: Platform  
    tags: [Models, Characters, Billing, API Keys]
  - name: Experimental
    tags: [Preview]
```

**Enhanced Documentation:**
- Private AI guarantee prominently featured
- Zero-retention policy clearly explained
- Feature capabilities well documented
- Rate limiting and authentication details
- Comprehensive error handling guidance

## Usage Instructions

### **For API Documentation Tools**
1. Use `venice.openapi.v3.yaml` with Redoc, Swagger UI, or similar tools
2. The specification includes `x-logo` and styling information
3. Tag groups provide logical navigation structure

### **For Code Generation**
- All schemas are properly defined for client generation
- Examples provide realistic integration patterns
- Error handling is comprehensively documented

### **For Developer Integration**
- Copy code samples and replace `{VENICE_API_KEY}` with actual API key
- Examples demonstrate all major Venice features
- Authentication and error handling patterns included

## Quality Metrics

| Metric | Status | Details |
|--------|--------|---------|
| **Validation** | ✅ | 0 errors, 6 minor warnings |
| **Coverage** | ✅ | Complete `/chat/completions` documentation |
| **Examples** | ✅ | 6 request + 8 code samples |
| **Error Handling** | ✅ | All HTTP status codes documented |
| **Authentication** | ✅ | Bearer token with examples |
| **Features** | ✅ | Streaming, vision, tools, web search |


## Notes

- **API Key Placeholder**: All code samples use `{VENICE_API_KEY}` placeholder
- **Production Ready**: Specification validates without errors
- **Comprehensive Coverage**: All major Venice features documented
- **Best Practices**: Follows OpenAPI 3.0.0 standards and conventions

## Additional Resources

### Documentation
- **Official API Docs**: https://docs.venice.ai
- **Venice.ai Platform**: https://venice.ai
- **OpenAPI Specification**: https://spec.openapis.org/oas/v3.0.0

### Tools
- **Swagger Editor**: https://editor.swagger.io - Online editor and validator
- **Redocly CLI**: https://redocly.com/docs/cli - Advanced linting and documentation
- **Spectral**: https://stoplight.io/open-source/spectral - OpenAPI linter
- **OpenAPI Generator**: https://openapi-generator.tech - SDK generation tool

### Community & Support
- **Discord Community**: Join for support and updates
- **GitHub Issues**: Report bugs or request features
- **Support Email**: support@venice.ai

### Related Files
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [Venice.ai API reference KNOWLEDGE BASE.md](Venice.ai%20API%20reference%20KNOWLEDGE%20BASE.md) - Comprehensive API knowledge base

### API Version Information
- **Current OpenAPI Version**: 3.0.0
- **API Version**: 20250929.201934
- **Last Updated**: 2025-09-26

---

**Maintained by**: [Fayeblade1488](https://github.com/Fayeblade1488)  
**License**: MIT  
**Repository**: [venice-API-reference](https://github.com/Fayeblade1488/venice-API-reference)