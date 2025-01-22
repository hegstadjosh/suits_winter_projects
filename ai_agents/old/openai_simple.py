from openai import OpenAI
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client and Rich console
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
console = Console()


def get_ai_response(messages, model="gpt-4o"):
    """
    Get AI response for given messages using specified model.
    
    Args:
        messages (list): List of message dictionaries with role and content
        model (str): Model identifier to use for the completion
        
    Returns:
        tuple: (updated_messages, success, error_message)
    """

    if type(messages) == str: 
        print("messages is a string, converting to list")
        messages = [{"role": "user", "content": messages}]

    try:
        if model != "gpt-4o": 
            # Remove system message if present
            messages = [msg for msg in messages if msg["role"] != "system"]

        # Get AI response
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        # Extract AI response
        ai_response = response.choices[0].message.content
        
        # Add AI response to messages
        messages.append({"role": "assistant", "content": ai_response})
        
        return messages, True, ai_response
        
    except Exception as e:
        return messages, False, str(e)

def chat_with_ai():
    # Available models
    models = {
        "1": "gpt-4o",
        "2": "o1-preview",
        "3": "o1-mini"
    }
    
    # Let user choose model
    print("\nAvailable models:")
    for key, model in models.items():
        print(f"{key}: {model}")
    
    model_choice = input("\nChoose a model (1-3) or press Enter for default (gpt-4o): ").strip()
    
    # Set model based on user choice
    selected_model = models.get(model_choice, "gpt-4o")
    print(f"\nUsing model: {selected_model}")

    # Initialize conversation with system message only for gpt-4o
    messages = []
    if selected_model == "gpt-4o":
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Respond in a friendly and concise manner."
        })
    
    print("\nChat started! (Type 'quit' to end the conversation)")
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check if user wants to quit
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break
            
        # Add user message to conversation
        messages.append({"role": "user", "content": user_input})
        
        # Get AI response using the new function
        messages, success, response = get_ai_response(messages, selected_model)
        
        if success:
            # Print AI response with markdown rendering
            print("\nAI:")
            md = Markdown(response)
            console.print(md)
        else:
            print(f"\nError: {response}")
            break

if __name__ == "__main__":
    chat_with_ai() 