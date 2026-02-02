"""Test script to verify Azure OpenAI configuration"""
import os
import asyncio
from dotenv import load_dotenv
from livekit.plugins import openai as openai_plugin
from livekit.agents import llm

load_dotenv()

async def test_azure_openai():
    """Test Azure OpenAI connection"""
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    
    print("Azure OpenAI Configuration:")
    print(f"  Endpoint: {azure_endpoint}")
    print(f"  API Key: {'*' * min(len(azure_api_key or ''), 10)}")
    print(f"  API Version: {azure_api_version}")
    print(f"  Deployment Name: {deployment_name}")
    print()
    
    # Try different base_url formats
    formats = [
        # Format 1: Just endpoint
        (azure_endpoint.rstrip('/'), "Just endpoint"),
        # Format 2: Endpoint + /openai
        (f"{azure_endpoint.rstrip('/')}/openai", "Endpoint + /openai"),
        # Format 3: Endpoint + /openai + api-version
        (f"{azure_endpoint.rstrip('/')}/openai?api-version={azure_api_version}", "Endpoint + /openai + api-version"),
        # Format 4: Endpoint + /openai/deployments/{deployment}
        (f"{azure_endpoint.rstrip('/')}/openai/deployments/{deployment_name}", "Endpoint + /openai/deployments/{deployment}"),
    ]
    
    for base_url, description in formats:
        print(f"Testing format: {description}")
        print(f"  Base URL: {base_url}")
        try:
            llm_instance = openai_plugin.LLM(
                model=deployment_name,
                api_key=azure_api_key,
                base_url=base_url,
            )
            
            chat_ctx = llm.ChatContext()
            chat_ctx.add_message(role="user", content="Say hello")
            
            print("  Attempting chat request...")
            async with llm_instance.chat(chat_ctx=chat_ctx) as stream:
                response_text = ""
                async for chunk in stream:
                    if chunk.delta and chunk.delta.content:
                        response_text += chunk.delta.content
                
                print(f"  ✅ SUCCESS! Response: {response_text[:50]}...")
                print(f"  ✅ This format works! Use this base_url: {base_url}")
                return base_url
        except Exception as e:
            print(f"  ❌ FAILED: {type(e).__name__}: {e}")
            print()
    
    print("❌ None of the formats worked. Please check your Azure OpenAI configuration.")
    return None

if __name__ == "__main__":
    asyncio.run(test_azure_openai())
