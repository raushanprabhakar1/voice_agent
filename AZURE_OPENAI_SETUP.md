# Azure OpenAI Setup Guide

Azure OpenAI provides access to OpenAI models through Microsoft Azure. This guide will help you set it up for the SuperBryn Voice Agent.

## Step 1: Create Azure OpenAI Resource

1. **Sign in to Azure Portal**
   - Go to [https://portal.azure.com/](https://portal.azure.com/)
   - Sign in with your Microsoft account

2. **Create Azure OpenAI Resource**
   - Click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create"
   - Fill in the form:
     - **Subscription**: Select your subscription
     - **Resource Group**: Create new or use existing
     - **Region**: Choose a region (e.g., East US, West Europe)
     - **Name**: Give it a name (e.g., `my-openai-resource`)
     - **Pricing Tier**: Choose your tier
   - Click "Review + create", then "Create"
   - Wait for deployment (takes a few minutes)

3. **Get Your Endpoint and Keys**
   - Once deployed, go to your resource
   - Under "Resource Management" → "Keys and Endpoint"
   - Copy:
     - **Endpoint**: `https://your-resource-name.openai.azure.com/`
     - **Key 1** or **Key 2**: Either one works

## Step 2: Deploy a Model

1. **Go to Azure OpenAI Studio**
   - In your Azure OpenAI resource, click "Go to Azure OpenAI Studio"
   - Or visit: [https://oai.azure.com/](https://oai.azure.com/)

2. **Deploy a Model**
   - Click "Deployments" in the left menu
   - Click "Create" or "+ Create"
   - Fill in:
     - **Model**: Choose a model (e.g., `gpt-4o`, `gpt-4o-mini`, `gpt-35-turbo`)
     - **Deployment name**: Give it a name (e.g., `gpt-4o-mini`)
     - **Model version**: Usually auto-selected
     - **Capacity**: Choose based on your needs
   - Click "Create"
   - Wait for deployment (may take a few minutes)

3. **Note Your Deployment Name**
   - This is the name you'll use in your `.env` file
   - Example: `gpt-4o-mini`, `gpt-4o`, etc.

## Step 3: Configure Backend

1. **Edit your `.env` file** in the `backend` directory:

```bash
cd backend
nano .env  # or use your preferred editor
```

2. **Add Azure OpenAI configuration**:

```env
# LLM Configuration - Azure OpenAI
LLM_PROVIDER=azure
LLM_MODEL=gpt-4o-mini  # This is just a label, actual model is from deployment name
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini  # Must match your deployment name
```

### Example Configuration

If your Azure resource is named `my-openai-resource` and you deployed `gpt-4o-mini`:

```env
LLM_PROVIDER=azure
LLM_MODEL=gpt-4o-mini
AZURE_OPENAI_ENDPOINT=https://my-openai-resource.openai.azure.com
AZURE_OPENAI_API_KEY=abc123def456ghi789...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

## Step 4: Test the Configuration

1. **Start the backend**:
```bash
cd backend
python agent.py dev
```

2. **Check for errors**:
   - If you see connection errors, verify your endpoint URL
   - If you see "deployment not found", check your deployment name
   - Make sure your API key is correct

## Step 5: Verify It's Working

1. Start your frontend
2. Start a voice call
3. The agent should respond using your Azure OpenAI deployment

## API Version

Azure OpenAI requires an API version. Common versions:
- `2024-02-15-preview` (recommended, supports latest features)
- `2023-12-01-preview`
- `2023-05-15`

Check the latest version in [Azure OpenAI documentation](https://learn.microsoft.com/azure/ai-services/openai/reference).

## Troubleshooting

### "Invalid endpoint"
- Make sure your endpoint URL is correct
- Should be: `https://your-resource-name.openai.azure.com`
- No trailing slash needed (code handles it)
- Check you're using the correct region

### "Deployment not found"
- Verify the deployment name matches exactly
- Check in Azure OpenAI Studio → Deployments
- Deployment name is case-sensitive

### "Invalid API key"
- Verify you copied the full key
- Try using Key 2 if Key 1 doesn't work
- Regenerate keys if needed

### "Model not found"
- The `LLM_MODEL` in `.env` is just a label
- The actual model is determined by `AZURE_OPENAI_DEPLOYMENT_NAME`
- Make sure the deployment exists and is active

### "API version not supported"
- Try a different API version
- Check which versions your deployment supports
- Latest: `2024-02-15-preview`

## Available Models in Azure OpenAI

Common models you can deploy:
- **gpt-4o**: Most capable, higher cost
- **gpt-4o-mini**: Fast and affordable
- **gpt-35-turbo**: Legacy but still good
- **gpt-4**: Previous generation
- **gpt-4-turbo**: Faster GPT-4

Check availability in your region at [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service).

## Cost Considerations

- Azure OpenAI pricing is similar to OpenAI
- Check pricing at: [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- Monitor usage in Azure Portal → Cost Management
- Set up spending limits if needed

## Security Best Practices

1. **Never commit API keys** to git
2. **Use Azure Key Vault** for production (optional)
3. **Rotate keys** periodically
4. **Use managed identity** for production deployments (advanced)

## Quick Reference

Your `.env` file should look like this:

```env
# ... other configs ...

# LLM Configuration - Azure OpenAI
LLM_PROVIDER=azure
LLM_MODEL=gpt-4o-mini
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your-actual-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

# ... other configs ...
```

## Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure OpenAI Studio](https://oai.azure.com/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- [API Reference](https://learn.microsoft.com/azure/ai-services/openai/reference)

That's it! Your agent will now use Azure OpenAI for all LLM calls.
