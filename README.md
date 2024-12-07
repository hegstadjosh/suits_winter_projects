# Intro 
Each of the files in ./ai_agents will run correctly if you have your api keys defined and the correct packages installed (you'll have to use pip install x if not). 

As well as free Perplexity Pro, we get $5 in free Perplexity API credits per month thru our Columbia Google accounts. I recommend purchasing OpenAI API credits-- $5 will last you a very long time (costs ~$1 per 40,000 words of input + output for gpt-4o), and it provides you much more capability than perplexity's (access to gpt-4o, new o1-preview & o1-mini; no searching; agents). 

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
