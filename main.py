import os
import json
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Your custom function
def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The Weather of {city} is {response.text}"
    return "Something went wrong!!"

def main():
    user_query = input("> ")
    
    # 1. Define the tool so the LLM knows it exists and what arguments it needs
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current real-time weather and temperature for a given city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city, e.g. London, Tokyo",
                        }
                    },
                    "required": ["city"],
                },
            },
        }
    ]

    # 2. Use a System Prompt to give the LLM its TV reporter persona
    messages = [
        {
            "role": "system", 
            "content": "You are an energetic and helpful TV weather reporter. Use the provided weather data to give the forecast and add practical, caring advice (like bringing an umbrella, wearing sunscreen, or staying hydrated) based on the specific conditions."
        },
        {"role": "user", "content": user_query}
    ]

    # 3. First API call: The LLM analyzes the prompt and decides if it needs to use the tool
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b", # Use your active free-tier model here
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 4. If the LLM decides it needs weather data, it will return a tool_call request
    if tool_calls:
        # Append the LLM's request to the conversation history
        messages.append(response_message)
        
        for tool_call in tool_calls:
            if tool_call.function.name == "get_weather":
                # Extract the city name the LLM pulled from the user's prompt
                function_args = json.loads(tool_call.function.arguments)
                city = function_args.get("city")
                
                # Execute your actual Python code
                print(f"[System: Fetching real-time data for {city}...]")
                weather_result = get_weather(city)
                
                # Append the raw data back into the conversation history
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": "get_weather",
                        "content": weather_result,
                    }
                )
        
        # 5. Second API call: Send the raw data back to the LLM so it can write the final TV report
        final_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages
        )
        print(f"\n{final_response.choices[0].message.content}")
        
    else:
        # If no tool was needed (e.g., the user just typed "Hello")
        print(f"\n{response_message.content}")

if __name__ == "__main__":
    main()