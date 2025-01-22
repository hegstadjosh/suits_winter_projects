from openai import OpenAI
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console
import os

# Load environment variables
load_dotenv()

# Initialize clients and console
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
perplexity_client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'), 
    base_url="https://api.perplexity.ai"
)
console = Console()

def get_openai_completion(messages, model="gpt-4o"):
    """
    Get completion from OpenAI models.
    
    Args:
        messages (list or str): List of message dictionaries or a single string query
        model (str): OpenAI model identifier
        
    Returns:
        tuple: (updated_messages, success, response/error_message)
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    try:
        if model != "gpt-4o":
            messages = [msg for msg in messages if msg["role"] != "system"]

        response = openai_client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        ai_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_response})
        
        return messages, True, ai_response
        
    except Exception as e:
        return messages, False, str(e)

def get_perplexity_completion(query, model="sonar-pro", stream=False):
    """
    Get completion from Perplexity models.
    
    Args:
        query (str): User query
        model (str): Perplexity model name
        stream (bool): Whether to stream the response
        
    Returns:
        Response object or None if error
    """
    messages = [
        {"role": "system", "content": "Be precise and concise."},
        {"role": "user", "content": query}
    ]

    params = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "stream": stream
    }

    try:
        response = perplexity_client.chat.completions.create(**params)
        return response
    except Exception as e:
        print(f"Error making Perplexity API call: {str(e)}")
        return None

def get_llm_completion(query, model="gpt-4o", stream=False):
    """
    Unified interface for getting completions from either OpenAI or Perplexity models.
    
    Args:
        query (str or list): User query or message list
        model (str): Model identifier (e.g., "gpt-4o", "sonar-pro", "o1-mini")
        stream (bool): Whether to stream the response (Perplexity only)
        
    Returns:
        tuple: (success, response/error_message)
    """
    # Perplexity models
    if model.startswith("sonar"):
        response = get_perplexity_completion(query, model, stream)
        if response:
            if stream:
                return True, response
            return True, response.choices[0].message.content
        return False, "Failed to get Perplexity response"
    
    # OpenAI models
    else:
        messages, success, response = get_openai_completion(query, model)
        return success, response

def interactive_chat():
    """Interactive chat interface supporting both OpenAI and Perplexity models."""
    models = {
        "1": "gpt-4o",
        "2": "o1-preview",
        "3": "o1-mini",
        "4": "sonar-pro",
        "5": "sonar"
    }
    
    print("\nAvailable models:")
    for key, model in models.items():
        print(f"{key}: {model}")
    
    model_choice = input("\nChoose a model (1-5) or press Enter for default (gpt-4o): ").strip()
    selected_model = models.get(model_choice, "gpt-4o")
    print(f"\nUsing model: {selected_model}")

    messages = []
    if selected_model == "gpt-4o":
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Respond in a friendly and concise manner."
        })
    
    print("\nChat started! (Type 'quit' to end)")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break
            
        success, response = get_llm_completion(
            messages + [{"role": "user", "content": user_input}] if messages else user_input,
            selected_model
        )
        
        if success:
            print("\nAI:")
            if isinstance(response, str):
                md = Markdown(response)
                console.print(md)
            else:  # Streaming response
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="")
                print()
        else:
            print(f"\nError: {response}")
            break

if __name__ == "__main__":
    interactive_chat() 