# Environment Variables

## .env
- `PERPLEXITY_API_KEY`: your perplexity api key
- `OPENAI_API_KEY`: your openai api key

# Project Structure

## ./ai_agents/

### openai_agents.py
- Uses OpenAI API to generate a response
- Uses function calling to get a response in a specific format
- Uses structured output to get a response in a specific format
- Uses JSON mode to get a response in a specific format
- Uses JSON schema to get a response in a specific format

### perplexity_api.py
- Uses Perplexity API to generate a response
- Returns a JSON object with the response, citations, and other information
