import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS
from prompts import system_prompt



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")

    client = genai.Client(api_key=api_key)

    user_input = input("User input: ")
    messages   = [f"user: {user_input}"]
    print('')
    
    while user_input != 'X':
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        counter = 0
        while response.function_calls and counter < MAX_ITERS:
            for function_call in response.function_calls:
                print(f"- Calling function: {function_call.name}({function_call.args})")
                function_result = call_function(function_call)
                if len(function_result) == 0:
                    raise RuntimeError(f"Empty function response for {function_call.name}")
                
                messages.append(f"Function called: {function_call.name}({function_call.args})")
                messages.append(f"Function result: {function_result}")
                print(f"- Function result: {function_result}")
                print('')

            response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
                ),
            )
            counter += 1
    
        if response.text is not None:
            print(f"AI response: {response.text}")
            print('')
            messages.append(f"agent: {response.text}")

        

        user_input = input("User input: ")
        print('')
        messages.append(f"user: {user_input}")

    print(messages)


if __name__ == "__main__":
    main()
