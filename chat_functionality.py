import openai
from tokenizers import ByteLevelBPETokenizer

tokenizer = ByteLevelBPETokenizer()

def tokenize(text):
    tokens = tokenizer.encode(text).tokens
    return tokens

def ChatGPT_conversation(conversation):
    # Format the conversation history as a string
    conversation_history = "\n".join([f"{msg['role']}:{msg['content']}" for msg in conversation])

    # Add a more specific instruction for the model
    conversation_history += "\n\nassistant: You are a helpful assistant. Please respond to the last message from the user."
    
    openai.api_key = "OPENAIKEY"

    # Replace 'your_model_id_here' with your fine-tuned model's ID
    model_id = "MODELID"

    response = openai.Completion.create(
        engine=model_id,
        prompt=conversation_history,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )

    assistant_message = response.choices[0].text.strip()
    return assistant_message.strip()

def completed_assistant(user_message, conversation):
    conversation.append({"role": "user", "content": user_message})
    assistant_message = ChatGPT_conversation(conversation)
    conversation.append({"role": "assistant", "content": assistant_message})
    return assistant_message
