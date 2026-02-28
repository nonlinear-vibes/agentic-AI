import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS
from prompts import system_prompt



def main():
    verbose = True
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")

    client = genai.Client(api_key=api_key)

    messages = []
    
    while True:
        user_input = input("User input: ")
        messages = [types.Content(role="user", parts=[types.Part(text=user_input)])]
        print('')
        if user_input == 'X':
            print("Exiting.")
            break

        try:
            final_response = generate_response(client, messages, verbose)
            print(f"AI response: {final_response}")
            print('')
        except Exception as e:
            print(f"Error during response generation: {e}")
            break

# agentic loop with function calls
def generate_response(client, messages, verbose=False):
        for _ in range(MAX_ITERS):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )

            if response.function_calls:
                for function_call in response.function_calls:
                    if verbose:
                        print(f"- Calling function: {function_call.name}({function_call.args})")

                    result = call_function(function_call)

                    if not result:
                        raise RuntimeError(f"Empty function response for {function_call.name}")
                    
                    if verbose:
                        print(f"-> {result}")

                    messages.append(types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call.name, response={"result": result})]))

            text_parts = [part.text for part in response.candidates[0].content.parts if part.text]
            final_text = "".join(text_parts)

            if final_text:
                if not response.function_calls:
                    messages.append(types.Content(role="model", parts=[types.Part(text=final_text)]))
                
                return final_text

            


if __name__ == "__main__":
    main()
