import os
import argparse
from dotenv import load_dotenv
from prompts import system_prompt

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
    # Add optional "Verbose" flag - Print extra prompt and response details.
    parse.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parse.parse_args()

    # Setup message dictionaries with OpenAI SDK.
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]


    # Get Response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    # Verbose flag logic
    if args.verbose == True and response is not None:
        print(f'User prompt: {args.user_prompt}')
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')



    print(response.choices[0].message.content)



if __name__ == "__main__":
    main()
