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
        
        try:
            # Get AI response
            response = client.chat.completions.create(
                model=selected_model,
                messages=messages
            )
            
            # Extract AI response
            ai_response = response.choices[0].message.content
            
            # Print AI response with markdown rendering
            print("\nAI:")
            md = Markdown(ai_response)
            console.print(md)
            
            # Add AI response to conversation history
            messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            break

if __name__ == "__main__":
    chat_with_ai() 