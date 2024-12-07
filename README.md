./.env:
- PERPLEXITY_API_KEY: your perplexity api key
- OPENAI_API_KEY: your openai api key

./ai_agents/
    openai_agents.py:
        - uses openai api to generate a response
        - uses function calling to get a response in a specific format
        - uses structured output to get a response in a specific format
        - uses json mode to get a response in a specific format
        - uses json schema to get a response in a specific format

    perplexity_api.py:
        - uses perplexity api to generate a response
        - returns a json object with the response, citations, and other information
