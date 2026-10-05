import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if api_key is None:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)


def get_github_user(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"{data.get('name')} has {data.get('public_repos')} public repos and {data.get('followers')} followers."
    except requests.exceptions.HTTPError:
        return f"GitHub user '{username}' not found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching GitHub data: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_github_user",
            "description": "Fetch a GitHub user's public profile information, including their name, repo count, and follower count, given their username.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The GitHub username to look up, e.g. torvalds"
                    }
                },
                "required": ["username"]
            }
        }
    }
]

def run_assistant():
    messages=[]
    print("--- AI GitHub Assistant ---")
    print("Ask me about any GitHub user. Type 'exit' to quit.\n")

    while True:
        user_input=input("You:")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                result = get_github_user(**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            final_response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                tools=tools
            )

            final_text = final_response.choices[0].message.content
            print(f"Assistant: {final_text}\n")
            messages.append({"role": "assistant", "content": final_text})

        else:
            print(f"Assistant: {response_message.content}\n")
            messages.append({"role": "assistant", "content": response_message.content})


if __name__ == "__main__":
    run_assistant()

    
