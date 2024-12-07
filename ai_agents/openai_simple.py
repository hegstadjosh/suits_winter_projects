from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat_with_ai():
    # Initialize conversation with system message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Respond in a friendly and concise manner."
        }
    ]
    
    print("Chat started! (Type 'quit' to end the conversation)")
    
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
                model="gpt-4o",  # You can change this to gpt-4 if you have access
                messages=messages
            )
            
            # Extract and print AI response
            ai_response = response.choices[0].message.content
            print("\nAI:", ai_response)
            
            # Add AI response to conversation history
            messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            break

if __name__ == "__main__":
    chat_with_ai() 