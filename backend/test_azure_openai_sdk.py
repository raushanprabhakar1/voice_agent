"""Test script to verify Azure OpenAI configuration using Azure OpenAI SDK"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_azure_openai_sdk():
    """Test Azure OpenAI connection using the Azure OpenAI SDK"""
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    
    print("=" * 60)
    print("Azure OpenAI SDK Test")
    print("=" * 60)
    print(f"Endpoint: {azure_endpoint}")
    print(f"API Key: {'*' * min(len(azure_api_key or ''), 10)}")
    print(f"API Version: {azure_api_version}")
    print(f"Deployment Name: {deployment_name}")
    print()
    
    if not azure_endpoint or not azure_api_key:
        print("❌ ERROR: AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set")
        return False
    
    # Test 1: Using OpenAI SDK with Azure configuration
    print("Test 1: Using OpenAI SDK with Azure configuration (LiveKit approach)")
    print("-" * 60)
    try:
        import openai
        from livekit.plugins import openai as openai_plugin
        
        base_url = azure_endpoint.rstrip("/")
        
        # Create OpenAI client with Azure configuration
        client = openai.AsyncClient(
            api_key=azure_api_key,
            base_url=base_url,
            default_query={"api-version": azure_api_version},
        )
        
        # Create LLM instance
        llm_instance = openai_plugin.LLM(
            model=deployment_name,
            client=client,
        )
        
        # Test chat
        from livekit.agents import llm as llm_module
        chat_ctx = llm_module.ChatContext()
        chat_ctx.add_message(role="user", content="Say hello in one word")
        
        print("  Sending test message...")
        async with llm_instance.chat(chat_ctx=chat_ctx) as stream:
            response_text = ""
            async for chunk in stream:
                if chunk.delta and chunk.delta.content:
                    response_text += chunk.delta.content
            
            print(f"  ✅ SUCCESS! Response: {response_text}")
            print(f"  ✅ LiveKit Azure OpenAI configuration works!")
            return True
            
    except Exception as e:
        print(f"  ❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 2: Direct Azure OpenAI SDK test
    print("Test 2: Direct Azure OpenAI SDK test")
    print("-" * 60)
    try:
        from openai import AzureOpenAI
        
        client = AzureOpenAI(
            api_key=azure_api_key,
            api_version=azure_api_version,
            azure_endpoint=azure_endpoint,
        )
        
        print("  Sending test message...")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "Say hello in one word"}
            ],
            max_tokens=10,
        )
        
        response_text = response.choices[0].message.content
        print(f"  ✅ SUCCESS! Response: {response_text}")
        print(f"  ✅ Direct Azure OpenAI SDK works!")
        return True
        
    except Exception as e:
        print(f"  ❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 3: Using OpenAI SDK with manual URL construction
    print("Test 3: Using OpenAI SDK with manual URL construction")
    print("-" * 60)
    try:
        import openai
        
        # Construct the full base URL
        base_url = f"{azure_endpoint.rstrip('/')}/openai/deployments/{deployment_name}"
        
        client = openai.AsyncClient(
            api_key=azure_api_key,
            base_url=base_url,
            default_query={"api-version": azure_api_version},
        )
        
        print("  Sending test message...")
        response = await client.chat.completions.create(
            model=deployment_name,  # Still needed even though it's in the URL
            messages=[
                {"role": "user", "content": "Say hello in one word"}
            ],
            max_tokens=10,
        )
        
        response_text = response.choices[0].message.content
        print(f"  ✅ SUCCESS! Response: {response_text}")
        print(f"  ✅ Manual URL construction works!")
        return True
        
    except Exception as e:
        print(f"  ❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    print("=" * 60)
    print("❌ All tests failed. Please check your Azure OpenAI configuration.")
    print("=" * 60)
    return False

if __name__ == "__main__":
    success = asyncio.run(test_azure_openai_sdk())
    exit(0 if success else 1)
