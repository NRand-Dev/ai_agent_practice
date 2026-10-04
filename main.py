import sys
import os
import argparse
import json

from dotenv import load_dotenv

from openai import OpenAI, chat

from prompts import system_prompt
from call_function import available_functions, call_function


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



    for _ in range(20):
        # Get Response
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        # Verbose flag logic
        if args.verbose == True and response is not None:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage.prompt_tokens}')
            print(f'Response tokens: {response.usage.completion_tokens}')


        # Check for functin calls
        # ## Assistant Messages appended here
        message = response.choices[0].message
        messages.append(message)

        ## Tool calls, print output, add to messages/convo history
        # If not tool calls, return the response
        if not message.tool_calls:
            print(message.content)
            return

        elif message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)

                if not result_message["content"]:
                    raise Exception(f"ERROR: Unexpected error")
                if args.verbose:
                    print(f"-> {result_message['content']}")

                messages.append(result_message)
                #print(f'{result_message}')

        # Check for maximum iterations
        if _ > 20:
            print(f"ERROR: More than 20 iterations.")
            sys.exit(1)


if __name__ == "__main__":
    main()
