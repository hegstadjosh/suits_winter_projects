from openai import OpenAI
import json
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
YOUR_API_KEY = os.getenv('PERPLEXITY_API_KEY')

# Initialize OpenAI client with Perplexity base URL
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

def get_perplexity_response(user_query, stream=False):
    messages = [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    # Parameters for the API call
    params = {
        "model": "sonar-pro",  # Using the pro model, can be changed to other sonar models
        "messages": messages,
        "temperature": 0.2,
        "stream": stream
    }

    try:
        if stream:
            response_stream = client.chat.completions.create(**params)
            return response_stream
        else:
            response = client.chat.completions.create(**params)
            return response
    except Exception as e:
        print(f"Error making API call: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Example query
    query = "Capital of India?"
    
    # Non-streaming example
    print("\nNon-streaming response:")
    response = get_perplexity_response(query)
    if response:
        print(f"User: {query}\n")
        print(f"Assistant: {response.choices[0].message.content}\n")
        
    # Streaming example
    print("\nStreaming response:")
    stream_response = get_perplexity_response(query, stream=True)
    if stream_response:
        print(f"User: {query}\n")
        print("Assistant: ", end="")
        for chunk in stream_response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
        print("\n")
