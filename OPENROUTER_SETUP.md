# OpenRouter Setup Guide

OpenRouter is a unified API that gives you access to multiple LLM models from different providers. It's great for this project because it offers free credits and supports many models.

## Step 1: Get OpenRouter API Key

1. **Sign up at OpenRouter**
   - Go to [https://openrouter.ai/](https://openrouter.ai/)
   - Click "Sign Up" or "Get Started"
   - Create an account (you can use GitHub, Google, or email)

2. **Get your API Key**
   - After signing in, go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
   - Click "Create Key"
   - Give it a name (e.g., "SuperBryn Voice Agent")
   - Copy the API key (you'll only see it once!)

3. **Check your credits**
   - OpenRouter provides free credits for new users
   - Go to [https://openrouter.ai/credits](https://openrouter.ai/credits) to see your balance
   - You can add more credits if needed

## Step 2: Choose a Model

OpenRouter supports many models. Here are good options for this project:

### Recommended Models (Free/Cheap):
- **`google/gemini-flash-1.5`** - Fast and free
- **`meta-llama/llama-3.2-3b-instruct:free`** - Free Llama model
- **`mistralai/mistral-7b-instruct:free`** - Free Mistral model
- **`qwen/qwen-2.5-7b-instruct:free`** - Free Qwen model

### Paid Models (Better Quality):
- **`openai/gpt-4o-mini`** - Fast and affordable ($0.15/$0.60 per 1M tokens)
- **`anthropic/claude-3-haiku`** - Fast Claude model
- **`openai/gpt-4o`** - Best quality but more expensive
- **`anthropic/claude-3.5-sonnet`** - High quality Claude

See all models at: [https://openrouter.ai/models](https://openrouter.ai/models)

## Step 3: Configure Backend

1. **Edit your `.env` file** in the `backend` directory:

```bash
cd backend
nano .env  # or use your preferred editor
```

2. **Set these variables**:

```env
# LLM Configuration
LLM_PROVIDER=openrouter
LLM_MODEL=google/gemini-flash-1.5
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

**Example configurations:**

For free model:
```env
LLM_PROVIDER=openrouter
LLM_MODEL=meta-llama/llama-3.2-3b-instruct:free
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

For paid model (better quality):
```env
LLM_PROVIDER=openrouter
LLM_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

3. **Save the file**

## Step 4: Test the Configuration

1. **Start the backend**:
```bash
cd backend
python agent.py dev
```

2. **Check for errors**:
   - If you see connection errors, verify your API key
   - If you see model errors, check the model name is correct
   - Make sure the model supports function calling (most do)

## Step 5: Verify It's Working

1. Start your frontend
2. Start a voice call
3. The agent should respond using the OpenRouter model you selected

## Troubleshooting

### "Invalid API Key"
- Double-check you copied the full key (starts with `sk-or-v1-`)
- Make sure there are no extra spaces
- Verify the key is active in OpenRouter dashboard

### "Model not found"
- Check the exact model name at [https://openrouter.ai/models](https://openrouter.ai/models)
- Model names are case-sensitive
- Format: `provider/model-name` or `provider/model-name:free`

### "Insufficient credits"
- Check your balance at [https://openrouter.ai/credits](https://openrouter.ai/credits)
- Use a free model if you're out of credits
- Add credits if needed

### "Function calling not supported"
- Some free models may not support function calling well
- Try: `google/gemini-flash-1.5` or `openai/gpt-4o-mini`
- Check model capabilities on OpenRouter

## Model Recommendations by Use Case

### Best for Development/Testing (Free):
```env
LLM_MODEL=google/gemini-flash-1.5
```

### Best Balance (Low Cost, Good Quality):
```env
LLM_MODEL=openai/gpt-4o-mini
```

### Best Quality (Higher Cost):
```env
LLM_MODEL=openai/gpt-4o
# or
LLM_MODEL=anthropic/claude-3.5-sonnet
```

## Cost Tracking (Optional)

OpenRouter provides usage tracking:
- View usage at [https://openrouter.ai/activity](https://openrouter.ai/activity)
- Set up spending limits in settings
- Monitor costs per request

## Additional Resources

- **OpenRouter Docs**: [https://openrouter.ai/docs](https://openrouter.ai/docs)
- **Model List**: [https://openrouter.ai/models](https://openrouter.ai/models)
- **Pricing**: [https://openrouter.ai/models](https://openrouter.ai/models) (click on any model for pricing)

## Quick Reference

Your `.env` file should look like this:

```env
# ... other configs ...

# LLM Configuration - OpenRouter
LLM_PROVIDER=openrouter
LLM_MODEL=google/gemini-flash-1.5
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here

# ... other configs ...
```

That's it! Your agent will now use OpenRouter for all LLM calls.
