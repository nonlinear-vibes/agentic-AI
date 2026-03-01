import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS, VERBOSE, THINKING, THINKING_TOKEN_LIMIT, KEEP_THOUGHTS
from prompts import system_prompt
import logging


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")

    client = genai.Client(api_key=api_key)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("session_history.txt"),
            # logging.StreamHandler() # Still prints to console
        ]
    )

    messages = []
    
    while True:
        user_input = input("User input: ")
        messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
        logging.info(f"User input: {user_input}")
        print('')
        if user_input == 'X':
            print("Exiting.")
            break

        try:
            final_response = generate_response(client, messages)
            print(f"AI response: {final_response}")
            print('')
        except Exception as e:
            print(f"Error during response generation: {e}")
            break

# agentic loop
def generate_response(client, messages):
        for _ in range(MAX_ITERS):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    thinking_config=types.ThinkingConfig(
                        include_thoughts=THINKING,
                        thinking_budget=THINKING_TOKEN_LIMIT),
                ),
            )

            model_content = response.candidates[0].content

            for part in model_content.parts:
                if part.thought:
                    logging.info(f"MODEL THOUGHT: {part.text}")

            if not KEEP_THOUGHTS:
                cleaned_parts = [p for p in model_content.parts if not p.thought]
                messages.append(types.Content(role="model", parts=cleaned_parts))
            else:
                messages.append(model_content)

            if response.function_calls:
                for function_call in response.function_calls:
                    logging.info(f"- Calling function: {function_call.name}({function_call.args})")

                    if VERBOSE:
                        print(f"- Calling function: {function_call.name}({function_call.args})")

                    result = call_function(function_call)
                    logging.info(f"->: {result}")
                    
                    if VERBOSE:
                        print(f"-> {result}")

                    messages.append(types.Content(
                        role="tool",
                        parts=[types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": result}
                        )]
                    ))
                continue

            text_parts = [p.text for p in model_content.parts if p.text and not p.thought]
            final_text = "".join(text_parts)
            logging.info(f"Final response: {final_text}")
            return final_text
            

if __name__ == "__main__":
    main()
