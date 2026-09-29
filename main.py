import os
import argparse
from dotenv import load_dotenv

from openai import OpenAI, chat


def main():
    print("Hello from ai-agent-nr!")
    # Setup environment and API_KEY
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key = None
        raise RuntimeError('No API key was found')

    # Setup OpenAI Client
    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
            api_key = api_key,
    )


    # Setup argparse
    parse = argparse.ArgumentParser(description="Chatbot")
    parse.add_argument("user_prompt", type=str, help="User prompt")
    args = parse.parse_args()

    # Setup message dictionaries with OpenAI SDK.
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]


    # Get Response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )


    # Token Usage Data - Print statements for debugging
    if response is not None:
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')

    print(response.choices[0].message.content)



if __name__ == "__main__":
    main()
