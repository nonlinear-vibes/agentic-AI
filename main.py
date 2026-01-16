import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")

    client = genai.Client(api_key=api_key)

    user_input = input("User input: ")
    messages = [f"user: {user_input}"]
    print('')
    
    while user_input != 'X':
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            )
        print(f"AI response: {response.text}")
        print('')
        messages.append(f"agent: {response.text}")
        user_input = input("User input: ")
        print('')
        messages.append(f"user: {user_input}")


if __name__ == "__main__":
    main()
