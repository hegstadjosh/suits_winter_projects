from openai import OpenAI
import requests
import json
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
YOUR_API_KEY = os.getenv('PERPLEXITY_API_KEY')

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": "Capital of India?"
        }
    ],
    #"max_tokens": "Optional",
    "temperature": 0.2,
    "top_p": 0.9,
    "search_domain_filter": ["perplexity.ai"],
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "month",
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
}
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}",
    "Content-Type": "application/json"
}

'''
INSTRUCTIONS:
below is a previous response json object in string form from the api
to get a real-time response, you will need to set up your own api key
do this by signing up with your school google account at https://perplexity.ai/
then go to https://www.perplexity.ai/settings/api and generate a new api key
go to the .env file and add the api key as PERPLEXITY_API_KEY
'''
response = ''' 
{
    "id": "3a9a1504-2203-4a59-8993-163c636a52e3",
    "model": "llama-3.1-sonar-small-128k-online",
    "created": 1733608672,
    "usage": {
        "prompt_tokens": 9,
        "completion_tokens": 29,
        "total_tokens": 38
    },
    "citations": [
        "https://en.wikipedia.org/wiki/Delhi",
        "https://www.britannica.com/place/Delhi",
        "https://www.jagranjosh.com/general-knowledge/which-city-became-the-capital-of-india-for-a-day-1731421925-1",
        "https://currentaffairs.adda247.com/states-and-capitals/",
        "https://www.foxnews.com/world/indias-capital-introduces-stricter-anti-pollution-measures-toxic-smog-hides-taj-mahal"
    ],
    "object": "chat.completion",
    "choices": [
        {
            "index": 0,
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "The capital of India is New Delhi, which is located in the National Capital Territory (NCT) of Delhi[1][2][4]."
            },
            "delta": {
                "role": "assistant",
                "content": ""
            }
        }
    ]
}
'''
#uncomment the line below to get a real-time response from the api
#response = requests.request("POST", url, json=payload, headers=headers)

print("User: ", payload["messages"][1]["content"], "\n")
print("Assistant: ", json.loads(response)["choices"][0]["message"]["content"], "\n")
print("Citations: ", json.loads(response)["citations"])
