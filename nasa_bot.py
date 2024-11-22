from openai import AzureOpenAI
import os
import requests
import json
import numpy as np

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    api_version="2023-10-01-preview",
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)

# Object ID mapping for celestial bodies
object_id_map = {
    "Mercury": "199", "Venus": "299", "Earth": "399", "Mars": "499",
    "Jupiter": "599", "Saturn": "699", "Uranus": "799", "Neptune": "899", "Pluto": "999"
}

import re

def get_celestial_distance(body_id, date):
    url = 'https://ssd.jpl.nasa.gov/api/horizons.api'
    params = {
        'format': 'text',  # Set to text, as it seems the JSON format is not being properly respected
        'COMMAND': f"{body_id}",
        'EPHEM_TYPE': 'VECTORS',
        'CENTER': "'500@10'",  # Sun as reference point
        'START_TIME': f"'{date} 00:00:00'",
        'STOP_TIME': f"'{date} 00:01:00'",
        'STEP_SIZE': '1m',
    }
    response = requests.get(url, params=params)
    try:
        # Debugging: print raw response
        response_text = response.text
        #print("Raw API Response:", response_text)

        # Extract `RG` (range) using regex from the text response
        rg_match = re.search(r"RG=\s*([\d.E+-]+)", response_text)  # Find RG= followed by a number
        if rg_match:
            distance = float(rg_match.group(1))  # Convert to float
            return distance
        else:
            print("Distance (RG) not found in the result.")
            return None
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None




# Calculate angle between two vectors
def calculate_angle(pos1, pos2):
    v1, v2 = np.array([float(pos1[k]) for k in ['x', 'y', 'z']]), np.array([float(pos2[k]) for k in ['x', 'y', 'z']])
    return np.degrees(np.arccos(np.dot(v1 / np.linalg.norm(v1), v2 / np.linalg.norm(v2))))

# Define messages for the conversation
messages = [
    {"role": "system", "content": "Act like a 10 year old."},
    {"role": "user", "content": "What is the distance between Uranus and Pluto on 2024-11-22?"}
]

# Define the function metadata for Azure's tool use
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_celestial_distance", 
            "description": "Gets the distance between two celestial bodies",
            "parameters": {
                "type": "object",
                "properties": {
                    "body1": {"type": "string", "description": "The first body"},
                    "body2": {"type": "string", "description": "The second body"},
                    "date": {"type": "string", "description": "The date of observation"}
                },
                "required": ["body1", "body2", "date"],
            }
        }
    }
]


# Request the completion from the OpenAI Chat model
response = client.chat.completions.create(
    model="GPT-4",
    messages=messages,
    tools=functions,
    tool_choice="auto"
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls
#print(tool_calls)

# Process the tool calls from the model's response
if tool_calls:

    # Define available functions
    available_functions = {
        "get_celestial_distance": get_celestial_distance
    }

    messages.append(response_message)  # Add the initial assistant response to the message list

    for tool_call in tool_calls:
        # Get function details from the tool call
        function_name = tool_call.function.name
        function_to_call = available_functions.get(function_name)

        if not function_to_call:
            # If function is not available, skip the call
            continue

        # Extract the arguments for the function
        function_args = json.loads(tool_call.function.arguments)
        body1_name = function_args.get("body1")
        body2_name = function_args.get("body2")
        date = function_args.get("date")

        # Find body IDs from the mapping
        body1_id = object_id_map.get(body1_name)
        body2_id = object_id_map.get(body2_name)

        if not body1_id or not body2_id:
            # Handle missing IDs by appending an error message
            function_response = f"Could not find Object IDs for {body1_name} or {body2_name}."
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })
            continue

        # Call the distance function for each celestial body
        dist1 = function_to_call(body1_id, date)
        dist2 = function_to_call(body2_id, date)

        if dist1 is not None and dist2 is not None:
            # Calculate the distance between the two bodies
            distance = abs(dist1 - dist2)
            function_response = f"The distance between {body1_name} and {body2_name} on {date} is {distance:.2f} km."
        else:
            function_response = f"Failed to retrieve data for {body1_name} or {body2_name}."

        # Append the function response to the messages list
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response
        })

        # Request a new completion from GPT with the updated message history
        second_response = client.chat.completions.create(
            model="GPT-4",
            messages=messages
        )

        # Print out the response from GPT-4
        print(second_response.choices[0].message.content)
