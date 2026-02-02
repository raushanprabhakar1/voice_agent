# Verifying Azure OpenAI Configuration

This guide helps you verify that your Azure OpenAI configuration is working correctly with LiveKit Agents.

## Quick Test

Run the test script to verify your Azure OpenAI setup:

```bash
cd backend
python test_azure_openai_sdk.py
```

Or if using the virtual environment:

```bash
cd backend
source venv/bin/activate
python test_azure_openai_sdk.py
```

## Manual Verification Steps

### 1. Check Environment Variables

Ensure your `.env` file has:

```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
```

### 2. Verify Deployment Name

The `AZURE_OPENAI_DEPLOYMENT_NAME` must **exactly match** the deployment name in Azure OpenAI Studio:
- Go to [Azure OpenAI Studio](https://oai.azure.com/)
- Navigate to "Deployments"
- Copy the exact deployment name (case-sensitive)

### 3. Test with Python Script

Create a simple test file `test_azure.py`:

```python
import os
import asyncio
from dotenv import load_dotenv
import openai
from livekit.plugins import openai as openai_plugin
from livekit.agents import llm

load_dotenv()

async def test():
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    print(f"Testing Azure OpenAI:")
    print(f"  Endpoint: {azure_endpoint}")
    print(f"  Deployment: {deployment_name}")
    print(f"  API Version: {azure_api_version}")
    
    # Create client with Azure configuration
    client = openai.AsyncClient(
        api_key=azure_api_key,
        base_url=azure_endpoint.rstrip("/"),
        default_query={"api-version": azure_api_version},
    )
    
    # Create LLM instance
    llm_instance = openai_plugin.LLM(
        model=deployment_name,
        client=client,
    )
    
    # Test chat
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(role="user", content="Say hello")
    
    async with llm_instance.chat(chat_ctx=chat_ctx) as stream:
        response = ""
        async for chunk in stream:
            if chunk.delta and chunk.delta.content:
                response += chunk.delta.content
        print(f"✅ Response: {response}")

if __name__ == "__main__":
    asyncio.run(test())
```

Run it:
```bash
python test_azure.py
```

### 4. Common Issues

#### 404 Error: Resource not found
- **Cause**: Wrong deployment name or endpoint
- **Fix**: 
  - Verify deployment name in Azure OpenAI Studio
  - Ensure endpoint is `https://{resource-name}.openai.azure.com` (no trailing slash, no `/openai`)

#### Authentication Error
- **Cause**: Wrong API key
- **Fix**: Regenerate API key in Azure Portal

#### API Version Error
- **Cause**: Unsupported API version
- **Fix**: Use `2024-02-15-preview` or `2024-06-01`

## Current Configuration

The current configuration in `agent.py` uses:

```python
client = openai.AsyncClient(
    api_key=azure_api_key,
    base_url=azure_endpoint.rstrip("/"),
    default_query={"api-version": azure_api_version},
)

llm_instance = openai_plugin.LLM(
    model=deployment_name,
    client=client,
)
```

This should work correctly with Azure OpenAI. If you're still getting errors, check:
1. The deployment name matches exactly
2. The endpoint URL is correct
3. The API key is valid
4. The API version is supported
