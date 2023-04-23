import openai
from tokenizers import ByteLevelBPETokenizer

tokenizer = ByteLevelBPETokenizer()

def tokenize(text):
    tokens = tokenizer.encode(text).tokens
    return tokens

def truncate_conversation(conversation, max_tokens=4096):
    conversation_text = ''.join([msg['content'] for msg in conversation])
    conversation_tokens = tokenize(conversation_text)
    if len(conversation_tokens) > max_tokens:
        conversation_tokens = conversation_tokens[-max_tokens:]
    truncated_conversation = ''.join(conversation_tokens)
    return truncated_conversation

def ChatGPT_conversation(conversation):
    conversation = truncate_conversation(conversation)
    openai.api_key = "YOURAPIRKEYHERE"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="\n".join([msg["content"] for msg in conversation]),
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
