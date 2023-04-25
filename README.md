# Text Bot GPT
License: GPL v3

This is a text bot for iMessage that uses a fine-tuned model from OpenAI's GPT. The program continuously runs to constantly check whether it needs to respond to a text message. If the specified number texts you, it will automatically feed the text message into OpenAI's ChatGPT API, using the fine-tuned model, and generate a response to the text. This text will then be sent to the specified phone number.

There are options to configure this program, such as removing the 'Approval' required before automatically sending responses. Many comments are added throughout the code for those curious about its inner workings. The comments also note some changes in functionality you can make.

This project is still heavily under development, so expect updates and changes in the coming days.

If you like my work, please consider donating:

[Buy Me A Coffee](https://www.buymeacoffee.com/tristanc)

## Getting Started
These are some basic instructions to help you get started.

### Prerequisites
What you need to install:

- imessage-reader - Python library for working with iMessage
- OpenAI API - ChatGPT API

Follow this link to enable full disk access for Terminal. This allows the program to access your chat.db in order to read and respond to text messages.

### Installing
A step-by-step series of examples that tell you how to get a development environment running:

1. Install OpenAI API (After obtaining an API key from the website):

pip install openai

2. Install imessage-reader:

pip install imessage-reader

3. Install tokenizer:

pip install tokenizers


## Usage
Before using the program, open the file 'config.py' and paste your OpenAI API key and fine-tuned model ID at the designated locations. Then paste the phone number you want to text with at the designated location (you may change this often depending on who you want to text). You also need to specify the path to the `send_iMessage.scpt` file that was downloaded (This is most likely located in the same directory as the other files you downloaded). For example: `script_path = "/Users/name/Desktop/text-bot-GPT/send_iMessage.scpt"`

To run the program, simply open your Terminal and go to the directory in which the files are located.

Then run:

python3 text-bot-GPT.py

This starts the program using your provided configuration. The program will say 'waiting' if you were the last to text in a conversation. Otherwise, it will print out a person's text, print out ChatGPT's response, and await your approval before sending.

## Built With
- [imessage-reader](https://github.com/niftycode/imessage_reader) - Python library for working with iMessage
- [OpenAI API](https://beta.openai.com/docs/) - ChatGPT API
- AppleScript - Used for sending iMessages

## Author
- Tristan (tristanc)

## License
This project is licensed under the GNU v.3 General Public License - see the LICENSE.md file for details

## Acknowledgments
- Shoutout to [niftycode](https://github.com/niftycode) - Author of imessage-reader
- [OpenAI](https://www.openai.com/)
