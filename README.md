# Venice.ai API

A privacy-first AI platform that provides OpenAI-compatible APIs for text and image generation. The platform emphasizes user privacy, open-source models, and uncensored AI responses.

**Complete API Reference**: For detailed information about all endpoints, parameters, and functionality, see our [comprehensive API reference](Venice.ai%20API%20reference%20KNOWLEDGE%20BASE.md).

## Features

- **Privacy-First Architecture**: Venice does not utilize or store user data for any purposes
- **Open-Source Models**: Only uses open-source models for full transparency
- **OpenAI API Compatible**: Seamless integration with existing OpenAI clients and tools
- **Uncensored Responses**: Default system prompts designed for natural, uncensored model responses
- **No Data Storage**: Venice does not store user conversations or generated content
- **Transparent Operations**: Full visibility into model operations and capabilities

## Base URL

All API requests must use Venice's base URL:
```
https://api.venice.ai/api/v1
```

## Authentication

Venice uses Bearer token authentication with JWT format:
```
Authorization: Bearer <your-api-key>
```

## Quick Start

### JavaScript/Node.js
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "your-api-key",
  baseURL: "https://api.venice.ai/api/v1",
});

// Chat completion
const response = await client.chat.completions.create({
  model: "venice-uncensored",
  messages: [
    { role: "user", content: "Hello!" }
  ]
});

console.log(response.choices[0].message.content);
```

### Python
```python
import openai

client = openai.OpenAI(
    api_key="your-venice-api-key",
    base_url="https://api.venice.ai/api/v1"
)

response = client.chat.completions.create(
    model="venice-uncensored",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## API Endpoints

- `POST /api/v1/chat/completions` - Generate text responses in a chat-like format
- `GET /api/v1/models` - List available models
- `POST /api/v1/images/generations` - Generate images from text prompts
- `POST /api/v1/image/generate` - Venice native image generation
- `POST /api/v1/embeddings` - Create embeddings for text
- `POST /api/v1/audio/speech` - Text-to-speech generation
- `GET /api/v1/characters` - Get available Venice characters
- `GET /api/v1/models/traits` - Get model traits
- `GET /api/v1/image/styles` - List available image styles

## Documentation

- **Comprehensive API Reference**: [Venice.ai API Reference KNOWLEDGE BASE.md](Venice.ai%20API%20reference%20KNOWLEDGE%20BASE.md)
- **Online Documentation**: https://docs.venice.ai
- **API Specification**: https://api.venice.ai/doc/api/swagger.yaml
- **Terms of Service**: https://venice.ai/legal/tos

## Support

- **Support Email**: support@venice.ai
