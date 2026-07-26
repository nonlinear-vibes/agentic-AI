import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from config import MAX_ITERS, VERBOSE, MODEL_ID, log_event
from prompts import SYSTEM_PROMPT


def main():
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        user_input = input("User input: ")
        
        if user_input.strip().lower() in ("x", "exit", "quit"):
            print("Exiting.")
            break

        messages.append({"role": "user", "content": user_input})
        log_event("User input", user_input)
        print('')

        try:
            final_response = generate_response(client, messages)
            print("----------------------------------------------------------------")
            print(messages)
            print("----------------------------------------------------------------")
            print(f"AI response: {final_response}")
            print('')
        except Exception as e:
            print(f"Error during response generation: {e}")
            break

# agentic loop
def generate_response(client, messages):
        for _ in range(MAX_ITERS):
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
                tools=available_functions,
                extra_body={
                    "reasoning": {
                        "effort": "low",
                        "summary": "auto"
                    }
                }
            )

            message = response.choices[0].message
            assistant_msg = {
                "role": "assistant",
                "content": message.content
            }

            reasoning = getattr(message, "reasoning", None)
            if reasoning:
                assistant_msg["reasoning"] = reasoning
                log_event("AI reasoning", reasoning)

            if message.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ] # list of dicts
                messages.append(assistant_msg)

                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    log_event("Function call", {"name": function_name, "args": function_args})

                    if VERBOSE:
                        print(f"- Calling function: {function_name}({function_args})")

                    try:
                        result = call_function(function_name, function_args)
                    except Exception as e:
                        result = {"erroe": str(e)}

                    log_event("Function result", {"result": result})                    
                    if VERBOSE:
                        print(f"-> {result}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result)
                    })

                continue

            messages.append(assistant_msg)
            
            final_text = message.content or ""
            log_event("AI response", {"text": final_text})
            return final_text
        
        return "Error: Max iterations reached without a final answer."
        

if __name__ == "__main__":
    main()
