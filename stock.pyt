import nltk
from nltk.chat.util import Chat, reflections

# Define a set of patterns and responses
patterns = [
    (r'hi|hello|hey', ['Hello! How can I assist you today?', 'Hey there! How can I help you?']),
    (r'how are you?', ['I am doing great, thank you!', 'I am fine, how about you?']),
    (r'what is your name?', ['I am a chatbot, and I don\'t have a name yet. But you can call me ChatBot!']),
    (r'bye|goodbye', ['Goodbye! It was nice talking to you.']),
    (r'(.*) (help|assist) (.*)', ['I am here to help! What do you need assistance with?']),
    (r'(.*) (your name|you) (.*)', ['I am just a chatbot here to assist you!']),
    (r'(.*)', ['I\'m not sure I understand. Could you ask something else?'])
]

# Create the chatbot instance
chatbot = Chat(patterns, reflections)

# Function to start the conversation
def start_conversation():
    print("Hello! I am your chatbot. Type 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("ChatBot: Goodbye! Take care!")
            break
        response = chatbot.respond(user_input)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    start_conversation()
