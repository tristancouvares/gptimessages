from imessage_reader import fetch_data
from chat_functionality import *
from config import *
import subprocessfrom imessage_reader import fetch_data
from chat_functionality import *
from config import *
import subprocess
from tokenizers import ByteLevelBPETokenizer
import time


# Apple Script to send iMessage 'message' to recipient 'phone_number'
def send_imessage(phone_number, message):
    subprocess.run(["osascript", script_path, phone_number, message])

# Checks who (you or recipient) sent the last text message in a conversation
def check_last(message_list):
    message = message_list[-1]
    if message[5] == 0:
        return True
    return False

# Gets the last text message sent in a conversation
def get_last(message_list):
    return message_list[-1][1]

# Counts the number of tokens in a given text
def count_tokens(text):
    tokenizer = ByteLevelBPETokenizer()
    return len(tokenizer.encode(text).ids)

# Truncate conversation if the total number of tokens exceeds the model's limit
def truncate_conversation(conversation, model_max_tokens=4096):
    token_count = 0
    user_message_indices = []

    for idx, message in enumerate(conversation):
        message_tokens = count_tokens(message["content"]) + 1  # Adding 1 for the role token
        token_count += message_tokens
        if message["role"] == "user":
            user_message_indices.append(idx)

    while token_count >= model_max_tokens:
        if len(user_message_indices) < 2:
            break

        first_user_idx = user_message_indices.pop(0)
        second_user_idx = user_message_indices[0]

        tokens_to_remove = sum(
            count_tokens(conversation[i]["content"]) + 1
            for i in range(first_user_idx, second_user_idx)
        )
        token_count -= tokens_to_remove
        conversation = conversation[:first_user_idx] + conversation[second_user_idx:]

    return conversation



# Primarily composed of a while loop that constantly runs waits for texts until you press 'Ctrl-C'
def text_bot(
    phone_number,
    conversation=[{"role": "system", "content": "You are a helpful assistant."}],
):
    while True:
        print("Waiting...")
        while True:
            fd = fetch_data.FetchData()
            messages = fd.get_messages()
            message_list = [text for text in messages if text[0] == phone_number]

            if not message_list:  # Check if the message_list is empty
                print("No messages found. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before checking again
                continue

            if check_last(message_list):
                print(f"Text: {get_last(message_list)}\n")
                break


        # Uses the 'completed_assistant' function to get how ChatGPT would respond to the person's text message
        new_message = completed_assistant(get_last(message_list), conversation)
        print(f"Response: {new_message}")

        if require_approval:
            check = input(
                "Press the 'Enter' key to continue sending ('Ctr-C to abort):"
            )

        # Uses the apple script to send the message to the phone number you provided
        send_imessage(phone_number, new_message)
        print("Message sent")

# Get the conversation history between you and the recipient. Give ChatGPT this information so it can respond to texts within the context of the conversation history.
def get_history(phone_number):
    fd = fetch_data.FetchData()
    messages = fd.get_messages()
    message_list = [text for text in messages if text[0] == phone_number]
    message_quant = len(message_list)

    conversation = [
        {
            "role": "system",
            "content": "You are to pretend to be a helpful assistant.",
        },
    ]

    for i in range(message_quant):
        if message_list[i][5] == 0:  # User's message
            conversation.append({"role": "user", "content": message_list[i][1]})
        else:  # Assistant's message
            conversation.append({"role": "assistant", "content": message_list[i][1]})

    return conversation


if __name__ == "__main__":
    phone_number = "+1" + input("Enter the recipient's phone number (without +1): ")
    conversation = get_history(phone_number)
    conversation = truncate_conversation(conversation)
    text_bot(phone_number, conversation)
from tokenizers import ByteLevelBPETokenizer
import time


# Apple Script to send iMessage 'message' to recipient 'phone_number'
def send_imessage(phone_number, message):
    subprocess.run(["osascript", script_path, phone_number, message])

# Checks who (you or recipient) sent the last text message in a conversation
def check_last(message_list):
    message = message_list[-1]
    if message[5] == 0:
        return True
    return False

# Gets the last text message sent in a conversation
def get_last(message_list):
    return message_list[-1][1]

# Counts the number of tokens in a given text
def count_tokens(text):
    tokenizer = ByteLevelBPETokenizer()
    return len(tokenizer.encode(text).ids)

# Truncate conversation if the total number of tokens exceeds the model's limit
def truncate_conversation(conversation, model_max_tokens=4096):
    token_count = 0
    truncated_conversation = []

    for message in reversed(conversation):
        message_tokens = count_tokens(message["content"])
        if token_count + message_tokens < model_max_tokens:
            token_count += message_tokens
            truncated_conversation.insert(0, message)
        else:
            break

    return truncated_conversation

# Primarily composed of a while loop that constantly runs waits for texts until you press 'Ctrl-C'
def text_bot(
    phone_number,
    conversation=[{"role": "system", "content": "You are a helpful assistant."}],
):
    while True:
        print("Waiting...")
        while True:
            fd = fetch_data.FetchData()
            messages = fd.get_messages()
            message_list = [text for text in messages if text[0] == phone_number]

            if not message_list:  # Check if the message_list is empty
                print("No messages found. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before checking again
                continue

            if check_last(message_list):
                print(f"Text: {get_last(message_list)}\n")
                break


        # Uses the 'completed_assistant' function to get how ChatGPT would respond to the person's text message
        new_message = completed_assistant(get_last(message_list), conversation)
        print(f"Response: {new_message}")

        if require_approval:
            check = input(
                "Press the 'Enter' key to continue sending ('Ctr-C to abort):"
            )

        # Uses the apple script to send the message to the phone number you provided
        send_imessage(phone_number, new_message)
        print("Message sent")

# Get the conversation history between you and the recipient. Give ChatGPT this information so it can respond to texts within the context of the conversation history.
def get_history(phone_number):
    fd = fetch_data.FetchData()
    messages = fd.get_messages()
    message_list = [text for text in messages if text[0] == phone_number]
    message_quant = len(message_list)

    conversation = [
        {
            "role": "system",
            "content": "You are to pretend to be a helpful assistant.",
        },
    ]

    for i in range(message_quant):
        if message_list[i][5] == 0:  # User's message
            conversation.append({"role": "user", "content": message_list[i][1]})
        else:  # Assistant's message
            conversation.append({"role": "assistant", "content": message_list[i][1]})

    return conversation


if __name__ == "__main__":
    phone_number = input("Enter the recipient's phone number: ")
    conversation = get_history(phone_number)
    conversation = truncate_conversation(conversation)
    text_bot(phone_number, conversation)
